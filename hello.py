# 요청이 들어오면 return해준다
# 플라스크 모듈 안에서 import 3개 불러오기
from flask import Flask, escape, request, render_template
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

@app.route(/html_tag)
def html_tag():
    return '<h1>안녕하세요</h1>'

@app.route(html_file)
def html_file():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)