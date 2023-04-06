import re
from itertools import zip_longest


ansi_escape = re.compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]
    |     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', re.VERBOSE)


def parse_agent_chain(chain):
    chain = ansi_escape.sub('', chain)
    chain = chain.replace('Entering new AgentExecutor chain...', '')
    return ''.join([f'''
> **:blue[Thought]**

{thought.strip()}

> **:green[Action]** ({action if action else ''})


`{action_input if action_input else ' '}`

> **:red[Observation]**

{f'{observation.strip()}' if len(observation.strip()) > 0 else '...'}

---
    ''' for thought, action, action_input, observation in zip_longest(
        re.findall(r'Thought:(\w?.*)', chain),
        re.findall(r'Action:\s+([^\n]+)', chain),
        re.findall(r'Action Input:\s+([^\n]+)', chain),
        re.findall(r'(?<=Observation: )(.*?)(?=Thought:)', chain, re.DOTALL),
        fillvalue='',
    )])


def history(prompts, chains):
    return '\n\n'.join(
        [
            f'''
<hr style="height:10px;background-color:#333;border:none;" />

#### {prompt.strip()}

{chain.strip()}
            ''' for prompt, chain in zip(
                prompts,
                chains,
            )
        ]
    )
