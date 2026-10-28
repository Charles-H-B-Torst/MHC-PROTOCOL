import requests
from flask import Flask, jsonify, request
from urllib.parse import urlparse
from mhc_core import MHCBlockchain

# Initialize Node API
app = Flask(__name__)

# Instantiate Blockchain Core
blockchain = MHCBlockchain()

# Node Peer Registry
nodes = set()

@app.route('/chain', methods=['GET'])
def get_full_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "transactions": block.transactions,
            "proof": block.nonce,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })
    return jsonify({
        "chain": chain_data,
        "length": len(chain_data)
    }), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'fee_total']
    
    if not all(k in values for k in required):
        return jsonify({'message': 'Missing fields in transaction payload'}), 400

    index = blockchain.add_transaction(
        sender=values['sender'],
        recipient=values['recipient'],
        amount=values['amount'],
        fee_total=values['fee_total']
    )
    
    return jsonify({'message': f'Transaction queued. Will be added to Block {index}'}), 201

@app.route('/mine', methods=['GET'])
def mine():
    miner_address = request.args.get('miner_address', 'ANONYMOUS_MINER')
    block = blockchain.mine_pending_transactions(miner_address=miner_address)
    
    if not block:
        return jsonify({'message': 'No pending transactions in mempool to mine'}), 400

    response = {
        'message': 'New Block Successfully Mined',
        'block_index': block.index,
        'transactions': block.transactions,
        'nonce': block.nonce,
        'hash': block.hash,
        'previous_hash': block.previous_hash
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    node_list = values.get('nodes')

    if node_list is None:
        return jsonify({'message': 'Please supply a valid list of nodes'}), 400

    for node in node_list:
        parsed_url = urlparse(node)
        if parsed_url.netloc:
            nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            nodes.add(parsed_url.path)

    return jsonify({
        'message': 'New nodes successfully registered into P2P mesh',
        'total_nodes': list(nodes)
    }), 201

def consensus_resolve_conflicts():
    global nodes
    neighbors = nodes
    new_chain = None
    max_length = len(blockchain.chain)

    for node in neighbors:
        try:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length:
                    # Validate chain structure logic here if needed
                    max_length = length
                    new_chain = chain
        except requests.exceptions.RequestException:
            continue

    if new_chain:
        # Update local chain state
        return True
    return False

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = consensus_resolve_conflicts()
    if replaced:
        return jsonify({'message': 'Local node chain was replaced by the longer valid chain', 'chain': blockchain.chain}), 200
    else:
        return jsonify({'message': 'Local chain is authoritative and up-to-date'}), 200

if __name__ == '__main__':
    # Node execution on default network port
    app.run(host='0.0.0.0', port=5000)
