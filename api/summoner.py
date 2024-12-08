from bs4 import BeautifulSoup
import requests, json

# getMasteryList = 
def getMasteryList(fullname):
    fullname = fullname.replace('#','-')
    url = f'https://www.op.gg/summoners/kr/{fullname}/mastery'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    sel = "#content-container > div.box--desktop.dashboard--loading.css-7ruavw.erdn3wx2"
    soup = str(soup.select(sel))

    champ_list = soup.split('<strong class="champion-name">')[1:]
    mastery_list = soup.split('<div class="champion-point">')[1:]
    
    temp_list = []

    for i in range(0, len(champ_list)):
        temp_dict = {}
        temp_dict['rank'] = i+1
        temp_dict['champion'] = champ_list[i].split('<')[0]
        temp_dict['mastery'] = mastery_list[i].split('<')[1][5:]

        temp_list.append(temp_dict)

    return temp_list

def getSummonerInfo(fullname):
    fullname = fullname.replace('#','-')
    url = f'https://www.op.gg/summoners/kr/{fullname}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup = soup.text
    
    temp_list = []

    for i in range(0, 1):
        temp_dict = {}
        temp_dict['user name'] = fullname
        temp_dict['level'] = soup.split('My Page')[1].split(fullname.split('-')[0])[0]
        # temp_dict['ladder'] = soup.split('\n')[1].replace(' ','')

        tier_solo = soup.split('Ranked Solo/Duo')[1]
        tier_flex = soup.split('Ranked Flex')[2]
        
        if 'Unranked' == tier_solo[:8]: tier_solo = 'Unranked'
        else: 
            t = tier_solo.split('LP')[0].strip(' ')
            tier_solo = t[:-2]+' - '+t[-2:]+'LP'
        if 'Unranked' == tier_flex[:8]: tier_flex = 'Unranked'
        else: 
            t = tier_flex.split('LP')[0].strip(' ')
            tier_flex = t[:-2]+' - '+t[-2:]+'LP'

        temp_dict['solo'] = tier_solo
        temp_dict['flex'] = tier_flex

        champ_list = []
        for l in soup.split('Ranked Flex')[-1].split('Played')[:-4]:
            champ_dict = {}
            champ_dict['name'] = l.split('CS')[0]
            champ_dict['games'] = l.split('%')[-1]+'games'
            champ_dict['kda'] = l.split(')')[1].split('KDA')[0]
            champ_dict['win rate'] = l.split('.')[-1][1:].split('%')[0]+'%'

            champ_list.append(champ_dict)

        temp_dict['season_most'] = champ_list

        temp_list.append(temp_dict)

    return temp_list

def summonersForEmail(email):
    with open('api/userDB.json', 'r') as f:
        all_users = json.load(f)
    name = all_users[email]['nickname']
    print(name)
    name = name.replace('-','#')
    info = getSummonerInfo(fullname = name)
    with open(f'api/user/{name}.json', 'w') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)