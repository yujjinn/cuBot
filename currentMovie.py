from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import time
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException
from konlpy.tag import Twitter
from collections import Counter
from dict import dic
from webdriver_manager.chrome import ChromeDriverManager
import pymysql


#--------------------------현재 상영 페이지--------------------------#
url = 'https://movie.naver.com/movie/running/current.nhn'
driver =webdriver.Chrome('C:\chromedriver') ## 경로
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')

#--------------------------현재 상영 페이지--------------------------#

twitter = Twitter()

arr_current_name = []
arr_current_smr = []
arr_current_score = []
arr_current_img = []
arr_current_words = []
titleName = ""
##현재 상영 영화
name = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li[*]/dl/dt/a')

#sql = "insert into movie2(image,NAME,jenre,director,Actor,rating,keyword1,keyword2,keyword3,keyword4,keyword5,keyword6) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql = "insert into movie2 select %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s from dual WHERE NOT EXISTS (select NAME from movie2 where NAME = %s);"
keyword1= ""
keyword2= ""
keyword3= ""
keyword4= ""
keyword5= ""
keyword6= ""
for i in name:
    arr_current_name.append(i.text)


current_size = len(arr_current_name)+1


for i in range(1,current_size) :
    print ("----------------", i , "----------------")
    titleName = arr_current_name[i-1]
    print(arr_current_name[i-1])
    driver.find_element_by_css_selector("#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li:nth-child("+str(i)+") > dl > dt > a").click()
    driver.implicitly_wait(2)

    ## 개요 뽑기
    smr = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[1]/*')
    smrContent = ""
    for i in smr:
        arr_current_smr.append(i.text)
        smrContent += (i.text+",")
    smrContent = smrContent[:-1]
    print("개요 : " + smrContent)

    ##감독
    director = ""
    dir = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[2]/p/a')
    for i in dir :
        director += (i.text+",")
    director = director[:-1]
    print("감독 : " + director)


    ##배우
    actors =  ""
    act = driver.find_elements_by_xpath('//*[@id="content"]/div[1]/div[4]/div[2]/div/ul/li[*]/a[2]')
    cnt = 0 
    for i in act :
        cnt = cnt + 1
        if cnt > 1 :
            actors += (i.text + ",")
    actors = actors[:-1]
    print("배우들 " + actors)
    ##평점
    score = ""
    for i in range(1,5):
        get_num = driver.find_element_by_xpath('//*[@id="pointNetizenPersentBasic"]/em['+str(i)+']')
        score += get_num.text
    print("score " , score)
    arr_current_score.append(score)

    ## 이미지 뽑기
    srcAddress=""
    try :
        img = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[2]/a/img')
        src = img.get_attribute('src')
    except :
        img = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[2]/img')
        src = img.get_attribute('src')
    arr_current_img.append(src)
    srcAddress = src
    print("src  " , src)



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
    print(lines)




    #키워드 뽑기
    nouns=[]
    keywords=[]
    for noun in twitter.nouns(lines):
        if (len(noun) == 1 and noun in dic ):
            nouns.append(noun)
        elif (len(noun) > 1 ):
            nouns.append(noun)
        count = Counter(nouns)

    cnt_common = count.most_common(6)  # 최다 빈출 키워드 6개까지 저장
    print ("--------------------------")
    cnt = 0
    for a in cnt_common :
        cnt = cnt + 1
        if cnt == 1:
            keyword1 = a[0]
        elif cnt == 2 :
            keyword2 = a[0]
        elif cnt == 3 :
            keyword3= a[0]
        elif cnt == 4 :
            keyword4 = a[0]
        elif cnt == 5 :
            keyword5 = a[0]
        elif cnt == 6 :
            keyword6 = a[0]

        keywords.append(a[0])

        print (a[0] , " | " , a )
    print(keyword1 + " "  + keyword2 + " " +keyword3 + " "+keyword4 + " "  + keyword5 + " " +keyword6)

    arr_current_words.append(keywords)

    db = pymysql.connect(host = 'aws주소', user = '사용자명', password = '비밀번호' ,db = 'db명')
    cursor = db.cursor()
    test_director = "test"
    test_actor = "testActor"
    cursor.execute(sql,(srcAddress,titleName,smrContent,director,actors,score,keyword1,keyword2,keyword3,keyword4,keyword5,keyword6,titleName))
    driver.implicitly_wait(2)
    db.commit()

    driver.back()
    driver.implicitly_wait(1)

db.close()


