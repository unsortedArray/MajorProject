# adding the core of the blockChain
# step one creating the block
## later we will convert it to currency



import datetime
import hashlib
import json

from flask import Flask, jsonify


# building a blockchain

class coreChain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_hash ='0')
    
    def create_block (self,proof,prev_hash):
        block = {'index':len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash
                 }
        self.chain.append(block)
        return block
        
    
    def get_prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof  = 1
        check_proof = False
        while(check_proof  is False):
            hash_operation =  hashlib.sha256(str(new_proof**2 - prev_proof**2 ).encode()).hexdigest()
            
            if hash_operation[:6] =='000000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        prev_block = chain[0]
        block_index = 1
        
        while block_index  < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(prev_block):
                return False
            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_operation[:6] !='000000':
                return False
            prev_block = block
            block += 1
                   

# creating the web app 
app = Flask(__name__)


coreChainInst = coreChain() 

#Mining the block 
@app.route('/mine_block', methods = ["GET"])
def mine_block():
    prev_block = coreChainInst.get_prev_block()
    prev_proof = prev_block['proof']
    proof = coreChainInst.proof_of_work(prev_proof)
    prev_hash = coreChainInst.hash(prev_block)
    block = coreChainInst.create_block(proof,prev_hash)
    response ={'message': 'congrats',
               
               'index' : block['index'],
               'timestamp' : block['timestamp'],
               'proof' : block['proof'],
               'prev_hash' : block['prev_hash']
            }
    return jsonify(response) , 200

# getting the chain 
    

@app.route('/get_chain', methods=["GET"])
def get_chain():
    response ={
            'chain': coreChainInst.chain,
            'length' : len(coreChainInst.chain)
            }
    return jsonify(response), 200


# adding the validity of the chain 
    

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = coreChainInst.is_chain_valid(coreChainInst.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)