from langchain.memory import ConversationBufferMemory

class Memory:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.conversation_history = []

    def save_message(self, message):
        self.conversation_history.append({"role": "user", "content": message})
        self.memory.save_context({"input": message}, {"output": ""})

    def save_response(self, response):
        if self.conversation_history:
            self.conversation_history[-1]["response"] = response
        self.memory.save_context({"input": ""}, {"output": response})

    def get_history(self):
        return self.conversation_history

memory = Memory()
