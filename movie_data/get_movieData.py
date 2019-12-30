from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException
from konlpy.tag import Twitter
from konlpy.tag import Okt
from collections import Counter
from dict import dic
from datetime import datetime


#--------------------------현재 상영 페이지--------------------------#

now = datetime.now()
date = ""
date += str(now.year)

m=""
m+= str(now.month)
if(len(m) < 2 ) :
    m = "0"+m
date += m
date += str(now.day)
print("date " ,date)

url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date='+date


driver =webdriver.Chrome('C:\chromedriver') ## 경로
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
#--------------------------현재 상영 페이지--------------------------#

twitter = Okt()

arr_rank_name = []
arr_rank_img = []
arr_rank_smr = []
arr_rank_words = []
arr_rank_score = []
arr_rank_director = []
arr_rank_actors = []



## 영화 페이지를 들어가서 정보 추출
def get_inform() :


        ## 이름 뽑기
        name = ""
        name = driver.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info > h3 > a').text
        arr_rank_name.append(name)
        print("-----------------------",name,"-----------------------")




        ## 개요 뽑기
        smr_arr=[]
        smr = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[1]/*')
        for i in smr:
            smr_arr.append(i.text)
            #print(i.text)
        arr_rank_smr.append(smr_arr)



        ##평점
        score = ""
        for i in range(1,5):
            get_num = driver.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em['+str(i)+']')
            score += get_num.text
        arr_rank_score.append(score)




        ## 이미지 뽑기
        img = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[2]/a/img')
        src = img.get_attribute('src')
        arr_rank_img.append(src)
        #print("src  " , src)


        ## 줄거리
        lines = ""
        content = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div/div/p')
        for i in content:
            lines+=i.text




        #제작 노트 보기
        more_cnt = 0
        try :
            driver.find_element_by_css_selector("#toggleMakingnoteButton").click()
            driver.implicitly_wait(2)
            more_cnt+=1
        except NoSuchElementException :
            print("no such element(1)")




        #내용 더 보기
        if(more_cnt > 0 ) :
            try :
                driver.find_element_by_css_selector("#moreMakingnoteButton").click()
                driver.implicitly_wait(2)
            except :
                print("no such element(2)")


        if more_cnt > 0 :
            content = driver.find_elements_by_xpath('//*[@id="makingnotePhase"]')
            for i in content:
                lines+=i.text
        else :
            driver.implicitly_wait(1)
        #print(lines)




        #키워드 뽑기
        nouns=[]
        keywords=[]
        for noun in twitter.nouns(lines):
            if (len(noun) == 1 and noun in dic ):
                nouns.append(noun)
            elif (len(noun) > 1 ):
                nouns.append(noun)
            count = Counter(nouns)

        cnt_common = count.most_common(15)
        print ("--------------------------")
        for a in cnt_common :
            keywords.append(a[0])
            #print (a[0] , " | " , a )

        arr_rank_words.append(keywords)



        ## 감독 및 배우들
        actors = []
        director = ""
        act = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[4]/div[2]/div/ul/li[*]/a')
        for a in act :
            if a.text != '' :
                actors.append(a.text)

        ## 감독은 첫번째 배열에 저장됨
        director = actors[0]

        ## 감독 삭제
        del actors[0]


        f = open('rank_movie.csv', 'a+', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerow([name,src, score,  smr_arr, keywords, director, actors])
        f.close()



def click_ranking( ):

    for i in range(1,51):

        ## 각 리스트 영화를 클릭
        driver.find_element_by_css_selector("#old_content > table > tbody > tr:nth-child("+str(i+int((i-1)/10)+1)+") > td.title > div > a").click()
        driver.implicitly_wait(2)


        try :
            ## 영화 정보 갖고 오기
            get_inform()
        except :
            ## 만약 로그인이 필요한 페이지라면 need-login 출력
            print("need login - adult")

        ## 로그인이 필요 없으면 영화 정보 갖고 오고 뒤로 가고
        ## 로그인이 필요한 경우는 뒤로 가서 다음 영화 정보 갖고 오기
        driver.back()
        driver.implicitly_wait(1)



## 랭킹 페이지 현재 40페이지까지 존재
for i in range(1,5):
    if i== 1 :
        click_ranking()
    else:
        driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
        click_ranking()
        driver.implicitly_wait(2)
