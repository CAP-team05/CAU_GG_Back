from flask import Flask, jsonify, render_template, request, Response, send_from_directory
from flask_mail import Mail, Message
from flask_cors import CORS
import json
import tier, summoner
import config as config
from functools import wraps
import userHandler as userHandler
import rankingHandler as rankingHandler
import communityHandler as cH
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
mail = Mail(app)
CORS(app)

# Flask-Mail 설정
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER

# utf8 json response 만들 때 사용
def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function

# 홈 페이지
@app.route('/')
def main():
    return "CAU.GG"

# 게임 티어 정보
@app.route('/tier/<pos>')
def tiers(pos):
    info = tier.getTierList(position= pos)
    return app.response_class(
        response=json.dumps(info, ensure_ascii = False, indent=4),
        mimetype='application/json'
    )

# 소환사 계정 정보 태그는 #말고 - 사용
@app.route('/summoner/<name>')
def summoners(name):
    name = name.replace('-','#')
    info = summoner.getSummonerInfo(fullname = name)
    with open(f'api/user/{name}.json', 'w') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    return app.response_class(
        response=json.dumps(info, ensure_ascii = False, indent=4),
        mimetype='application/json'
    )


@app.route('/mastery/<name>')
def masteries(name):
    # 소환사 숙련도 정보 가져오기
    info = summoner.getMasteryList(fullname=name)

    # JSON 파일 경로 설정
    file_path = f'api/user/{name.replace("-", "#")}.json'

    # 파일 생성 또는 업데이트
    if os.path.exists(file_path):
        # 기존 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                # 파일이 비어있거나 JSON 형식이 잘못된 경우
                existing_data = []
    else:
        # 파일이 없으면 빈 리스트로 초기화
        existing_data = []

    # "mastery" 데이터 추가
    if isinstance(existing_data, list) and len(existing_data) > 0:
        # 리스트의 마지막 항목에 "mastery" 추가
        existing_data[-1]["mastery"] = info if isinstance(info, list) else []
    else:
        # 데이터가 예상한 형식이 아니거나 비어있는 경우
        existing_data = [{"mastery": info if isinstance(info, list) else []}]

    # 업데이트된 데이터를 파일에 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    # API 응답 반환
    return app.response_class(
        response=json.dumps(existing_data, ensure_ascii=False, indent=4),
        mimetype='application/json'
    )

# 챔피언 이미지 불러오기 (개발 중)
@app.route('/champion/<name>', methods=['GET'])
def champion_image(name):
    # print('championBGs/{}.png'.format('Azir'))
    return send_from_directory('static', f'championBGs/{name}.png')


@app.route('/register', methods=['POST'])
@as_json
def register():
    data = request.json
    email = data['email']
    password = data['password']
    nickname = data['nickname']
    major = data['major']
    print(data)
    userHandler.insertUser(email, password, nickname, major, False)
    summoner.summonersForEmail(email)

    try:
        verification_link = f"http://127.0.0.1:8080/verify?email={email}"
        print(verification_link)
        send_verification_email(email, verification_link)
        return {"message": "User registered successfully. Verification email sent", "nickname": nickname}
    except Exception as e:
        return {"error": str(e)}
    
def send_verification_email(recipient_email, verification_link):
    """인증 이메일 전송 함수"""
    try:
        _html = f"""\
                    <html>
                    <body>
                        <p>안녕하세요,<br>
                        아래 링크를 클릭하여 이메일 인증을 완료해 주세요:<br>
                        <a href="{verification_link}">{verification_link}</a>
                        </p>
                    </body>
                    </html>
                    """  # HTML 내용
        html = _html.encode('utf-8')
        print(html)
        
        with app.app_context():  # Flask-Mail은 앱 컨텍스트가 필요
            msg = Message(
                subject="Cau.gg email Verification",  # 이메일 제목
                recipients=[recipient_email],  # 수신자
                body=f"안녕하세요,\n\n아래 링크를 클릭하여 이메일 인증을 완료해 주세요:\n{verification_link}\n\n감사합니다.",  # 텍스트 내용
                html=html
            )
            mail.send(msg)  # 이메일 전송
            print(f"인증 이메일이 {recipient_email}로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류 발생: {e}")
        
@app.route('/verify', methods=['GET'])
def verify():
    email = request.args.get('email')
    userHandler.verifyUser(email)
    summoner.summonersForEmail(email)
    return {"message": "User verified successfully"}
        
@app.route('/login', methods=['POST'])
@as_json
def login():
    data = request.json
    email = data['email']
    password = data['password']
    
    if userHandler.checkUser(email, password):
        return {"message": "Login successful", "nickname": userHandler.getNickname(email)}
    else:
        return {"message": "Login failed", "nickname": None}


@app.route('/newpost', methods=['POST'])
@as_json
def newpost():
    # raw_data = request.get_data(as_text=True).encode('utf-8').decode('utf-8')
    # data = json.loads(raw_data)
    data = request.json
    nickname = data['nickname']
    title = data['title']
    content = data['content']
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if cH.insertUser(nickname, title, content, timestamp):
        return {"message": "Post created successfully"}
    else:
        return {"message": "Post creation failed"}

@app.route('/postlist', methods=['GET'])
@as_json
def postlist():
    return cH.getPostList()
    
@app.route('/ranking/<major>', methods=['GET'])
@as_json
def ranking(major):
    return rankingHandler.ranking(major)

# app 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
