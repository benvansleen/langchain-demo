from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory


def load_memory():
    return ConversationBufferMemory(
        memory_key='chat_history',
    )


def run_agent(tools, memory, input):

    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.0,
    )

    tools = load_tools(tools, llm=llm)

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix='''
    Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:
        ''',
        suffix='''
    Begin!

    {chat_history}
    Question: {input}
    {agent_scratchpad}
        ''',
        input_variables=['input', 'chat_history', 'agent_scratchpad'],
    )

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    agent = ZeroShotAgent(
        tools=tools,
        llm_chain=llm_chain,
        verbose=True,
    )

    agent_chain = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        memory=memory,
    )

    return agent_chain.run(input=input)
