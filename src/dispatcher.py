import re
from typing import List, Optional
from .inference_engine import InferenceEngine
from .emotion_engine import EmotionEngine

class Dispatcher:
    """Manages simulation turns and environment context."""
    def __init__(self, model_path: str, persona_a: dict, persona_b: dict):
        self.engine = InferenceEngine(model_path)
        self.emotions = {"AgentA": EmotionEngine(), "AgentB": EmotionEngine()}
        self.personas = {"AgentA": persona_a, "AgentB": persona_b}
        self.drive = {"AgentA": {"satiety": 0.0, "novelty": 0.5}, "AgentB": {"satiety": 0.0, "novelty": 0.5}}
        self.history = []
        self.watcher_state = "Active"

    def _calculate_urgency(self, agent_id: str) -> float:
        emo = self.emotions[agent_id].get_state()
        drv = self.drive[agent_id]
        return max(0.0, (emo["friction"] * 0.5) + (drv["novelty"] * 0.3) - (drv["satiety"] * 0.2) + 0.3)

    def step(self) -> Optional[dict]:
        u_a, u_b = self._calculate_urgency("AgentA"), self._calculate_urgency("AgentB")
        if u_a < 0.2 and u_b < 0.2: return {"type": "silence", "message": "..."}
        speaker_id = "AgentA" if u_a >= u_b else "AgentB"
        other_id = "AgentB" if speaker_id == "AgentA" else "AgentA"
        
        env = "[ENVIRONMENT: 光が刺している]" if self.watcher_state == "Active" else "[ENVIRONMENT: 暗い]"
        context = f"{env}\nState: {self.emotions[speaker_id].get_state()}\nYou are {self.personas[speaker_id]['name']}.\n"
        for h in self.history[-5:]: context += f"{h['role']}: {h['content']}\n"
        
        raw = self.engine.generate(speaker_id, context)
        delta = self.emotions[speaker_id].parse_delta(raw)
        new_state = self.emotions[speaker_id].update(delta)
        
        msg_match = re.search(r"\[MESSAGE\]\s*(.*)", raw, re.DOTALL)
        content = msg_match.group(1).strip() if msg_match else raw
        
        self.drive[speaker_id]["satiety"] = min(1.0, self.drive[speaker_id]["satiety"] + 0.1)
        self.drive[speaker_id]["novelty"] = max(0.0, self.drive[speaker_id]["novelty"] - 0.05)
        self.history.append({"role": self.personas[speaker_id]['name'], "content": content})
        
        return {"speaker": speaker_id, "role": self.personas[speaker_id]['name'], "content": content, "emotions": new_state}
