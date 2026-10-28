import hashlib
import time
import json
from ecdsa import SigningKey, SECP256k1, VerifyingKey

class MHCBlock:
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        # Difficulty 5: Hash must start with '00000'
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()
        return self.hash


class MHCBlockchain:
    def __init__(self):
        self.chain = []
        self.mempool = []
        
        # Absolute Supply Limits and Economics
        self.MAX_SUPPLY = 25_000_000 * 1000000000  # Stored in base Math's units (1 MHC = 1 Billion Maths)
        self.BASE_ANNUAL_EMISSION = 5_000 * 1000000000
        
        # Black Hole Address (Null address with no private key control)
        self.BLACK_HOLE_ADDRESS = "0x0000000000000000000000000000000000000000"
        
        # Create Genesis Block
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transactions = [{
            "sender": "SYSTEM",
            "recipient": "GENESIS_HOLDER",
            "amount": 0,
            "fee_total": 0,
            "fee_burned_blackhole": 0,
            "fee_miner_reward": 0
        }]
        genesis_block = MHCBlock(index=0, previous_hash="0", transactions=genesis_transactions, nonce=0)
        genesis_block.hash = genesis_block.mine_block(difficulty=5)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, recipient, amount, fee_total):
        # Black Hole Engine: 95% of fees are permanently burned, 5% goes to miner reward
        fee_burned = fee_total * 0.95
        fee_miner = fee_total * 0.05

        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "fee_total": fee_total,
            "fee_burned_blackhole": fee_burned,
            "fee_miner_reward": fee_miner
        }
        self.mempool.append(transaction)
        return self.get_latest_block().index + 1

    def mine_pending_transactions(self, miner_address):
        if not self.mempool:
            return None

        # Reward transaction for the miner including collected 5% fees
        total_miner_fees = sum([tx["fee_miner_reward"] for tx in self.mempool])
        
        # Apply strict issuance rules (5,000 MHC fixed + quadrennial adjustments)
        reward_tx = {
            "sender": "NETWORK_EMISSION",
            "recipient": miner_address,
            "amount": self.BASE_ANNUAL_EMISSION + total_miner_fees,
            "fee_total": 0,
            "fee_burned_blackhole": 0,
            "fee_miner_reward": 0
        }
        
        block_transactions = [reward_tx] + self.mempool
        
        new_block = MHCBlock(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            transactions=block_transactions
        )
        
        new_block.mine_block(difficulty=5)
        self.chain.append(new_block)
        
        # Clear mempool after successful block inclusion
        self.mempool = []
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
            if not current.hash.startswith('00000'):
                return False
        return True
