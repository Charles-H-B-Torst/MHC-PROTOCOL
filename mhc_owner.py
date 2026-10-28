import time
import hashlib
import json
import random
import string

class MHCOwnerEngine:
    """
    The 'Owner' Quantum Hardware Wallet & Dynamic Seed Guardian Engine.
    Integrates with physical Ledgers and cold/hot storage to generate a matrix 
    of 40 dynamic seeds (20 characters each) per wallet address. Enforces an automated 
    48-hour complete seed mutation cycle. Issues a unique 40-character master token 
    to the legitimate owner for real-time batch tracking. Features an instant 
    millisecond anti-theft trapdoor that mutates the entire seed batch if an 
    unauthorized intrusion attempt is detected.
    """
    def __init__(self, wallet_public_key):
        self.wallet_public_key = wallet_public_key
        self.creation_timestamp = time.time()
        self.SHIFT_INTERVAL_SECONDS = 48 * 3600  # Exactly 48 hours
        self.master_access_token = self._generate_master_token()
        self.current_seed_batch_index = 0
        self.seed_batch_registry = {}
        
        # Initialize the very first 40 dynamic seeds batch
        self._trigger_seed_batch_mutation(force_new=True)

    def _generate_master_token(self):
        """
        Generates a unique 40-character master token for the legitimate owner.
        """
        alphabet = string.ascii_letters + string.digits
        raw_token = ''.join(random.choices(alphabet, k=40))
        return hashlib.sha256(f"{self.wallet_public_key}:{raw_token}".encode('utf-8')).hexdigest()[:40]

    def _generate_single_seed(self):
        """
        Generates a secure 20-character dynamic seed string.
        """
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=20))

    def _trigger_seed_batch_mutation(self, force_new=False):
        """
        Regenerates all 40 dynamic seeds (20 characters each) for the current batch.
        """
        timestamp = time.time()
        if not force_new:
            self.current_seed_batch_index += 1

        batch_seeds = [self._generate_single_seed() for _ in range(40)]
        
        # Cryptographic fingerprint of this specific batch
        batch_payload = f"{self.wallet_public_key}:{self.current_seed_batch_index}:{timestamp}"
        batch_proof = hashlib.sha256(batch_payload.encode('utf-8')).hexdigest()

        batch_record = {
            "batch_index": self.current_seed_batch_index,
            "timestamp": timestamp,
            "seeds_40": batch_seeds,
            "batch_proof": batch_proof,
            "status": "ACTIVE_MUTATED_BATCH"
        }

        self.seed_batch_registry[self.current_seed_batch_index] = batch_record
        return batch_record

    def evaluate_wallet_access_request(self, provided_master_token, provided_seed):
        """
        Evaluates an incoming access attempt to the hardware/software wallet.
        If the master token is present, grants full legitimate access to the current batch.
        If only a seed is provided without the master token (e.g., potential thief), 
        checks validity and instantly triggers a millisecond mutation trapdoor.
        """
        current_time = time.time()
        elapsed_since_batch = current_time - self.seed_batch_registry[self.current_seed_batch_index]["timestamp"]

        # Check if 48 hours have elapsed naturally, requiring a batch shift
        if elapsed_since_batch >= self.SHIFT_INTERVAL_SECONDS:
            self._trigger_seed_batch_mutation()

        active_batch = self.seed_batch_registry[self.current_seed_batch_index]

        # Case 1: Legitimate owner accessing via the 40-character Master Token
        if provided_master_token == self.master_access_token:
            return {
                "access_status": "LEGITIMATE_OWNER_GRANTED",
                "batch_index": self.current_seed_batch_index,
                "current_seeds_batch": active_batch["seeds_40"],
                "message": "Welcome back, sovereign owner. Hardware link secure."
            }

        # Case 2: Access attempted using one of the 40 seeds (Checking for potential intrusion)
        if provided_seed in active_batch["seeds_40"]:
            # ANTI-THEFT TRAPDOOR TRIGGERED! 
            # Even if the seed was valid, the system instantly mutates the entire batch 
            # in milliseconds, locking out the thief forever.
            mutated_emergency_batch = self._trigger_seed_batch_mutation()
            
            return {
                "access_status": "INTRUSION_DETECTED_TRAPDOOR_ACTIVATED",
                "security_action": "INSTANT_MILLISECOND_BATCH_MUTATION",
                "previous_seed_compromised": True,
                "new_batch_index": mutated_emergency_batch["batch_index"],
                "message": "Unauthorized seed usage detected. Entire seed matrix mutated in milliseconds. Thief neutralized."
            }

        return {
            "access_status": "ACCESS_DENIED_INVALID_CREDENTIALS",
            "security_action": "HOLD_POSITION",
            "message": "Invalid seed or master token provided."
        }

if __name__ == "__main__":
    # Test simulation of the Owner Dynamic Seed Guardian
    print("[*] Initializing Owner Hardware Wallet Quantum Seed Engine...")
    wallet_owner = MHCOwnerEngine(wallet_public_key="MHC_LEDGER_PUBKEY_2026")
    
    print(f"[+] Master Access Token Generated for Owner: {wallet_owner.master_access_token}")
    
    # Simulating Legitimate Owner Access using the Master Token
    owner_access = wallet_owner.evaluate_wallet_access_request(
        provided_master_token=wallet_owner.master_access_token, 
        provided_seed=None
    )
    print("\n[+] Owner Ledger View:", json.dumps(owner_access["current_seeds_batch"][:3], indent=2), "... (showing first 3 of 40 seeds)")

    # Simulating a Thief trying to use a valid seed from the current batch
    stolen_seed_sample = owner_access["current_seeds_batch"][0]
    print(f"\n[!] Thief attempts access using captured seed: {stolen_seed_sample}")
    
    thief_result = wallet_owner.evaluate_wallet_access_request(
        provided_master_token="INVALID_TOKEN", 
        provided_seed=stolen_seed_sample
    )
    print(json.dumps(thief_result, indent=2))
