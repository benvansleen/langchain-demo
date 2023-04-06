from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, ZeroShotAgent, AgentExecutor
from langchain.memory import ConversationBufferMemory
from .tools import todo_tool


def load_memory():
    return ConversationBufferMemory(
        memory_key='chat_history',
    )


def run_agent(tools, memory, input):

    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.0,
    )

    tools = load_tools(tools, llm=llm) + todo_tool

    prompt = ZeroShotAgent.create_prompt(
        tools,
        prefix='''
Answer the following questions as best you can. You have access to the following tools:
        ''',
        suffix='''
ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the EXACT name of the tool
Action Input: the input to the tool
Observation: the result of the action
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""

Begin! REMEMBER TO FOLLOW FORMATTING RULES!

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
        max_iterations=3,
        memory=memory,
    )

    return agent_chain.run(input=input)
