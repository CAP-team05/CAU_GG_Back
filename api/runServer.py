from flask import Flask, jsonify, render_template
import json

import tier, summoner

app = Flask(__name__)

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

# 소환사 계정 정보
@app.route('/summoner/<name>')
def summoners(name):
    info = summoner.getSummonerInfo(fullname = name)
    return app.response_class(
        response=json.dumps(info, ensure_ascii = False, indent=4),
        mimetype='application/json'
    )

# 소환사 숙련도 정보
@app.route('/mastery/<name>')
def masteries(name):
    info = summoner.getMasteryList(fullname = name)
    return app.response_class(
        response=json.dumps(info, ensure_ascii = False, indent=4),
        mimetype='application/json'
    )


# app 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2222)
