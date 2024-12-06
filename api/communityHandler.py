import json
from collections import OrderedDict

postDB = 'api/postDB.json'

def insertUser(nickname, title, content, time):
    try:
        with open(postDB, 'r') as f:
            all_posts = json.load(f)
    except json.JSONDecodeError:
        # 파일이 비어 있거나 손상된 경우 초기화
        all_posts = {}

    all_posts[f'{len(all_posts)}'] = ({'title': title, 'nickname': nickname, 'content': content, 'time': time})
    
    with open(postDB, 'w') as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=4)
        
    return True

def getPostList():
    try:
        with open(postDB, 'r') as f:
            all_posts = json.load(f)
    except json.JSONDecodeError:
        # 파일이 비어 있거나 손상된 경우 초기화
        all_posts = {}
        
    return all_posts