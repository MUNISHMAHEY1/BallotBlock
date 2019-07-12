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


class HashCalculator():

    def databaseHash(self):
        hash_dict = {}

        # Include hash for Election Config
        queryset = ElectionConfig.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict['election_config'] = m.hexdigest()

        # Include hash for Candidates
        queryset = Candidate.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict['candidates'] = m.hexdigest()

        # Include hash for Positions
        queryset = Position.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict['positions'] = m.hexdigest()

        # Include hash for Electors
        queryset = Position.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict['electors'] = m.hexdigest()

        # Include hash for Users
        queryset = User.objects.all()
        cs_json_str = json.dumps(list(queryset.values()), cls=DjangoJSONEncoder)
        m = hashlib.sha512()
        m.update(cs_json_str.encode("utf-8"))
        hash_dict['users'] = m.hexdigest()

        return {'database':hash_dict}

    def __ignoreFile(self, filename):
        if filename.startswith('.'):
            return True
        if filename.endswith('.pyc'):
            # print(filename)
            return True
        return False

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

        return {'souce_code':hash_dict}

class BBlockHandler():

    @transaction.atomic
    def add(self):

        if BBlock.objects.all().count() == 0:
            raise Exception('It is not possible to add a block without genesis block')

        last_block = None
        if BBlock.objects.all().count() > 0:
            last_block = BBlock.objects.all().order_by('-timestamp_iso')[0]

        hc = HashCalculator()

        #bblock = BBlock.objects.create()
        bblock = BBlock()
        bblock.database_hash = str(hc.databaseHash())
        bblock.source_code_hash = str(hc.databaseHash())
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
        bblock.total_votes = cv_quantity
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
        bblock.source_code_hash = str(hc.databaseHash())
        bblock.electors = str(list(Voted.objects.all().values()))
        bblock.candidate_votes = str(list(CandidateVote.objects.all().values()))
        bblock.timestamp_iso = datetime.datetime.now().isoformat()
        bblock.total_votes = 0
        bblock.block_hash = bblock.calculateHash()
        bblock.parent_hash = '0'.zfill(128)
        bblock.save()