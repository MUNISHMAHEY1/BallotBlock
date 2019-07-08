from django.core.serializers.json import DjangoJSONEncoder
from election.models import ElectionConfig, Candidate, Elector, Position
from vote.models import Voted, CandidateVote
from chain.models import BlockStructure
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


class BBlock():

    def __init__(self, source_code, database):
        self.source_code = source_code
        self.database = database

    def getDatabaseHash(self):
        #TODO: Returns a dictionary with the information of database
        #return self.database

    def getSourceCodeHash(self):
        #TODO: Returns a dictionary with the information of database
        #return self.source_code

    def getElectors(self):
        #TODO: Returns a list with electors in this block which already voted
        return self.electors

    def getCandidateVotes(self):
        #TODO: Retunrs a dictionary with Candidates and votes received
        return self.candidate_votes

    def getHash(self):
        #TODO: Calculates the hash of the block based on information inside the block.
        #This function
    
    def getPreviousHash(self):
        #TODO: Retunrs self.previous_hash

    def getBlockDateTimeGeneration(self):
        #TODO: Returns a timestamp of the block generation.
        #This information should be added in the block also.

    def read(self, block_number):
        #TODO: Read json of file and load information to instance variables.
        #Read file
        #Load database_hash
        #Load source_code_hash
        #Load Electors
        #Load Votes
    
    def retrieve(self):
        #TODO: Read information from database
        hc = HashCalculator()
        self.database_hash = hc.databaseHash
        self.source_code = hc.databaseHash
        self.candidate_votes = CandidateVote.objects.filter().values()
        self.electors = Voted.objects.filter(hash_val=None).values()
        '''
        .
        .
        .
        '''
           

    '''
    def write(self):
        #TODO: Just as a good practice, try to refactor the write function.
        It should be simple like:
        self.retrieve()
        content_list = []
        content_list.append(self.getDatabaseHash())
        content_list.append(self.getSourceCodeHash())
        .
        .
        .
        content_list.append(self.getPreviousHash())
        json_content = json.dumps(content_list)
        with open(file):
            file.write(json_content)
    '''
    

    def write(self):
        # TODO: Implement the write method to write in a file
        print("Inside write")
        queryset_elecConfig = ElectionConfig.objects.all()
        #print(dir(queryset))
        queryset_voted = Voted.objects.all().filter(hash_val=None)
        queryset_CandidateVote = CandidateVote.objects.all()
        queryset_voted_prevblock= Voted.objects.exclude(hash_val=None)
        genysisBlockCheck=BlockStructure.objects.all()
        #print(queryset_elecConfig.values()[0]['start_time'])
        #print(queryset_voted.values())
        #print(queryset_CandidateVote.values())
        # print(queryset_voted_prevblock.values())
        # prev_block_data=queryset_voted_prevblock.values()
        prev_block_data=genysisBlockCheck.values()
        genysisBlock=0
        
        if prev_block_data:
            genysisBlock=1
        else:
            genysisBlock=0
        
        count_voters=0
        electors_voted=[]       
        for i in queryset_voted.values():
             count_voters=count_voters+1
             print (i)
             #elector_id['elector_id']=i['elector_id']
             electors_voted.append(i['elector_id'])

        #print ("No of electors voted = ", count_voters)
        print('Electors who voted=',electors_voted)
        
        candidate_votes=[]
        count_votes=0
        for i in queryset_CandidateVote.values():
             count_votes=count_votes + i['quantity']
             print (i)
             candidate_votes.append(i)
        print ("No of  votes= ", count_votes)
        
        dbHash={}
        scHash={}
        Block_data={}
        # prev_block_hash=None
        path_main=os.getcwd()
        if count_voters == count_votes:
            
            print('Valid')
            
            hash_val=HashCalculator()
            dbHash=dict(hash_val.databaseHash())
            scHash=dict(hash_val.sourceCodeHash())
            filepath= path_main + '\\' +'Blockchain'
            # genysisBlock=1

            if not genysisBlock:
                
                genysisBlock_prevHash={'database_hash':dbHash, 'sc_hash':scHash}
                genisysFileParentHashPath=filepath+'\\'+'genisysBlockParentHAsh.json'

                try:
                    os.makedirs(filepath) 
                
                    with open(genisysFileParentHashPath, 'w') as fp:
                        json.dump(genysisBlock_prevHash, fp)
                    fp.close()

                    with open(genisysFileParentHashPath,'r') as fp2:
                        m2 = hashlib.sha512()
                        data2=fp2.read()
                        m2.update(data2.encode("utf-8"))
                        # m.update(cs_json_str.encode("utf-8"))
                        hash_val_genParent=m2.hexdigest()
                    fp2.close()
                    print ('Hash of Genisys block parent hash= ',hash_val_genParent)

                    Block_data={'database_hash':dbHash,'sc_hash':scHash,'prev_hash':hash_val_genParent}
                    # genysisBlock_filename='0.json'
                    # BlockStructure.objects.all().delete()
                    genysisBlock_filepath = filepath + '\\' + '0.json'
                    with open(genysisBlock_filepath, 'w') as fp:
                        json.dump(Block_data, fp)
                    fp.close()
                    genblockNumber=0

                    genBlockwrite= BlockStructure.objects.create(BlockNo=genblockNumber,ParentHash=hash_val_genParent)
                    genBlockwrite.save()
                    return 1
                except FileExistsError:
                    print ("File Exists")
                    
                    # print ("Parent has for genysis block already exists")
                    # if os.path.isfile(genisysFileParentHashPath): #if file exists remove the file
                    #     #if os.path.getsize(genisysFileParentHashPath)>0: # if file is not empty
                    #     os.remove(genisysFileParentHashPath) # remove the file if it exists
                        
                    #     with open(genisysFileParentHashPath, 'w') as fp:
                    #         json.dump(genysisBlock_prevHash, fp)
                    #     fp.close()

                    #     with open(genisysFileParentHashPath,'r') as fp2:
                    #         m2 = hashlib.sha512()
                    #         data2=fp2.read()
                    #         m2.update(data2.encode("utf-8"))
                    #         # m.update(cs_json_str.encode("utf-8"))
                    #         hash_val_genParent=m2.hexdigest()
                    #     fp2.close()
                    #     print ('Hash of Genisys block parent hash= ',hash_val_genParent)
                
                    # Block_data={'database_hash':dbHash,'sc_hash':scHash,'voters_voted':electors_voted,
                    #             'candidates_votes':candidate_votes,'total_votes':count_votes,'prev_hash':hash_val_genParent}
                    # # genysisBlock_filename='0.json'
                    # genysisBlock_filepath = filepath + '\\' + '0.json'
                    # with open(genysisBlock_filepath, 'w') as fp:
                    #     json.dump(Block_data, fp)
                    # fp.close()
                    # genblockNumber=0
                    # genBlockwrite= BlockStructure.objects.create(BlockNo=genblockNumber,ParentHash=hash_val_genParent)
                    # genBlockwrite.save()

            else:
                # prev_block_data2=BlockStructure.objects.all()
                # data_prevBlock=prev_block_data2.values().reverse()[0]
                prev_block_data2=BlockStructure.objects.latest('BlockNo')
                prevBlockNo=prev_block_data2.BlockNo
                lastBlock=filepath + '\\' + str(prevBlockNo) + '.json'
                
                
                with open(lastBlock,'r') as fp2:
                    m2 = hashlib.sha512()
                    data2=fp2.read()
                    m2.update(data2.encode("utf-8"))
                    # m.update(cs_json_str.encode("utf-8"))
                    hash_val_lastBlock=m2.hexdigest()
                fp2.close()

                NewBlock_data={'database_hash':dbHash,'sc_hash':scHash,'voters_voted':electors_voted,
                            'candidates_votes':candidate_votes,'total_votes':count_votes,'prev_block_hash':hash_val_lastBlock}
                
                newBlockNo= prevBlockNo + 1
                newBlockPath= filepath + '\\' + str(newBlockNo) + '.json'

                with open(newBlockPath, 'w') as fp:
                    json.dump(NewBlock_data, fp)
                fp.close()
                
                #Update the BlockStructure database
                NewBlockWrite= BlockStructure.objects.create(BlockNo=newBlockNo,ParentHash=hash_val_lastBlock)
                NewBlockWrite.save()

                return 1
                # parentHash=data_prevBlock['ParentHash']

                # for i in data_prevBlock:
                #     print ("i:",i)
                
                # for i in prev_block_data2:
                #     print (i)
            # print (dbHash,scHash)
            # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # blockchain="Blockchain"
            # for root,dirs,files in os.walk(BASE_DIR):
            #     if blockchain not in dirs:
            #         if not os.path.exists(os.path.abspath(blockchain)):
            #             os.mkdir(blockchain)
            #     else:
            #         print(os.path.dirname(os.path.abspath(blockchain)))
            # Block_data={'database_hash':dbHash,'sc_hash':scHash,'voters_voted':electors_voted,
            # 'candidates_votes':candidate_votes,'total_votes':count_votes,'prev_block_hash':}
            
            # print (Block_data)


        # with open('result.json', 'w') as fp:
        #     json.dump(sample, fp)
        #pass

    def validate(self):
        # TODO: Implement the write method to write in a file
        pass

class BChain():

    def __init__(self):
        # TODO: Read all the blocks
        # self.blocks = readBlocks
        pass

    def addBlock(self):
        # TODO: Implement add new block in a chain
        pass

    def validatebc(self):
        # TODO: Validate the chain
        pass

    def read(self):
        # TODO: Read all the files and populate the cain


