import os
import requests

# URL 목록 파일 경로
file_path = r"C:/Users/ahnjh/Documents/GitHub/CAU_GG_Back/crawling/Cleaned_LoL_Champions.txt"
# 이미지를 저장할 폴더 경로
save_folder = r"C:/Users/ahnjh/Documents/GitHub/CAU_GG_Back/crawling/asdf"


# URL에서 이미지 다운로드 함수
def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)  # 스트리밍 모드로 요청
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(1024):  # 1KB씩 다운로드
                file.write(chunk)
    except Exception as e:
        print(url)

# URL 목록 읽기
with open(file_path, "r", encoding="utf-8") as file:
    names = file.readlines()

for name in names:
    name = name.strip()
    url = "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_0.jpg".format(name)
    file_name = "{}.jpg".format(name)  # 저장할 파일 이름
    save_path = os.path.join(save_folder, file_name)  # 저장 경로
    download_image(url, save_path)

print(len(names))