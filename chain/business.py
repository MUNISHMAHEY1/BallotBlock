from django.core.serializers.json import DjangoJSONEncoder
from election.models import ElectionConfig, Candidate, Elector, Position
from vote.models import Voted, CandidateVote
from chain.models import BBlock
from django.contrib.auth.models import User
import hashlib
import json
import os
from balletblock import settings
from django.db import transaction
import datetime
import ast

class HashCalculator():

    def databaseHash(self):
        hash_dict = {}

        # Include hash for Election Config
        queryset = list(ElectionConfig.objects.all().values())
        cs_json_str = json.dumps(queryset, cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["election_config"] = queryset
        hash_dict["election_config_hash"] = m.hexdigest()
        

        # Include hash for Candidates
        queryset = list(Candidate.objects.all().values())
        cs_json_str = json.dumps(str(queryset), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["candidates"] = queryset
        hash_dict["candidates_hash"] = m.hexdigest()

        # Include hash for Positions
        queryset = list(Position.objects.all().values())
        cs_json_str = json.dumps(str(queryset), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["positions"] = queryset
        hash_dict["positions_hash"] = m.hexdigest()

        # Include hash for Electors
        queryset = list(Elector.objects.all().values())
        cs_json_str = json.dumps(str(queryset), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["electors"] = queryset
        hash_dict["electors_hash"] = m.hexdigest()

        # Include hash for Users
        queryset = list(User.objects.all().values('id', 'first_name', 'last_name', 'email', 'is_superuser'))
        cs_json_str = json.dumps(str(queryset), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["users"] = queryset
        hash_dict["users_hash"] = m.hexdigest()

        d = {"database":hash_dict}

        return json.dumps(d, cls=DjangoJSONEncoder)

    def __ignoreFile(self, filename):
        if filename.endswith('.py'):
            return False
        if filename.endswith('.js'):
            return False
        if filename.endswith('.css'):
            return False
        if filename.endswith('.html'):
            return False
        return True

    def sourceCodeHash(self):
        BUF_SIZE = 65536
        hash_dict = {}

        for root, dirs, files in os.walk(settings.BASE_DIR):
            for filename in files:
                if not os.path.isdir(os.path.join(root, filename)):
                    if not self.__ignoreFile(str(filename)):
                        m = hashlib.sha512()
                        with open(os.path.join(root, filename), 'rb') as f:
                            while True:
                                data = f.read(BUF_SIZE)
                                if not data:
                                    break
                                m.update(data)
                        hash_dict[os.path.join(root, filename)] = m.hexdigest()

        return {"souce_code":hash_dict}

class BBlockHandler():

    @transaction.atomic
    def add(self):

        if BBlock.objects.all().count() == 0:
            obj=BBlockHandler()
            obj.add_genesis()
            print ("Genysis block")
            # raise Exception('It is not possible to add a block without genesis block')
        
        total_blocks=list(BBlock.objects.all().order_by('-timestamp_iso'))
        total_blocks=len(total_blocks)
        last_block = BBlock.objects.all().order_by('-timestamp_iso')[0]

        hc = HashCalculator()

        #bblock = BBlock.objects.create()
        bblock = BBlock()
        bblock.database_hash = str(hc.databaseHash())
        bblock.hash_of_database_hash = bblock.calculateHashOfDatabaseHash()
        bblock.source_code_hash = str(hc.sourceCodeHash())
        bblock.hash_of_source_code_hash = bblock.calculateHashOfSourceCodeHash()
        
        bblock.timestamp_iso = datetime.datetime.now().isoformat()
        
       
        same_qtt_votes = False
        cv_quantity = 0
        while not same_qtt_votes:
            # Workaround to lock electors who will be locked.
            Voted.objects.filter(hash_val__isnull=True).update(hash_val='x')
            # electors = list(Voted.objects.filter(hash_val='x').values())
            electors = list(Voted.objects.all().values())
            print("electors=",electors)
            no_electors=len(electors) #electors in new block
            print ("No of electors=",no_electors)
            
            candidate_votes = list(CandidateVote.objects.filter().values())
            cv_quantity = self.__count_votes(candidate_votes) #votes in new block
            print("No of Votes=",cv_quantity)
            if total_blocks>1: # for block genysis  there is no need for parameters to be checked
                print("HAHAHA")
                bb=BBlockHandler()
                guess_rate_value=bb.guess_rate(cv_quantity,no_electors)

            if last_block:
                cv_quantity = cv_quantity - last_block.total_votes
            if cv_quantity == (len(electors) * Position.objects.count()):
                same_qtt_votes = True

        bblock.candidate_votes = str(candidate_votes)
        bblock.electors = str(electors)
        
        if last_block:        
            bblock.parent_hash = last_block.block_hash
        else:
            bblock.parent_hash = '0'.zfill(128)
        bblock.block_hash = bblock.calculateHash()
        bblock.total_votes = last_block.total_votes + cv_quantity
        bblock.save()
        Voted.objects.filter(hash_val='x').update(hash_val=bblock.block_hash)

    def __count_votes(self, candidate_votes):
        cv_quantity = 0
        for cv in candidate_votes:
            cv_quantity += cv['quantity']
        return cv_quantity

    @transaction.atomic
    def add_genesis(self):
        hc = HashCalculator()
        #bblock = BBlock.objects.create()
        bblock = BBlock()
        bblock.database_hash = str(hc.databaseHash())
        bblock.hash_of_database_hash = bblock.calculateHashOfDatabaseHash()
        bblock.source_code_hash = str(hc.sourceCodeHash())
        bblock.hash_of_source_code_hash = bblock.calculateHashOfSourceCodeHash()
        bblock.electors = str(list(Voted.objects.all().values()))
        bblock.candidate_votes = str(list(CandidateVote.objects.all().values()))
        bblock.timestamp_iso = datetime.datetime.now().isoformat()
        bblock.total_votes = 0
        bblock.block_hash = bblock.calculateHash()
        bblock.parent_hash = '0'.zfill(128)
        bblock.save()
        print("End")
    
    @transaction.atomic
    def guess_rate(self,votes_new_block, elector_qty):
        #Highest No of votes -> new block votes - old block votes / no of voters 
        last_block = ast.literal_eval(BBlock.objects.all().order_by('-timestamp_iso')[0].candidate_votes) #ast.literal converts string to list or dictionary easily
        old_block_votes=0
        for i in last_block:
            old_block_votes+=i['quantity']
        print("Old_block_values=",old_block_votes)
        print("votes_new_block=",votes_new_block)
        guess_rate_val=(int(votes_new_block)-int(old_block_votes))/int(elector_qty)
        print("Gues val rate=",guess_rate_val)
        return (guess_rate_val)
    
    @transaction.atomic
    def attendance_rate(self,votes_new_block, elector_qty):