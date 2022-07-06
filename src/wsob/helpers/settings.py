from random import randint

def get_user_agent() -> str:
    " Return a random User-Agent from user-agents.txt file to use in request "

    file_path: str = "src/wsob/helpers/user-agents.txt"
    
    with open(file_path) as content:
        user_agent: str = content.readlines()
        user_agent: str = user_agent[randint(0, len(user_agent) -1)]
        user_agent: str = user_agent.encode('utf-8')

        return str(user_agent)

headers = {
    'User-Agent': get_user_agent(),
    'Connection': 'keep-alive'
}

props = {
    'verify': False,
    'headers': headers,
    'allow_redirects': True
}