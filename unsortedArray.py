# adding the core of the blockChain
# step one creating the block
## later we will convert it to currency



import datetime
import hashlib
import json

from flask import Flask, jsonify , request
import requests

from uuid import uuid4

from urllib.parse import urlparse



# building a blockchain

class coreChain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, prev_hash ='0')
        self.nodes = set()
    
    def create_block (self,proof,prev_hash):
        block = {'index':len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash,
                 'transactions' : self.transactions
                 }
        self.transactions =[]
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
            block_index += 1
        return True
    

    def add_transactions(self, sender, reciever, ammount):
        self.transactions.append({'sender':sender,
            'reciever':reciever,
            'ammount':ammount

            })
        prev_block = self.get_prev_block()
        return prev_block['index'] +1



    def add_Nodes ( self , address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

# add consesus method

    def replace_chain(self):
        network = self.nodes
       
        longest_chain = None
        max_length = len(self.chain)
        print('max_length'+ str(max_length))
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            
            if response.status_code == 200:
                length =response.json()['length']
                chain = response.json()['chain']
                print(length)
                print(chain)
                if length > max_length and self.is_chain_valid(chain):
                    print("here")
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
# creating the web app 
app = Flask(__name__)

## creating an address for the node on the port 5000

node_address = str(uuid4()).replace('-','')
print(node_address)

coreChainInst = coreChain() 

#Mining the block 
@app.route('/mine_block', methods = ["GET"])
def mine_block():
    prev_block = coreChainInst.get_prev_block()
    prev_proof = prev_block['proof']
    proof = coreChainInst.proof_of_work(prev_proof)
    prev_hash = coreChainInst.hash(prev_block)
    coreChainInst.add_transactions( sender = node_address , reciever ="UnsortedArray" , ammount = 1)

    block = coreChainInst.create_block(proof,prev_hash)
    response ={'message': 'congrats',
               
               'index' : block['index'],
               'timestamp' : block['timestamp'],
               'proof' : block['proof'],
               'prev_hash' : block['prev_hash'],
               'transactions': block['transactions']
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

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transactions_keys= ['sender', 'receiver', 'amount']
    
    if not all (key in json for key in transactions_keys):
        return ' something is missing', 400

    index = coreChainInst.transactions(json['sender'], json['reciever'], json['ammount'])

    response ={'message': f'this transaction will be added to block {index}'}

    return jsonify(response), 201

@app.route('/conenct_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    print(json)
    nodes = json.get('nodes')
    if nodes is None:
        return " Empty Nodes" , 400
    for node in nodes:
        coreChainInst.add_Nodes(node)
    response = { 'message': ' All the nodes are connected',
    'total_nodes' : list(coreChainInst.nodes)

    }
    return jsonify(response), 201

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    replace_chain = coreChainInst.replace_chain()
    if replace_chain == False:
        response = {'message': 'All good. The Blockchain is largest .',
        'actual_chain': coreChainInst.chain}
    else:
        response = {'message': 'Chain had to be chained',
        'new_chain' : coreChainInst.chain}

    return jsonify(response), 200


app.run(host = '0.0.0.0', port = 5000)