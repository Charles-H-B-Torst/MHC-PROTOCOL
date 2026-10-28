import time

class MHCLittleChildEvent:
    """
    The 'Little Child' Protocol Event Engine.
    Every 6 years, a cosmic-monetary convergence occurs, plunging the network 
    into an intense 1-year cryptographic crucible where mining difficulty 
    tightens from 5 zeros to 6 zeros, before easing back to 5 zeros.
    """
    def __init__(self, genesis_timestamp):
        self.genesis_timestamp = genesis_timestamp
        self.YEAR_SECONDS = 31_536_000  # Standard 365 days in seconds
        self.CYCLE_DURATION = 6 * self.YEAR_SECONDS  # Full 6-year cycle
        self.EVENT_DURATION = 1 * self.YEAR_SECONDS  # 1-year crucible duration

    def get_current_difficulty(self, current_timestamp=None):
        if current_timestamp is None:
            current_timestamp = time.time()

        elapsed_time = current_timestamp - self.genesis_timestamp
        if elapsed_time < 0:
            return 5  # Baseline fallback difficulty

        # Position within the current 6-year epoch cycle
        cycle_position = elapsed_time % self.CYCLE_DURATION

        # The 'Little Child' event strikes during the final year of the 6-year cycle (Years 5 to 6)
        event_start_threshold = 5 * self.YEAR_SECONDS

        if cycle_position >= event_start_threshold:
            # The crucible is active: 6 zeros difficulty (Maximum computational torture)
            return 6
        else:
            # Baseline sovereign state: 5 zeros difficulty
            return 5

    def get_event_status(self, current_timestamp=None):
        if current_timestamp is None:
            current_timestamp = time.time()

        elapsed_time = current_timestamp - self.genesis_timestamp
        if elapsed_time < 0:
            return {"status": "Pre-Genesis", "difficulty": 5}

        cycle_position = elapsed_time % self.CYCLE_DURATION
        year_in_cycle = cycle_position / self.YEAR_SECONDS
        is_active = cycle_position >= (5 * self.YEAR_SECONDS)
        
        return {
            "little_child_active": is_active,
            "current_difficulty": 6 if is_active else 5,
            "cycle_year": round(year_in_cycle, 2),
            "target_hash_prefix": "000000" if is_active else "00000",
            "event_phase": "CRUCIBLE (6 Zeros)" if is_active else "EXPANSION (5 Zeros)"
        }

if __name__ == "__main__":
    # Test simulation from genesis timestamp
    mock_genesis = time.time() - (5 * 31_536_000) # Simulating year 5 (event entering active phase)
    engine = MHCLittleChildEvent(genesis_timestamp=mock_genesis)
    print("Little Child Event Engine Test:")
    print(engine.get_event_status())
