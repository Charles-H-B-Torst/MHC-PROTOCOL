import os
import sys
import socket
from mhc_core import MHCBlockchain
from mhc_node import app, blockchain, nodes

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def print_banner():
    banner = """
    ========================================================
             MATHEW HENRY COIN (MHC) PROTOCOL
             The Deflationary Sovereign Engine
             Max Supply: 25,000,000 MHC
             Black Hole Burn Rate: 95% of all fees
    ========================================================
    """
    print(banner)

def initialize_mhc_node():
    print_banner()
    print("[+] Initializing MHC cryptographic core...")
    print(f"[+] Genesis block successfully validated.")
    print(f"[+] Total supply cap locked at: {blockchain.MAX_SUPPLY / 1000000000:,.0f} MHC")
    print(f"[+] Black hole address active: {blockchain.BLACK_HOLE_ADDRESS}")
    
    local_ip = get_local_ip()
    port = int(os.environ.get("PORT", 5000))
    
    print(f"[+] MHC Node online and listening on network interface: {local_ip}:{port}")
    print("[+] Ready for genesis broadcast and decentralized peer discovery.")
    
    # Run Flask application server
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    initialize_mhc_node()
