import datetime, hashlib, json, random, sys
import multiprocessing as mp

core_num = 16
difficulty = 5

class pow_data:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1,proof_ans = 0, previous_hash = '0')

    def create_block(self, proof, proof_ans, previous_hash):
        Block = {
            "index": len(self.chain) + 1,
            "date": str(datetime.datetime.now()),
            "timestamp": str(datetime.datetime.now().timestamp()),
            "proof": proof,
            "proof_ans": proof_ans,
            "previous_hash": previous_hash
        } 
        self.chain.append(Block)
        return Block
    
    def get_previous_block(self):
        return self.chain[-1]

    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, previous_proof, i, quit, foundit, return_dict):
        new_proof = random.randint(1, sys.maxsize)
        print(new_proof)
        check_proof = False
        while not quit.is_set():
            while check_proof is False:
                hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
                if hash_operation[:difficulty] == '0'*difficulty:
                    check_proof = True
                    return_dict['new_proof'] = new_proof
                    return_dict['hash_operation'] = hash_operation
                else:
                    new_proof = random.randint(1, sys.maxsize)
                    # new_proof += 1
            foundit.set()
        print(hash_operation)
        
        # return new_proof, hash_operation

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:difficulty] != '0'*difficulty:
                return False
            previous_block = block
            block_index += 1
        return True

blockchain = pow_data() # Creating a Blockchain

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)

    manager = mp.Manager()
    return_dict = manager.dict()
    jobs = []

    quit = mp.Event()
    foundit = mp.Event()
    for i in range(core_num):
        p = mp.Process(target=blockchain.proof_of_work, args=(previous_proof, i, quit, foundit, return_dict))
        jobs.append(p)
        p.start()
    foundit.wait()
    quit.set()

    print('>>>create block')
    proof = return_dict['new_proof']
    proof_ans = return_dict['hash_operation']
    block = blockchain.create_block(proof, proof_ans, previous_hash)
    
    response = {"message": 'Successfully mined a block :)',
                "index": block['index'],
                "date": block['date'],
                "timestamp": block['timestamp'],
                "proof": block['proof'],
                "proof_ans": block['proof_ans'],
                "previous_hash": block['previous_hash']
                }
    return  json.dumps(response)

def get_chain():
    response = {'chian' : blockchain.chain,
                'length' : len(blockchain.chain)
                }
    return  json.dumps(response)

def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : 'Everything is fine. Blockchain is valid ^_^'}
    else:
        response = {'message' : 'We have a problem. Blockchain is invalid :('}
    return  json.dumps(response)

def main():
    while(1):
        block_info = json.loads(mine_block())
        with open('full.log', 'a') as f1:
            print(str(block_info)+'\n')
            f1.write(str(block_info)+'\n')
        with open('time.log', 'a') as f2:
            print(block_info['timestamp']+'\n')
            f2.write(block_info['timestamp']+'\n')

if __name__ == '__main__':
    main()