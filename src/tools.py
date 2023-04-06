from langchain.agents import tool


FILE = '../todos'


@tool
def make_todo(todo: str) -> str:
    '''Create and store a new TODO item'''
    with open(FILE, 'a') as f:
        f.write(f'{todo}\n')
    return f'Added {todo} to your todo list'


@tool
def remove_todo(i: int) -> str:
    '''Remove the ith TODO item using zero-based indexing. i MUST be an integer.'''
    try:
        i = int(''.join([ch for ch in i if ch.isdigit()]))
        with open(FILE, 'r') as f:
            todos = [todo for todo in f.readlines() if todo.strip()]
        to_be_removed = todos[i]
        del todos[i]
        with open(FILE, 'w') as f:
            for todo in todos:
                f.write(f'{todo}\n')
        return f'Removed {to_be_removed} from your todo list'
    except Exception as e:
        return f'ERROR: Failed to remove todo because: {e}'


@tool(return_direct=False)
def get_todos(*args, **kwargs) -> str:
    '''Get all TODO items'''
    with open(FILE, 'r') as f:
        todos = '\n'.join([
            f'{i + 1}. {line.strip()}\n'
            for i, line in enumerate(
                [l for l in f.readlines() if l.split()]
            )
        ])
    return todos


todo_tool = [
    make_todo,
    remove_todo,
    get_todos,
]
