
import pandas as pd
import gensim
import pymysql
import random

import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO)

ko_model = gensim.models.Word2Vec.load('ko.bin')
su_model = gensim.models.Word2Vec.load('model.h5')



db = pymysql.connect(host='호스트명_aws주소', \
                     user='root', password='비밀번호', db='db명')


def calculation_similarity(s1,s2):

    try:
        b = ko_model.wv.similarity(s1,s2)
    except KeyError:
        b=0

    return b


#책 데이터(이미지, 제목, 작가, 출판사, 키워드) 불러오기




def call_book(kwd):
    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "select * from book"
        cursor.execute(sql)
        #cursor.execute(sql,(kwd,kwd,kwd,kwd,kwd,kwd))
        result = cursor.fetchall()


        data = pd.DataFrame(result)


        #책 정보 dataframe
        book = data.loc[:,['image','NAME','Actor','channel']]
        #book = data.loc[:,['a','b','c','d']]
        #키워드 정보 dataframe
        word = data.loc[:,['keyword1','keyword2','keyword3','keyword4','keyword5','keyword6']]

        #word = data.loc[:,['f']]
        #키워드 부분만 사용
        #print(word)

        word = word.dropna()
        #모든 데이터가 NaN인 행은 다 지워라
        #print(word)

        a=ko_model.wv.most_similar(kwd) #오픈소스 사용
        a2=su_model.wv.most_similar(kwd)#내 모델 사용

        index_group=[]   #키워드 맞는 행의 index를 저장하기 위한 그룹

        #1.키워드를 갖고 있는 책을 추출
        temp = word.loc[(word.keyword1==kwd) | (word.keyword2==kwd) | (word.keyword3==kwd) | (word.keyword4==kwd) | (word.keyword5==kwd) | (word.keyword6==kwd), :]

        for i, v in zip(temp.index.values, temp):
            index_group.append(i)

        print("in try index ", index_group)
        #2.유사 키워드를 갖고 있는 행만 가져오기
        #print(word.loc[(word.e=='가족') | (word.f=='가족') | (word.g=='가족') | (word.h=='가족') | (word.i=='가족') | (word.j=='가족'), :])
        for k in range(len(a)):
            temporary =  word.loc[(word.keyword1==a[k][0]) | (word.keyword2==a[k][0]) | (word.keyword3==a[k][0]) | (word.keyword4==a[k][0]) | (word.keyword5==a[k][0]) | (word.keyword6==a[k][0]), :]
            #temporary = split.loc[(str(split[0])==a[k][0])| (str(split[1])==a[k][0]) | (str(split[2])==a[k][0]) | (str(split[3])==a[k][0]) | (str(split[4])==a[k][0])]
            #print(temporary)
            for i, v in zip(temporary.index.values, temporary):
               index_group.append(i)
            #행 번호 저장
        print("ko in try index ", index_group)
        for k in range(len(a2)):
            temporary =  word.loc[(word.keyword1==a2[k][0]) | (word.keyword2==a2[k][0]) | (word.keyword3==a2[k][0]) | (word.keyword4==a2[k][0]) | (word.keyword5==a2[k][0]) | (word.keyword6==a2[k][0]), :]
            #temporary = split.loc[(str(split[0])==a[k][0])| (str(split[1])==a[k][0]) | (str(split[2])==a[k][0]) | (str(split[3])==a[k][0]) | (str(split[4])==a[k][0])]
            #print(temporary)
            for i, v in zip(temporary.index.values, temporary):
               index_group.append(i)
            #행 번호 저장
        print("subin in try index ", index_group)
        similar_sum={}   #key:index value:Sum
        for i in range(len(index_group)):
            Sum=0  #각 키워드와 유사 단어 사이의 유사도 값을
            for j in range(len(a)):
                Sum+=calculation_similarity(word.loc[index_group[i]].keyword1,a[j][0])
                Sum+=calculation_similarity(word.loc[index_group[i]].keyword2,a[j][0])
                Sum+=calculation_similarity(word.loc[index_group[i]].keyword3,a[j][0])
                Sum+=calculation_similarity(word.loc[index_group[i]].keyword4,a[j][0])
                Sum+=calculation_similarity(word.loc[index_group[i]].keyword5,a[j][0])
                Sum+=calculation_similarity(word.loc[index_group[i]].keyword6,a[j][0])
            similar_sum[index_group[i]]=Sum  #키워드 6 * 유사 단어 10개 (60번 연산)

        #print(similar_sum)
        res = sorted(similar_sum.items(), key=(lambda x: x[1]), reverse = True)  #value값이 큰 기준으로 정렬
        #print(res)
        key_list=[]
        for i in range(len(res)):
            key_list.append(res[i][0])

        if not index_group:
            lists="검색 결과가 없습니다. 다른 검색어를 입력해주세요.<br>"   #키워드가 일치하는 게 아예 없는 경우
        else:
            #print("---------------")
            lists = ""
            lists = "<br><table><tr bgcolor='#D3D3D3' align='center'><td></td><td>제목</td><td>작가</td><td>출판사</td><td>더보기</td></tr>"
            for i in key_list:
                #print(book.iloc[i][3])
                lists += "<tr><td>"+"<img src="+book.iloc[i][0]+"></img></td><td>"+book.iloc[i][1]+"</td><td>"+book.iloc[i][2]+"</td><td>"+book.iloc[i][3]+"</td><td><a href='https://book.naver.com/search/search.nhn?sm=sta_hty.book&sug=&where=nexearch&query="+book.iloc[i][1]+"' target='_blank'><img src=\"/static/more.jpg\"></a></td></tr>"
            lists += "</table>"

        return lists
    except KeyError:
        index_group=[]   #키워드 맞는 행의 index를 저장하기 위한 그룹

            #1.키워드를 갖고 있는 책을 추출
        temp = word.loc[(word.keyword1==kwd) | (word.keyword2==kwd) | (word.keyword3==kwd) | (word.keyword4==kwd) | (word.keyword5==kwd) | (word.keyword6==kwd), :]

        for i, v in zip(temp.index.values, temp):
            index_group.append(i)
        print("except index " , index_group)
        print("except length" , len(index_group))

        if len(index_group) == 0:
            return "검색 결과가 없습니다. 다른 검색어를 입력해주세요.<br>"   #키워드가 일치하는 게 아예 없는 경우
        else:
            #print("---------------")
            lists = ""
            lists = "<br><table><tr bgcolor='#D3D3D3' align='center'><td width='30%'></td><td width='30%'>제목</td><td width='20%'>작가</td><td width='20%'>출판사</td><td width='8%'>더보기</td></tr>"
            for i in index_group:
                #print(book.iloc[i][3])
                lists += "<tr><td>"+"<img src="+book.iloc[i][0]+"></img></td><td>"+book.iloc[i][1]+"</td><td>"+book.iloc[i][2]+"</td><td>"+book.iloc[i][3]+"</td><td><a href='https://book.naver.com/search/search.nhn?sm=sta_hty.book&sug=&where=nexearch&query="+book.iloc[i][1]+"' target='_blank'><img src=\"/static/more.jpg\"></a></td></tr>"
            lists += "</table>"
            return lists


def call_movie(kwd):
    try:
        a=ko_model.wv.most_similar(kwd) #오픈소스 사용
        #a2=su_model.wv.most_similar(kwd)#내 모델 사용

        #index_group=[]   #키워드 맞는 행의 index를 저장하기 위한 그룹

        cursor = db.cursor(pymysql.cursors.DictCursor)

        sql = "select image, NAME, Actor, rating from newmovie where keyword like %s OR jenre like %s"
        cursor.execute(sql,('%'+kwd+'%','%'+kwd+'%'))
        #cursor.execute(sql,(kwd,kwd,kwd,kwd,kwd,kwd))
        result = cursor.fetchall()
        cnt_num = len(result)
        result = list(result)

        print("영화 : 해당 키워드 개수 -> ", cnt_num)

        '''
        if cnt_num < 5 :
            for i in range(len(a)):
                sql = "select image, NAME, Actor, rating from newmovie where keyword like %s OR jenre like %s"
                cursor.execute(sql,('%'+a[i][0]+'%','%'+a[i][0]+'%'))
                #cursor.execute(sql,(kwd,kwd,kwd,kwd,kwd,kwd))
                result_ko = cursor.fetchall()
                result += list(result_ko)
                #data += pd.DataFrame(result)
        '''


        #print(result)
        if not result:
            lists="검색 결과가 없습니다. 다른 검색어를 입력해주세요.<br>"   #키워드가 일치하는 게 아예 없는 경우
        else:
            #print("---------------")
            lists = ""
            lists = "<br><table><tr bgcolor='#D3D3D3' align='center'><td width='10%'></td><td width='10%'>제목</td><td width='10%'>출연진</td><td width='8%'>평점</td><td width='8%'>더보기</td></tr>"
            #print(result[0]['image'])

            rnd_num = []

            if len(result) < 5 :
                rnd_num = random.sample(range(0, len(result)), len(result))
            else :
                rnd_num = random.sample(range(0, len(result)), 5)
            for i in rnd_num:
                lists += "<tr><td>"+"<img src="+result[i]['image']+"></img></td><td>"+result[i]['NAME']+"</td><td>"+result[i]['Actor']+"</td><td>"+result[i]['rating']+"</td><td><a href='https://movie.naver.com/movie/search/result.nhn?query="+result[i]['NAME']+"&section=all&ie=utf8' target='_blank'><img src=\"/static/more.jpg\"></a></td></tr>"
            lists += "</table>"
        #print(lists)
        return lists
    except KeyError:
        return "검색 결과가 없습니다. 다른 검색어를 입력해주세요.<br>"




def call_drama(kwd):
    try:
        a=ko_model.wv.most_similar(kwd) #오픈소스 사용
        #a2=su_model.wv.most_similar(kwd)#내 모델 사용

        #index_group=[]   #키워드 맞는 행의 index를 저장하기 위한 그룹

        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = "select image, NAME, CHANNEL, actor from newdrama where keyword like %s"
        cursor.execute(sql,'%'+kwd+'%')
        #cursor.execute(sql,(kwd,kwd,kwd,kwd,kwd,kwd))
        result1 = cursor.fetchall()
        cnt_num = len(result1)
        result = list(result1)
        print("드라마 : 해당 키워드 개수 -> ", cnt_num)
        '''
        if cnt_num < 5:
            for i in range(len(a)):
                sql = "select image, NAME, CHANNEL, actor from newdrama where keyword like %s"
                cursor.execute(sql,'%'+a[i][0]+'%')
                #cursor.execute(sql,(kwd,kwd,kwd,kwd,kwd,kwd))
                result2 = cursor.fetchall()
                result+=list(result2)
        '''
        #print(result)
        if not result:
            lists="검색 결과가 없습니다. 다른 검색어를 입력해주세요.<br>"   #키워드가 일치하는 게 아예 없는 경우
        else:
            #print("---------------")
            lists = ""
            lists = "<br><table><tr bgcolor='#D3D3D3' align='center'><td></td><td>제목</td><td>방송사</td><td>배우</td><td>더보기</td></tr>"
            #print(result[0]['image'])

            rnd_num = []
            if len(result) < 5:
                rnd_num = random.sample(range(0, len(result)), len(result))
            else :
                rnd_num = random.sample(range(0, len(result)),5)
            for i in rnd_num:
            #print(book.iloc[i][3])
                lists += "<tr><td>"+"<img src="+result[i]['image']+"></img></td><td>"+result[i]['NAME']+"</td><td>"+result[i]['CHANNEL']+"</td><td>"+result[i]['actor']+"</td><td><a href='http://www.tving.com/find/main.do?kwd="+result[i]['NAME']+"' target='_blank'><img src=\"/static/more.jpg\"></a></td></tr>"
            lists += "</table>"

        #print(lists)
        return lists
    except KeyError:
        return "검색 결과가 없습니다. 다른 검색어를 입력해주세요.<br>"
