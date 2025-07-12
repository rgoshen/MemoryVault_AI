class ChatEngine:
    def __init__(self, memory_manager):
        if not memory_manager:
            raise ValueError("Memory manager is required")
        self.memory_manager = memory_manager

    def generate_response(self, user_message):
        # Extract topic (very simple for now)
        # Just return something that contains the topic and "understand"
        return f"I understand you mentioned{user_message}."
