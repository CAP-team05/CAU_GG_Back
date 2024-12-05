import os, json
import shutil

def copy_and_change_extension(folder_path, target_folder, new_name_format):
    try:
        # 대상 폴더가 존재하지 않으면 생성
        os.makedirs(target_folder, exist_ok=True)
        
        # 폴더 내 모든 파일 가져오기
        files = os.listdir(folder_path)
        
        # 파일 복사 및 확장자 변경
        for index, file_name in enumerate(files):
            old_file_path = os.path.join(folder_path, file_name)
            
            # 파일인지 확인
            if os.path.isfile(old_file_path):
                # 확장자 확인
                file_extension = os.path.splitext(file_name)[1]
                
                # .jpg 파일만 처리
                if file_extension.lower() == ".jpg":
                    # 새 파일 이름 지정
                    new_file_name = new_name_format.format(index=index) + ".png"
                    new_file_path = os.path.join(target_folder, new_file_name)
                    
                    # 파일 복사
                    os.rename(old_file_path, new_file_path)
        
        print("모든 파일 복사 및 확장자 변경 완료!")
    
    except Exception as e:
        print(f"오류 발생: {e}")



# 대상 폴더 경로
folder_path = "C:\\Users\\ahnjh\\Documents\\GitHub\\CAU_GG_Back\\crawling\\championIcons"

with open("C:\\Users\\ahnjh\\Documents\\GitHub\\CAU_GG_Back\\input.json", 'r', encoding='utf-8') as file:
    names = json.load(file)
                         
# 결과 저장 리스트
result = []

# 폴더 내 모든 파일 처리

tempList = []
for file_name in os.listdir(folder_path):
    kor_name = file_name.split("/")[-1]
    kor_name = kor_name.split(".")[0]
    
    for name in names:
        if name["korean_name"] == kor_name:
            eng_name = name["english_name"]
            eng_name = eng_name.replace("'", "")
            eng_name = eng_name.replace(" ", "")
            eng_name = eng_name.replace(".", "")
            eng_name = eng_name.strip(" ")
            eng_name = eng_name.lower()

    new_file_name = eng_name
    target_folder = "C:\\Users\\ahnjh\\Documents\\GitHub\\CAU_GG_Back\\crawling"

    copy_and_change_extension(folder_path, folder_path, new_file_name)

        
