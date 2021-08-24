import naver_dailynews_crawler as ndn

#웹페이지 분석을 위한 라이브러리 입니다.
from bs4 import BeautifulSoup
#크롬드라이버를 사용하기 위한 라이브러리입니다.
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#크롬을 통한 데이터 크롤링시, 봇 벤 방지를 막기 위한 시간초 제한을 두기 위한 라이브러리입니다.
import time
#정규식을 활용하기 위한 라이브러리 입니다.
import re
#데이터프레임형을 생성하기 위한 라이브러리 입니다.
import pandas as pd
#json구조를 활용하기 위한 라이브러리 입니다.
import json
#프로그램을 돌리는 사용자의 os를 활용하기 위한 라이브러리 입니다.
import os, sys
#트위터 api 입니다.
import tweepy
import itertools
import numpy as np


def twitter_crawler(driver, path):
    # 사용자의 경로를 가져옵니다.
    sys.path.append(os.pardir)

    key_path = './api_key.json'
    with open(key_path, 'r') as f:
        key = json.load(f)

    # 개인정보 인증을 요청하는 Handler입니다.
    auth = tweepy.OAuthHandler(key['CONSUMER_KEY'], key['CONSUMER_SECRET'])

    # 인증 요청을 수행합니다.
    auth.set_access_token(key['ACCESS_TOKEN_KEY'], key['ACCESS_TOKEN_SECRET'])

    # twitter API를 사용하기 위한 준비입니다.
    api = tweepy.API(auth, wait_on_rate_limit=True)


# 트위터 게시물 가져오는 단계
def twitter_crawling(keyword,api,page):
    columns = ['내용']
    df = pd.DataFrame(columns=columns)

    max_tweets = 10
    searched_tweets = [status for status in tweepy.Cursor(api.search, q=keyword).items(max_tweets)]

    for tweet in searched_tweets:
        tweet_json = tweet._json
        tweet_text = tweet_json['text']
        row = [tweet_text]
        series = pd.Series(row, index=df.columns)
        df = df.append(series, ignore_index=True)

    df['내용'] = df['내용'].apply(lambda x: clean_text(x))
    df = df.drop_duplicates(subset=['내용'])

    return df

def insta_crawler(driver):
    # 인스타 게시물을 불러오기 위한 사전작업 단계
    driver.get('https://www.instagram.com/')
    p_tag = WebDriverWait(driver, timeout=5).until(EC.presence_of_element_located((By.TAG_NAME, "P")))

    time.sleep(1)

    # 인스타그램 로그인을 위한 계정정보
    email = 'data.campuss'
    input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
    input_id.clear()
    input_id.send_keys(email)

    password = 'data.2021'
    input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
    input_pw.clear()
    input_pw.send_keys(password)
    input_pw.submit()

    time.sleep(3)

    driver.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF').click()
    time.sleep(3)
    driver.find_element_by_css_selector('button.aOOlW.HoLwm').click()
    time.sleep(1)

def insta_searching(word):
    url = 'https://www.instagram.com/explore/tags/' + str(word)
    return url

def click_first(driver):
    time.sleep(3)
    first = driver.find_element_by_css_selector('div._9AhH0')
    first.click()
    time.sleep(3)

def next_page(driver):
    next_page = driver.find_element_by_css_selector(
        'body > div._2dDPU.CkGkG > div.EfHg9 > div > div > a._65Bje.coreSpriteRightPaginationArrow')
    next_page.click()
    time.sleep(3)

def get_content(driver):

    # 1. 현재 페이지의 HTML 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    tag_list = []
    # 2. 본문내용
    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ''
    # 3. 본문 내용에서 해시태그 가져오기(정규표현식 활용)
    tags = re.findall('#[A-Za-z0-9가-힣]+', content)
    tag = ''.join(tags).replace("#", " ")  # "#" 제거
    tag_data = tag.split()
    for tag_one in tag_data:
        tag_list.append(tag_one)

    data = [content, tag_data]
    return data

def clean_text(text):
    cleaned_text = re.sub('[^ ㄱ-ㅣ가-힣]+',' ',text)
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text


def insta_crawling(driver, keyword, target):
    result_list = []
    url = insta_searching(keyword)
    driver.implicitly_wait(1)
    driver.get(url)
    time.sleep(1)

    click_first(driver)

    for i in range(target):
        try:
            result_list.append(get_content(driver))
            next_page(driver)
        except:
            time.sleep(1)
            next_page(driver)
    df = pd.DataFrame(result_list)
    df.columns = ['내용', '해시태그']
    df['내용'] = df['내용'].apply(lambda x: clean_text(x))
    df['해시태그'] = df['해시태그'].apply(lambda x: str(x))
    df['해시태그'] = df['해시태그'].apply(lambda x: clean_text(x))
    df['내용'] = df['내용'] + df['해시태그']
    df.drop(['해시태그'], axis=1, inplace=True)
    df = df.drop_duplicates(subset=['내용'])
    return df

def sns_main(key_word,page):
    key_path = './api_key.json'
    with open(key_path, 'r') as f:
        key = json.load(f)
    driver = webdriver.Chrome(path)
    # 개인정보 인증을 요청하는 Handler입니다.
    auth = tweepy.OAuthHandler(key['CONSUMER_KEY'], key['CONSUMER_SECRET'])
    # 인증 요청을 수행합니다.
    auth.set_access_token(key['ACCESS_TOKEN_KEY'], key['ACCESS_TOKEN_SECRET'])
    # twitter API를 사용하기 위한 준비입니다.
    api = tweepy.API(auth, wait_on_rate_limit=True)

    insta_crawler(driver)

    for i in key_word:
        keyword = i
        target = page*100
        insta_df = insta_crawling(driver, keyword, target)
        time.sleep(1)
        twitter_df = twitter_crawling(keyword,api,target)
        sns_df = pd.concat([twitter_df, insta_df], join='outer', ignore_index=True)
        sns_df.to_csv('../Data/crawling data/'+i+'_sns.csv', encoding='utf-8-sig')


# 뽐뿌 웹사이트 크롤러 입니다.
def ppomppu_crawler(query, driver_path, page):
    # 셀리니움을 활용해서 크롬 웹브라우저로 검색을 합니다.
    driver = webdriver.Chrome(executable_path=driver_path)
    text = []

    for i in range(1, page + 1):
        post_links = []

        base_url = 'https://www.ppomppu.co.kr/'
        # 입력한 페이지수와 쿼리로 크롤링을 해옵니다.
        parm = 'search_bbs.php?page_size=50&bbs_cate=2&keyword=' + query + '&order_type=date&search_type=sub_memo&page_no=' + str(
            i)
        url = base_url + parm
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 뽐뿌의 경우 한페이지에 50개의 게시물이 있습니다.
        for j in range(1, 51):
            if soup.select('body > div > div.contents > div.container > div > form > div > div:nth-of-type(' + str(
                    j) + ') > div > p.desc > span:nth-of-type(1)')[0].text != '[뽐뿌게시판]':
                try:  # 예고와 유안타가 들어간 게시글은 봇이 작성한 무의미한 게시글 이였습니다.
                    if '예고' not in soup.select(
                            'body > div > div.contents > div.container > div > form > div > div:nth-of-type(' + str(
                                    j) + ') > div > span > a')[0].text:
                        if '유안타' not in soup.select(
                                'body > div > div.contents > div.container > div > form > div > div:nth-of-type(' + str(
                                        j) + ') > div > span > a')[0].text:
                            post_links.append(soup.select(
                                'body > div > div.contents > div.container > div > form > div > div:nth-of-type(' + str(
                                    j) + ') > div > span > a'))
                except:
                    print('')

        for k in range(len(post_links)):
            try:  # 게시물 안에서 입력된 텍스트들을 가져옵니다(게시물 본문)
                base_url = 'https://www.ppomppu.co.kr/'
                link_url = base_url + post_links[k][0].get('href')
                driver.get(link_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                temp = soup.find_all('td', class_='board-contents')
                text.append(clean_text(temp[0].text))
            except:
                print('')

    driver.close()
    return text


# 에프엠 코리아 웹사이트 크롤러 입니다.
def fmkorea_document(query, driver_path, page):
    driver = webdriver.Chrome(executable_path=driver_path)
    data_list = []

    for i in range(1, page + 1):
        base_url = 'https://www.fmkorea.com/?act=IS&is_keyword='
        parm = query + '&mid=home&where=document&page=' + str(i)
        url = base_url + parm
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for j in range(1, 11):
            regex = "\[[^]]*\]"
            title = soup.select('#content > div > ul.searchResult > li:nth-of-type(' + str(j) + ') > dl > dt > a')
            title = title[0].text
            title = re.sub(regex, '', str(title))
            title = clean_text(title)

            contents = soup.select('#content > div > ul.searchResult > li:nth-of-type(' + str(j) + ') > dl > dd')
            contents = clean_text(contents[0].text)
            data_list.append(title + contents)
    driver.close()

    return data_list


# 인스티즈 웹사이트 크롤러 입니다.
def instiz(query, driver_path, page):
    driver = webdriver.Chrome(executable_path=driver_path)
    data_list = []

    for i in range(1, page + 1):
        base_url = 'https://www.instiz.net/popup_search.htm#gsc.tab=0&gsc.q='
        parm = query + '&gsc.page=' + str(i)
        url = base_url + parm
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        title = ''
        content = ''
        comment = ''
        for j in range(1, 11):
            try:
                content_url = soup.select(
                    '#___gcse_0 > div > div > div > div.gsc-wrapper > div.gsc-resultsbox-visible > div.gsc-resultsRoot.gsc-tabData.gsc-tabdActive > div > div.gsc-expansionArea > div:nth-of-type(' + str(
                        j) + ') > div.gs-webResult.gs-result > div.gsc-thumbnail-inside > div > a')[0].get('href')
                driver.get(str(content_url))
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                try:
                    title = soup.select('#nowsubject > a')[0].text
                    content = soup.select('#memo_content_1')[0].text
                    content = content.replace('  에 게시된 글입니다', '')
                    content = content.replace('← 빈공간을 더블탭 해보세요 →', '')
                    comment = soup.select('#ajax_table > tbody')[0].text
                    comment = clean_text(comment)
                    # 임의로 전처리...
                    comment = comment.replace('•••', '')
                    comment = comment.replace('답글 스크랩 신고', '')
                except:
                    print("")
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                data_list.append(title + content + comment)
            except:
                print('')
    driver.close()

    return data_list


# 네이트판 웹사이트 크롤러 입니다.
def nate_pann_crawler(query, driver_path, page):
    driver = webdriver.Chrome(executable_path=driver_path)
    text = []

    for i in range(1, page + 1):
        post_links = []

        base_url = 'https://pann.nate.com'
        parm = '/search/talk?q=' + query + '&sort=DD&page=' + str(i)
        url = base_url + parm
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for j in range(1, 11):
            if '주식뉴스모음' not in soup.select(
                    '#container > div.content.sub > div.srcharea > div.srch_list.section > ul > li:nth-of-type(' + str(
                            j) + ') > div.tit > a')[0].text:
                post_links.append(soup.select(
                    '#container > div.content.sub > div.srcharea > div.srch_list.section > ul > li:nth-of-type(' + str(
                        j) + ') > div.tit > a'))

        for k in range(len(post_links)):
            try:
                link_url = base_url + post_links[k][0].get('href')
                driver.get(link_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                temp = soup.select('#contentArea')[0].text
                text.append(clean_text(temp))
            except:
                print('')

    driver.close()
    return text


# dc 웹사이트 크롤러 입니다.
def dc(query, driver_path, page):
    driver = webdriver.Chrome(executable_path=driver_path)

    text = []

    for i in range(1, page + 1):
        post_links = []

        base_url = 'https://search.dcinside.com/post/q/.'

        url = base_url + query + '/p/' + str(i)

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for j in range(1, 26):
            post_links.append(soup.select(
                '#container > div > section.center_content > div.inner > div.integrate_cont.sch_result.result_all > ul > li:nth-of-type(' + str(
                    j) + ') > a'))

        for k in range(len(post_links)):

            try:
                link_url = post_links[k][0].get('href')
                driver.get(link_url)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                temp = soup.find_all('div', class_='write_div')[0].text

                text.append(clean_text(temp))
            except:

                print('')
    driver.close()
    return text


# 루리 웹사이트 크롤러 입니다.
def ruli(query, driver_path, page):
    driver = webdriver.Chrome(executable_path=driver_path)
    text = []

    for i in range(1, page + 1):
        base_url = 'https://bbs.ruliweb.com/search?q='
        url = base_url + query + '&page=' + str(i) + '&c_page=' + str(
            i) + '#comment_search&gsc.tab=0&gsc.q=' + query + '&gsc.page=1'
        driver.get(url)
        driver.refresh()
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for j in range(1, 16):
            comment = soup.select(
                '#comment_search > div > ul > li:nth-of-type(' + str(j) + ') > div > div > a.title.text_over')
            comment = comment[0].text
            comment = clean_text(comment)
            text.append(comment)
            title = soup.select(
                '#board_search > div > ul > li:nth-of-type(' + str(j) + ') > div > div > a.title.text_over')
            title = title[0].text
            tilte = clean_text(title)  # 게시물에 신문기사가 너무 많아서 우선 게시물의 제목만 가져왔습니다
            text.append(title)
    driver.close()
    return text


def community_crawler(key_word,page,driver_path):
    text = []
    for i in key_word:
        text.extend(ppomppu_crawler(i,driver_path,page))
        text.extend(fmkorea_document(i,driver_path,page))
        text.extend(instiz(i,driver_path,page))
        text.extend(nate_pann_crawler(i,driver_path,page))
        text.extend(dc(i,driver_path,page))
        text.extend(ruli(i,driver_path,page))


        #크롤링 해온 본문들을 데이터프레임화 합니다.
        df = pd.DataFrame(text,columns=['text'])

        #크롤링해온 본문중 빈 게시글(숫자나 특수기호로 이루어져있어 비어져버린 경우)을 제거해줍니다.
        drop_index = df[df['text']==""].index
        df.drop(drop_index,inplace=True)

        #긁어온 데이터를 csv파일로 저장합니다.
        df.to_csv('../Data/crawling data/'+i+'_community.csv',encoding='utf-8-sig')

def news_crawler(key_word,page,path):
    for i in key_word:
        news_df = ndn.crawling_news(i, path, page + 1)
        df_len = len(news_df)
        news_df.to_csv('../Data/crawling data/' + i + '_news.csv', encoding='utf-8-sig')
        news_split_df = ndn.create_news_df_split(df_len,news_df)
        news_split_df.to_csv('../Data/crawling data/' + i + '_news_split.csv', encoding='utf-8-sig')

def run_crawler():
    key_word = ['환경오염', '친환경']
    # 사용자의 경로를 가져옵니다.
    sys.path.append(os.pardir)
    # 맥 사용시
    # path = './chromedriver'

    # 윈도우 사용시
    path = './chromedriver.exe'

    update = input('기업 환경 사전 구축 시스템에 오신것을 환영합니다!\n사전을 업데이트 하시겠습니까?\nY or N 으로 입력.\n')
    if update == 'Y' or update == 'y':
        page = int(input('크롤링 해올 페이지 수를 입력하세요!\n'))

        community_crawler(key_word, page, path)
        sns_main(key_word, page)
        news_crawler(key_word, page,path)

        print('크롤링 완료 !!\n')

    elif update == 'N' or update == 'n':
        print('기존 사전으로 분석을 시작하겠습니다.')


if __name__ == "__main__":
    run_crawler()


