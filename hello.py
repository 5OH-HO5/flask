# 요청이 들어오면 return해준다
# 플라스크 모듈 안에서 import 3개 불러오기
from flask import Flask, escape, request, render_template
import random
from bs4 import BeautifulSoup
import requests
# 플라스크를 app이라는 변수에 저장
app = Flask(__name__)
# 밑에 있는 함수가 시작되기 전에 시작되는 부분
# /라는 요청이 들어오면 밑에있는 hello함수를 실행시키겠다
@app.route('/')
# /라는 것은 127.0.0.1:5000이 숨겨져 있다
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/hi')
# 127.0.0.1:5000/hi
def hi():
    return 'hi'

@app.route('/oh')
# 127.0.0.1:5000/oh
def oh():
    return 'ohminjae'

@app.route('/html_tag')
def html_tag():
    return '<h1>안녕하세요</h1>'

@app.route('/html_file')
def html_file():
    return render_template('index.html')

# render 만들다/되게 하다/세우다
@app.route('/variable')
def variable():
    name = '오민재'
    return render_template('variable.html', html_name = name)

# 동적 routing
@app.route('/greeting/<string:name>/')
def greeting(name):
    def_name = name
    return render_template('greeting.html', html_name = def_name)

# /cube/3
# 3의 3제곱은 27입니다.
@app.route('/cube/<int:number>/')
def cube(number):
    def_number = number
    return render_template('cube.html', html_number = def_number)
    # cube.html을 리턴해주는게 render_template의 역할
    # ** 지수를 표현 // 3의 4제곱 = 3 ** 4

@app.route('/cube1/<int:num>/')
def cube1(num):
    num = num
    cube_num = num ** 3
    return render_template('cube1.html', num = num, cube_num = cube_num)

# random으로 lunch menu choice하기
@app.route('/lunch')
def lunch():
    list_menu = ['짜장면','짬뽕','탕수육']

# random.choice
# random library import해주기

# {중괄호 dictionary 형태로 가능}
# menus = {
#   '짜장': '이미지 주소',
#   '짜장': '이미지 주소',
#   '짜장': '이미지 주소'}
# menu_list = menus.keys()
# print(menu_list)

# choice 안에 list는 string 형태 아님
    pick = random.choice(list_menu)
    return render_template('lunch.html', pick = pick)

@app.route('/movies')
def movies():
    movies = ['겨울왕국2','쥬만지','해리포터']
    return render_template('movies.html', movies = movies)

@app.route('/ping')
def ping():
    return render_template('ping.html')

@app.route('/pong', methods = ['GET','POST'])
def pong():
    # request.args => GET 형식으로 데이터가 들어온다면 사용
    # request.form => POST 형식으로 데이터가 들어온다면 사용
    # print(request.form.get('keyword'))
    keyword = request.form.get('keyword')
    return render_template('pong.html', keyword = keyword)

@app.route('/naver')
def naver():
    return render_template('naver.html')

@app.route('/google')
def google():
    return render_template('google.html')

@app.route('/summoner')
def summoner():
    return render_template('summoner.html')

@app.route('/opgg')
def opgg():
    # args.get('asdf') = keyerror 에러를 반영
    # args.get['asdf'] = None 값을 반영
    # args.get('asdf', '잘못된 접근입니다.') = 잘못된 정보면 잘못된 접근이라는 디폴트값 반영가능
    username = request.args.get('username')
    opgg_url = f"https://www.op.gg/summoner/userName={username}"

    response = requests.get(opgg_url).text
    soup = BeautifulSoup(response, 'html.parser')
    tier = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierRank').text
    win = soup.select_one('#SummonerLayoutContent > div.tabItem.Content.SummonerLayoutContent.summonerLayout-summary > div.SideContent > div.TierBox.Box > div > div.TierRankInfo > div.TierInfo > span.WinLose > span.wins')
    return render_template('opgg.html', username = username, opgg_url = opgg_url, tier = tier, win = win.text.replace('W',''))

@app.route('/real_time_search')
def real_time_search():
    url = 'https://www.naver.com/'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    rank_list = []
    for i in range(1, 21):
        rank = soup.select_one(f'#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li:nth-child({i}) > a > span.ah_k').text
        rank_list.append(rank)
    random.shuffle(rank_list)
    return render_template('real_time_search.html', rank_list = rank_list)


@app.route('/result')
def result():
    popkeyword = request.args.get('popkeyword')
    url = 'https://www.naver.com/'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')
    rank_a = soup.select_one('#PM_ID_ct > div.header > div.section_navbar > div.area_hotkeyword.PM_CL_realtimeKeyword_base > div.ah_roll.PM_CL_realtimeKeyword_rolling_base > div > ul > li:nth-child(1) > a > span.ah_k').text
    return render_template('result.html', popkeyword = popkeyword, rank_a = rank_a)


if __name__ == '__main__':
    app.run(debug=True)