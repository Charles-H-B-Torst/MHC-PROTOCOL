import time
import requests
import sys

class MHCMiner:
    def __init__(self, node_url, miner_address):
        self.node_url = node_url
        self.miner_address = miner_address

    def check_pending_transactions(self):
        try:
            response = requests.get(f"{self.node_url}/chain")
            if response.status_code == 200:
                # Simple check loop simulation for active mining readiness
                return True
        except requests.exceptions.RequestException:
            print("[-] Error connecting to local MHC node. Ensure mhc_launcher.py is running.")
            return False
        return False

    def mine(self):
        print(f"[*] Miner initialized for address: {self.miner_address}")
        print(f"[*] Connecting to network node at: {self.node_url}")
        print("[*] Searching for pending transactions in mempool... Press CTRL+C to halt.")

        while True:
            try:
                # Request mining execution on the target node
                response = requests.get(f"{self.node_url}/mine?miner_address={self.miner_address}")
                
                if response.status_code == 200:
                    data = response.json()
                    print("\n[+] ========================================")
                    print(f"[+] BLOCK #{data['block_index']} SUCCESSFULLY MINED!")
                    print(f"[+] Nonce / Proof: {data['nonce']}")
                    print(f"[+] Block Hash: {data['hash']}")
                    print(f"[+] Previous Hash: {data['previous_hash']}")
                    print("[+] Transactions included and 95% fees burned.")
                    print("[+] ========================================\n")
                elif response.status_code == 400:
                    # No transactions in mempool, pause briefly before retrying
                    sys.stdout.write(".")
                    sys.stdout.flush()
                
                time.sleep(5)
            except KeyboardInterrupt:
                print("\n[!] Mining interrupted by user. Shutting down miner.")
                break
            except Exception as e:
                print(f"\n[-] Mining error encountered: {e}")
                time.sleep(10)

if __name__ == "__main__":
    # Default local configuration for genesis and local node mining
    NODE_ENDPOINT = "http://localhost:5000"
    MINER_WALLET = "MHC_GENESIS_SOVEREIGN_HOLDER_2026"
    
    miner = MHCMiner(node_url=NODE_ENDPOINT, miner_address=MINER_WALLET)
    miner.mine()
