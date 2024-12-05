import os
from PIL import Image

def convert_and_rename_jpg_to_png(folder_path):
    # 폴더 내 파일 목록 가져오기
    files = os.listdir(folder_path)
    
    for file in files:
        # 파일 확장자가 jpg인 경우만 처리
        if file.lower().endswith('.jpg'):
            # 소문자로 파일 이름 변경
            old_path = os.path.join(folder_path, file)
            lowercase_file = file.lower()
            lowercase_path = os.path.join(folder_path, lowercase_file)
            
            # 파일 이름 변경
            if old_path != lowercase_path:
                os.rename(old_path, lowercase_path)
            
            # JPG -> PNG 변환
            png_path = os.path.splitext(lowercase_path)[0] + '.png'
            
            try:
                with Image.open(lowercase_path) as img:
                    img.save(png_path, 'PNG')
            except Exception as e:
                print(f"변환 실패: {lowercase_path}, 에러: {e}")

# 실행 예시
folder_path = "C:/Users/ahnjh/Documents/GitHub/CAU_GG_Back/crawling/championBGs"
convert_and_rename_jpg_to_png(folder_path)
