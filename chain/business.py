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

import json

class doubleQuoteDict(dict):
    def __str__(self):
        return json.dumps(self)

    def __repr__(self):
        return json.dumps(self)


class HashCalculator():

    def databaseHash(self):
        hash_dict = {}

        # Include hash for Election Config
        queryset = ElectionConfig.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["election_config"] = cs_json_str
        hash_dict["election_config_hash"] = m.hexdigest()
        

        # Include hash for Candidates
        queryset = Candidate.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["candidates"] = cs_json_str
        hash_dict["candidates_hash"] = m.hexdigest()

        # Include hash for Positions
        queryset = Position.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["positions"] = cs_json_str
        hash_dict["positions_hash"] = m.hexdigest()

        # Include hash for Electors
        queryset = Position.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["electors"] = cs_json_str
        hash_dict["electors_hash"] = m.hexdigest()

        # Include hash for Users
        queryset = User.objects.all()
        cs_json_str = json.dumps(list(queryset.values('id', 'first_name', 'last_name', 'email')), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict["users"] = cs_json_str
        hash_dict["users_hash"] = m.hexdigest()

        d = {"database":hash_dict}

        return doubleQuoteDict(d)

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
            raise Exception('It is not possible to add a block without genesis block')
            
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
            electors = list(Voted.objects.filter(hash_val='x').values())
            candidate_votes = list(CandidateVote.objects.filter().values())
            cv_quantity = self.__count_votes(candidate_votes)
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