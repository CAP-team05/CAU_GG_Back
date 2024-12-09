# CAU_GG backend manual

1. 프로젝트 다운로드
```bash
git clone <현재 주소 레포>
cd CAU_GG_BACK
code . 혹은 이 디렉토리 열기
```
2. api/config.py 설정

> config.py의 경우 stml 메일 서비스 옵션들을 넣어주면 된다.
코드예시

```python
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'cauggteam@gmail.com'
MAIL_PASSWORD = '****************'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'cauggteam@gmail.com'
```
google 계정 2차 인증 후 mail server의 비밀번호 생성 가능

3. api/runServer.py 내 라이브러리 설치
```bash
pip install flask....., ect.
```

4. api/runServer.py 실행


