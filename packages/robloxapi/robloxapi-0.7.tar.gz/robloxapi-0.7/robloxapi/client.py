from .src.request import client_Request
from .src.User import User
def client(cookie=str()):
    global functions
    if cookie:
        cookies = {
            '.ROBLOSECURITY': cookie
        }
        r = client_Request('https://www.roblox.com/game/GetCurrentUser.ashx', parse=False, cookies=cookies)
        if r is 'null':
            print('Rython: Failed to login. Using Rython without login')
            functions = lambda: None
            functions.User = User()
            return functions
        else:   
            functions = lambda: None
            functions.User = User(cookie, r)
            return functions
    else:
        functions = lambda: None
        functions.User = User()
        return functions

        #Check cookie
   

