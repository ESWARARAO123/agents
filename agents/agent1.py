from langchain.llms import Ollama
from langchain.chains import ConversationChain
from memory.episodic_memory import memory

llm = Ollama(model="mistral")

def agent1(prompt):
    chain = ConversationChain(llm=llm, memory=memory)
    return chain.run(prompt)
