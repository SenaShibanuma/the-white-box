import json
import re

class EmotionEngine:
    """Calculates emotional states: E_{t+1} = E_t * gamma + delta."""
    def __init__(self, gamma=0.95):
        self.gamma = gamma
        self.state = {"congruence": 0.5, "resonance": 0.5, "friction": 0.0, "attenuation": 0.0}

    def parse_delta(self, raw_output: str) -> dict:
        match = re.search(r"\[EMOTION_DELTA\]\s*(\{.*?\})", raw_output, re.DOTALL)
        if match:
            try: return json.loads(match.group(1).strip())
            except: return {}
        return {}

    def update(self, delta: dict) -> dict:
        for key in self.state:
            d = delta.get(key, 0.0)
            self.state[key] = max(0.0, min(1.0, self.state[key] * self.gamma + d))
        return self.state

    def get_state(self) -> dict:
        return self.state.copy()
