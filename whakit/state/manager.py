# whakit/state/state_manager.py

from typing import Dict, List


class StateManager:
    def __init__(self):
        # In-memory state storage
        self.states: Dict[str, Dict] = {}

    def get_state(self, user_id: str) -> Dict:
        return self.states.get(user_id, {})

    def set_state(self, user_id: str, state: Dict):
        self.states[user_id] = state

    def clear_state(self, user_id: str):
        if user_id in self.states:
            del self.states[user_id]

    # New methods for chat history
    def get_chat_history(self, user_id: str) -> List[str]:
        return self.states.get(user_id, {}).get('chat_history', [])

    def append_chat_history(self, user_id: str, message: str):
        if user_id not in self.states:
            self.states[user_id] = {}
        self.states[user_id].setdefault('chat_history', []).append(message)
    
    def clear_chat_history(self, user_id: str):
        if user_id in self.states and 'chat_history' in self.states[user_id]:
            del self.states[user_id]['chat_history']