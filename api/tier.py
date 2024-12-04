from bs4 import BeautifulSoup
import requests, json

# sortAlpha = line 에서 숫자를 제거하는 함수
# line: string -> name: string
def sortAlpha(line):
    n = [str(num) for num in line if num.isalpha()]
    name = str(''.join(map(str, n)))
    return name

# getTierList = 포지션 별 티어 리스트 크롤링 (from OPGG)
# position: string -> champ_list: list (of dictionarys)
def getTierList(position):
    url = 'https://www.op.gg/champions?position='+position
    # print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup = soup.text.split('against')[1].split('ADVERTISEMENTREMOVE')[0]

    soup = soup.split('%')

    champ_list = []
    
    for i in range(0, len(soup)//3):
        temp_dict = {}
        temp_dict['rank'] = int(i)+1
        i = i*3
        temp_dict['name'] = sortAlpha(soup[i])
        temp_dict['win'] = round(float(soup[i][-6:])%100, 2)
        temp_dict['pick'] = round(float(soup[i+1]), 2)
        temp_dict['ban'] = round(float(soup[i+2]), 2)

        champ_list.append(temp_dict)

    return champ_list

# 포지션 별 티어 json 파일 만드는 함수, 잦은 변동으로 해당 기능 사용 안할 예정
'''
def makeTierFiles():
    for pos in ['all', 'top', 'jungle', 'mid', 'adc', 'support']:
        file_name = 'tiers/'+pos+'.json'
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(getTierList(pos), f, ensure_ascii = False, indent=4)
    print("All file has created successfully!")
'''