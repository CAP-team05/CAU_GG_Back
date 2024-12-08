import json
from collections import OrderedDict

userDB = 'api/userDB.json'
    
def insertUser(email, password, nickname, major, verified):
    try:
        with open(userDB, 'r') as f:
            all_users = json.load(f)
    except json.JSONDecodeError:
        # 파일이 비어 있거나 손상된 경우 초기화
        all_users = {}
        
    if (email in all_users):
        return

    all_users[email] = {
        'password': password,
        'nickname': nickname,
        'major': major,
        'verified': verified
    }
    
    with open(userDB, 'w') as f:
        json.dump(all_users, f, ensure_ascii=False, indent=4)
        
def checkVerify(email):
    try:
        with open(userDB, 'r') as f:
            all_users = json.load(f)
    except json.JSONDecodeError:
        # 파일이 비어 있거나 손상된 경우 초기화
        all_users = {}
        
    if (email in all_users):
        return all_users[email]['verified']
    else:
        return False
        
def verifyUser(email):
    try:
        with open(userDB, 'r') as f:
            all_users = json.load(f)
    except json.JSONDecodeError:
        # 파일이 비어 있거나 손상된 경우 초기화
        all_users = {}
        
    if (email in all_users):
        all_users[email]['verified'] = True
        with open(userDB, 'w') as f:
            json.dump(all_users, f, ensure_ascii=False, indent=4)
            
def checkUser(email, password):
    try:
        with open(userDB, 'r') as f:
            all_users = json.load(f)
    except json.JSONDecodeError:
        all_users = {}
    
    if (email in all_users):
        print(f"email ${email}")
        if(all_users[email]['verified'] == False):
            return False
        if(all_users[email]['password'] == password):
            return all_users[email]['nickname']

def getNickname(email):
    try:
        with open(userDB, 'r') as f:
            all_users = json.load(f)
    except json.JSONDecodeError:
        all_users = {}
    
    if (email in all_users):
        return all_users[email]['nickname']
    else:
        return None