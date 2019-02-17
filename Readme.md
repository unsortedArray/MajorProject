## Our crowd funding platform

#### The core runs on all the networks (P) P = peers and host port name is mentioned on the layout

#### Run all the servers using python "filename.py" ** on success it will show the server is running on the port a,b,c

#### Now for all the Nodes make a post request on the postman "/conenct_nodes" with body->raw-> json form with the entries in the network

#### All the routes have been specified below with their purpose 

			* mine_block ** to mine the block

			* get_chain  ** shows the status of the chain on the current node

			* replace_chain ** synchronises the chain with the maximum chain

			* add_transaction ** POST request with json details as in transaction file  


			* is_valid used ** an implicit call to check the internal configuration of the chain
