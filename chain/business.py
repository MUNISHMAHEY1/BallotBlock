from django.core.serializers.json import DjangoJSONEncoder
from election.models import ElectionConfig, Candidate, Elector, Position
from django.contrib.auth.models import User
import hashlib
import json
import os
from balletblock import settings


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
            print(filename)
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


class BBlock():

    def __init__(self, source_code, database):
        self.source_code = source_code
        self.database = database

    def write(self):
        # TODO: Implement the write method to write in a file
        pass

    def velidate(self):
        # TODO: Implement the write method to write in a file
        pass

class BChain():

    def addBlock(self):
        # TODO: Implement add new block in a chain
        pass

    def addBlock(self):
        # TODO: Validate the chain
        pass