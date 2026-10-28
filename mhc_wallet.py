import os
import binascii
import json
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError

class MHCWallet:
    def __init__(self):
        # Generate ECC Private Key using SECP256k1 curve (same standard as Bitcoin)
        self._private_key = SigningKey.generate(curve=SECP256k1)
        self._verifying_key = self._private_key.get_verifying_key()
        self.address = self.generate_address()

    def generate_address(self):
        # Derive public wallet address from SECP256k1 public key
        pub_key_bytes = self._verifying_key.to_string()
        return "MHC" + binascii.hexlify(pub_key_bytes[:20]).decode('utf-8')

    def export_private_key(self):
        # Export raw hex private key for backup
        return binascii.hexlify(self._private_key.to_string()).decode('utf-8')

    @staticmethod
    def import_private_key(hex_private_key):
        # Load existing wallet from hex private key string
        key_bytes = binascii.unhexlify(hex_private_key)
        wallet = MHCWallet.__new__(MHCWallet)
        wallet._private_key = SigningKey.from_string(key_bytes, curve=SECP256k1)
        wallet._verifying_key = wallet._private_key.get_verifying_key()
        wallet.address = wallet.generate_address()
        return wallet

    def sign_transaction(self, recipient_address, amount_maths, fee_maths):
        # Format standardized payload for cryptographic signing
        payload = {
            "sender": self.address,
            "recipient": recipient_address,
            "amount": amount_maths,
            "fee_total": fee_maths
        }
        message_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        signature_bytes = self._private_key.sign(message_bytes)
        
        return {
            "payload": payload,
            "signature": binascii.hexlify(signature_bytes).decode('utf-8'),
            "public_key": binascii.hexlify(self._verifying_key.to_string()).decode('utf-8')
        }

    @staticmethod
    def verify_transaction_signature(signed_transaction):
        try:
            payload = signed_transaction["payload"]
            signature_hex = signed_transaction["signature"]
            public_key_hex = signed_transaction["public_key"]

            message_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
            signature_bytes = binascii.unhexlify(signature_hex)
            public_key_bytes = binascii.unhexlify(public_key_hex)

            verifying_key = VerifyingKey.from_string(public_key_bytes, curve=SECP256k1)
            return verifying_key.verify(signature_bytes, message_bytes)
        except (BadSignatureError, KeyError, Exception):
            return False

if __name__ == "__main__":
    # Test wallet creation & signature integrity
    test_wallet = MHCWallet()
    print("New MHC Wallet Initialized")
    print(f"Address: {test_wallet.address}")
    print(f"Private Key: {test_wallet.export_private_key()}")
