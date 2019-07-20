from django.core.serializers.json import DjangoJSONEncoder
from election.models import ElectionConfig, Candidate, Elector, Position
from vote.models import Voted, CandidateVote
from chain.models import BBlock
from django.contrib.auth.models import User
import hashlib
import json
import os
from balletblock import settings
from django.db import transaction, DatabaseError
import datetime
from election.business import ElectionBusiness


class HashCalculator():

    def databaseHash(self):
        hash_dict = {}

        # Include hash for Election Config
        queryset = list(ElectionConfig.objects.all().values('id', 'description', 'start_time', 'end_time', 
                        'block_time_generation', 'guess_rate', 'min_votes_in_block', 'min_votes_in_last_block',
                        'attendance_rate', 'locked').order_by('id'))
        cs_json_str = json.dumps(queryset, cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["election_config"] = queryset
        hash_dict["election_config_hash"] = m.hexdigest()
        

        # Include hash for Candidates
        queryset = list(Candidate.objects.all().values('id', 'name', 'position_id').order_by('id'))
        cs_json_str = json.dumps(queryset, cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["candidates"] = queryset
        hash_dict["candidates_hash"] = m.hexdigest()

        # Include hash for Positions
        queryset = list(Position.objects.all().values('id', 'description', 'quantity').order_by('id'))
        cs_json_str = json.dumps(queryset, cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["positions"] = queryset
        hash_dict["positions_hash"] = m.hexdigest()

        # Include hash for Electors
        queryset = list(Elector.objects.all().values('id', 'user_id').order_by('id'))
        cs_json_str = json.dumps(queryset, cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["electors"] = queryset
        hash_dict["electors_hash"] = m.hexdigest()

        # Include hash for Users
        queryset = list(User.objects.all().values('id', 'first_name', 'last_name', 'email', 'is_superuser').order_by('id'))
        cs_json_str = json.dumps(queryset, cls=DjangoJSONEncoder)
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
        source_list = []

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
                        source_list.append({"file": os.path.join(root, filename), "file_hash": m.hexdigest()})
        
        d = {"source_code": source_list} 

        return json.dumps(d, cls=DjangoJSONEncoder)

class BBlockHandler():

    def shouldAddBlock(self):
        eb = ElectionBusiness()
        # While election is occurring, new blocks should be generated.
        if eb.isOccurring():
            return True
        ec = ElectionBusiness().getCurrentElectionConfig()
        if not ec:
            raise DatabaseError('There is not Election Configuration for the current election')
        # Independently of election is occurring, if we have votes, a new block must be generated.
        if Voted.objects.filter(hash_val__isnull=True).count() > 0 or Voted.objects.filter(hash_val='x').count() > 0:
            return True
        # If election ended and we do not have votes we do not need to generate a block.
        return False
    
    def shouldAddLastBlock(self):
        if self.isLastBlock():
            ec = ElectionBusiness().getCurrentElectionConfig()
            if not ec.isOccurring():
                return True
            if Voted.objects.count() == Elector.objects.count():
                return True
        return False
    
    def isLastBlock(self):
        if self.shouldAddBlock():
            ec = ElectionBusiness().getCurrentElectionConfig()
            if (Voted.objects.count()-ec.min_votes_in_last_block)/Elector.objects.count() > ec.attendance_rate:
                return True
        return False
    
    def checkMinVotes(self, bblock):
        ec = ElectionBusiness().getCurrentElectionConfig()
        if self.shouldAddBlock():
            electors = json.loads(bblock.electors)
            if self.isLastBlock():
                if self.shouldAddLastBlock():
                    return True
            if (len(electors) * Position.objects.count()) >= ec.min_votes_in_block:
                return True
        return False
    
    #def checkGuessRate(self, bblock):
        #TODO: Implement guess rate validation
    #    return False
        
    def checkGuessRate(self,votes_new_block, elector_qty):
        #Highest No of votes -> new block votes - old block votes / no of voters 
        last_block = ast.literal_eval(BBlock.objects.all().order_by('-timestamp_iso')[0].candidate_votes) #ast.literal converts string to list or dictionary easily
        old_block_votes=0
        for i in last_block:
            old_block_votes+=i['quantity']
        guess_rate_val=(int(votes_new_block)-int(old_block_votes))/int(elector_qty)
        return (guess_rate_val)

    def shouldIncludeElectors(self, bblock):
        if not self.checkMinVotes(bblock):
            return (False, 'Number of electors rule is not attended.')
        #if not self.checkGuessRate(bblock):
        #    return (False, 'Guess rate rule is not attended.')
        return (True, '')


    @transaction.atomic
    def add(self):
        if not self.shouldAddBlock():
            return

        if BBlock.objects.all().count() == 0:
            raise DatabaseError('It is not possible to add a block without genesis block')
            
        previous_block = BBlock.objects.all().order_by('-timestamp_iso')[0]

        hc = HashCalculator()

        #bblock = BBlock.objects.create()
        bblock = BBlock()
        bblock.database_hash = hc.databaseHash()
        bblock.hash_of_database_hash = bblock.calculateHashOfDatabaseHash()
        bblock.source_code_hash = hc.sourceCodeHash()
        bblock.hash_of_source_code_hash = bblock.calculateHashOfSourceCodeHash()
        
        bblock.timestamp_iso = datetime.datetime.now().isoformat()
        same_qtt_votes = False
        cv_quantity = 0
        while not same_qtt_votes:
            # Workaround to lock electors who will be locked.
            Voted.objects.filter(hash_val__isnull=True).update(hash_val='x')
            electors = list(Voted.objects.filter(hash_val='x').values())
            candidate_votes = list(CandidateVote.objects.filter().values())
            cv_quantity = self.__count_votes(candidate_votes)
            cv_quantity = cv_quantity - previous_block.total_votes
            if cv_quantity == (len(electors) * Position.objects.count()):
                same_qtt_votes = True

        bblock.candidate_votes = json.dumps(candidate_votes, cls=DjangoJSONEncoder)
        bblock.electors = json.dumps(electors, cls=DjangoJSONEncoder)
        bblock.parent_hash = previous_block.block_hash
        bblock.total_votes = previous_block.total_votes + cv_quantity

        ret = self.shouldIncludeElectors(bblock)
        if not ret[0]:
            bblock.electors = json.dumps([], cls=DjangoJSONEncoder)
            bblock.reason = ret[1]
            Voted.objects.filter(hash_val='x').update(hash_val=None)

        bblock.block_hash = bblock.calculateHash()
        Voted.objects.filter(hash_val='x').update(hash_val=bblock.block_hash)
        bblock.save()

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
        bblock.database_hash = hc.databaseHash()
        bblock.hash_of_database_hash = bblock.calculateHashOfDatabaseHash()
        bblock.source_code_hash = hc.sourceCodeHash()
        bblock.hash_of_source_code_hash = bblock.calculateHashOfSourceCodeHash()
        bblock.electors = json.dumps(list(Voted.objects.all().values()), cls=DjangoJSONEncoder)
        bblock.candidate_votes = json.dumps(list(CandidateVote.objects.all().values()), cls=DjangoJSONEncoder)
        bblock.timestamp_iso = datetime.datetime.now().isoformat()
        bblock.total_votes = 0
        bblock.block_hash = bblock.calculateHash()
        bblock.parent_hash = '0'.zfill(128)
        bblock.reason=''
        bblock.save()
   
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
    
    # @transaction.atomic
    # def attendance_rate(self,votes_new_block, elector_qty):