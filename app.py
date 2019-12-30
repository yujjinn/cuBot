
from flask import Flask, render_template, request
import word2vec_model
import random


app = Flask(__name__)


random_keyword = ['마약', '고민', '시인', '추리', '디지털', '나무', '도박', '위안부', '야구', '성경', '죄수', '자신', '뉴욕', '거미', '환상', '희생', '출산', \
'남편', '수술', '서울', '클래식', '러시아', '아픔', '창업', '그림', '운명', '배신', '페미니스트', '베트남', '선물', '웃음', '편지', '아들', '인형',  '보석', \
'기억', '자연', '천사', '잘못', '카페', '외계인', '어른', '축구', '종교', '달팽이', '호주', '동네', '자매', '만남', '라이프', '노력', '소동', '가족', '오페라',\
'할아버지', '뮤지컬', '아침', '여성', '음악', '낙원', '유령',  '판타지', '생각', '파리', '영재', '영국', '진심', '여우', '화가', '공부', '댄스', '슬픔',  '음식', \
'위로', '연애', '눈물', '악마', '영혼', '모험', '여인', '아빠', '치유', '비극', '수업', '독일', '이별', '성공', '가문', '일상', '드라마', '청소년', '재능', '국가', \
'사회', '결혼', '긍정', '미국', '목표', '무기', '왕국', '생존',  '중국', '발명', '야망', '풍자', '첫사랑', '파라오', '캐릭터', '군인', '네트워크', '범죄', '교사', \
'취재', '런던', '시민', '생명', '일기장', '믿음', '만화', '귀족', '죽음', '상처', '의식', '황제',  '요리', '재회', '기독교', '감정', '이민', '엄마', '덴마크', '경찰',\
'행복', '지구', '과학', '세태', '인생', '의사', '열정', '커플', '공포', '리더', '회사원', '아일랜드', '원망',  '직장',  '감동', '질투', '형사', '왕자', '학살', '추억',\
'마법', '대화', '우주', '감시', '몰입', '고독', '바보', '육아', '노동', '일기', '욕망', '세대', '교도소',  '도시', '호텔', '예수', '희망', '로맨스', '스릴러', '부모',\
'지도', '비밀',  '토끼', '게임', '걸작', '사막', '사랑', '동물', '분노', '부자', '응원', '웹툰', '강의', '스님', '미션', '소원', '부부',  '집사',  '캐나다',  '마녀',\
'천재', '애니메이션', '이슈', '심연', '도전', '현실',  '고양이',  '수사', '새벽', '전쟁', '할머니', '회사', '펭귄', '괴물', '조선', '실험',  '가상현실', '소녀', \
'말리', '페이스', '재즈',  '부활', '리듬',  '노인', '남매', '꼬마', '프랑스', '아기', '연인', '청춘',  '역사', '협상', '수수께끼', '방황', '여행', '뱀파이어','유럽','신부', '친구']



@app.route("/")
def home():
    return render_template("front_page.html")

##2019.08.25 랜덤 함수 적용 해결
##영어 입력시 소문자 대문자 상관없이 출력




### 드라마
@app.route("/drama")
def get_drama_response():
    #사용자 입력 값
    userText = request.args.get('msg')
    userText = str(userText)
    print ("DRAMA user Text : ", userText)
    return word2vec_model.call_drama(userText)




### 영화
@app.route("/movie")
def get_movie_response():
    #사용자 입력 값
    userText = request.args.get('msg')

    print ("MOVIE user Text : ", userText)

    return word2vec_model.call_movie(userText)




### 책
@app.route("/book")
def get_book_response():
    #사용자 입력 값

    userText = request.args.get('msg')
    userText = str(userText)
    print ("BOOK user Text : ", userText)
    
    return word2vec_model.call_book(userText)




# 추천 키워드 버튼 생성
@app.route("/process")
def view_do_something():
    print("get in process")

    num = request.args.get('num')
    print("num " , num)

    random_num = []
    random_num = random.sample(range(0, len(random_keyword)), 3)
    return_button = '<hr>'
    Rcnt = 0
    for a in random_num :
        Rcnt+=1
        return_button += '<button id ="'+num+'rcm_genre'+str(Rcnt)+'" onclick="get_inform(\''+random_keyword[a]+'\');">'+random_keyword[a]+'</button>&nbsp;&nbsp;'

    return_button += '<br><br><button id ="rcm_keyword" onclick="rcm_f5()">새 키워드</button>&nbsp;<button id ="back_to_first" onclick="go_back()">돌아가기</button><br><hr><br>'
    return return_button



# 키워드 추천 새로고침(새 키워드 갖고 오기)
@app.route("/rcmF5", methods=['post'])
def recommend_f5():
    print("get in process")
    if request.method == 'POST':
        #your database process here
        print("POST")
    else:
        print("GET")

    random_num = []
    random_num = random.sample(range(0, len(random_keyword)), 3)
    return_keyword = ""
    for i in random_num :
        return_keyword+=(random_keyword[i]+",")

    return return_keyword




if __name__ == "__main__":
    app.run()
