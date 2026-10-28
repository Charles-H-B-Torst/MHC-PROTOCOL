import time
import json

class MHCHeirCoinEngine:
    """
    The 'HeirCoin' Micro-Pulse Emission Engine.
    Executes a microscopic, rhythmic heartbeat across the network: exactly every 
    24 hours, a trivial yet sovereign emission of 100 Maths is injected. 
    A quiet, perpetual pulse ensuring the network's time-ledger never sleeps.
    """
    def __init__(self, genesis_timestamp):
        self.genesis_timestamp = genesis_timestamp
        self.DAY_SECONDS = 86_400  # Exactly 24 hours in seconds
        self.DAILY_EMISSION_MATHS = 100.0  # The micro-pulse of 100 Maths
        self.heir_registry = {}

    def evaluate_heir_pulse(self, beneficiary_address, current_timestamp=None):
        """
        Evaluates elapsed time from genesis and triggers the 24-hour micro-emission 
        if a new daily threshold has been crossed.
        """
        if current_timestamp is None:
            current_timestamp = time.time()

        elapsed_time = current_timestamp - self.genesis_timestamp
        if elapsed_time < 0:
            return {"status": "PRE_GENESIS", "pulse_emitted": False}

        # Calculate exact day index since genesis
        current_day_index = int(elapsed_time // self.DAY_SECONDS)
        next_pulse_timestamp = self.genesis_timestamp + ((current_day_index + 1) * self.DAY_SECONDS)
        time_until_next_pulse = max(0, next_pulse_timestamp - current_timestamp)

        pulse_key = f"HEIR_DAY_{current_day_index}"

        # Track emission per day and beneficiary
        if pulse_key not in self.heir_registry:
            daily_record = {
                "day_index": current_day_index,
                "timestamp_emitted": current_timestamp,
                "beneficiary": beneficiary_address,
                "maths_emitted": self.DAILY_EMISSION_MATHS,
                "status": "MICRO_PULSE_SECURED"
            }

            self.heir_registry[pulse_key] = daily_record
            return {
                "status": "HEIRCOIN_PULSE_SUCCESS",
                "pulse_emitted": True,
                "day": current_day_index,
                "details": daily_record
            }

        return {
            "status": "DAY_CYCLE_PENDING",
            "pulse_emitted": False,
            "day": current_day_index,
            "seconds_until_next_heir_pulse": round(time_until_next_pulse, 2)
        }

if __name__ == "__main__":
    # Test simulation of the HeirCoin micro-pulse engine
    mock_genesis = time.time() - 86_400  # Simulating crossing the 24-hour mark
    heir_engine = MHCHeirCoinEngine(genesis_timestamp=mock_genesis)
    
    test_wallet = "MHC_HEIR_SOVEREIGN_HOLDER_2026"
    print("[*] Testing HeirCoin 24h Micro-Pulse Engine...")
    result = heir_engine.evaluate_heir_pulse(test_wallet)
    print(json.dumps(result, indent=2))

 
