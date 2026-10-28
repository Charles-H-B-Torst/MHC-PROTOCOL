
import time
import json

class MHCMinerHoper:
    """
    The 'MinerHoper' Autonomous Protocol Engine.
    Triggered precisely every 8 months from genesis, executing a targeted 
    sovereign emission of 10 MHC (fully divided into 10,000,000,000 Maths) 
    distributed equally to every active miner and validator safeguarding the network.
    """
    def __init__(self, genesis_timestamp):
        self.genesis_timestamp = genesis_timestamp
        # Exactly 8 months in seconds (8/12 of a standard 365-day year)
        self.HOPER_INTERVAL_SECONDS = int((8 / 12) * 31_536_000)
        self.EMISSION_PER_MINER_MHC = 10.0
        self.EMISSION_IN_MATHS = int(self.EMISSION_PER_MINER_MHC * 1_000_000_000)
        self.hoper_registry = {}

    def check_and_execute_hoper_pulse(self, active_validators_list, current_timestamp=None):
        """
        Evaluates temporal distance from genesis and fires the 8-month pulse 
        if an interval threshold has been crossed.
        """
        if current_timestamp is None:
            current_timestamp = time.time()

        elapsed_time = current_timestamp - self.genesis_timestamp
        if elapsed_time < 0:
            return {"status": "PRE_GENESIS", "pulse_fired": False}

        # Calculate how many 8-month cycles have elapsed
        current_cycle_index = int(elapsed_time // self.HOPER_INTERVAL_SECONDS)
        next_pulse_timestamp = self.genesis_timestamp + ((current_cycle_index + 1) * self.HOPER_INTERVAL_SECONDS)
        time_until_next_pulse = max(0, next_pulse_timestamp - current_timestamp)

        pulse_key = f"HOPER_CYCLE_{current_cycle_index}"

        # Check if this specific 8-month cycle pulse has already been executed
        if pulse_key not in self.hoper_registry:
            # Execute the sovereign distribution to all active validators/miners
            distribution_ledger = {}
            for validator_address in active_validators_list:
                distribution_ledger[validator_address] = {
                    "reward_mhc": self.EMISSION_PER_MINER_MHC,
                    "reward_maths": self.EMISSION_IN_MATHS,
                    "status": "DISTRIBUTED_AND_LOCKED"
                }

            pulse_record = {
                "cycle_index": current_cycle_index,
                "timestamp_fired": current_timestamp,
                "recipients_count": len(active_validators_list),
                "total_maths_emitted": len(active_validators_list) * self.EMISSION_IN_MATHS,
                "ledger": distribution_ledger
            }

            self.hoper_registry[pulse_key] = pulse_record
            return {
                "status": "PULSE_SUCCESSFULLY_EXECUTED",
                "pulse_fired": True,
                "cycle": current_cycle_index,
                details: pulse_record
            }

        return {
            "status": "INTERVAL_PENDING",
            "pulse_fired": False,
            "cycle": current_cycle_index,
            "seconds_until_next_hoper_pulse": round(time_until_next_pulse, 2)
        }

if __name__ == "__main__":
    # Test simulation of the MinerHoper engine
    mock_genesis = time.time() - (8 * 30 * 86400) # Simulating exact 8-month threshold cross
    hoper_engine = MHCMinerHoper(genesis_timestamp=mock_genesis)
    
    sample_validators = ["MHC_VAL_ALPHA_2026", "MHC_VAL_BETA_2026", "MHC_VAL_OMEGA_2026"]
    print("[*] Testing MinerHoper Autonomous Pulse Engine...")
    result = hoper_engine.check_and_execute_hoper_pulse(sample_validators)
    print(json.dumps(result, indent=2))
