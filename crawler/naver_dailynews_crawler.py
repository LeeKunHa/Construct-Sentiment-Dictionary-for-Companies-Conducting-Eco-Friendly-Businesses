
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import itertools
import pandas as pd


# 특수문자 및 영어등 텍스트 전처리 함수
def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    cleaned_text = ' '.join(cleaned_text.split())
    return cleaned_text


# 경향신문
# 각 네이버 일간지 기사 크롤링한 부분을 함수로 표현
def biz_khan(query, driver_path, page):
    head_list = []  # 기사 제목
    data_list = []  # 기사 내용

    current_page = 1  # 현재 페이지 1로 설정(1부터 page까지 크롤링)
    last_page = (int(page) - 1) * 10 + 1

    domain = '경향신문'  # 네이버뉴스에서 어떤 일간지 기사 가져올건지 도메인 설정(html)

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        # 달라지는 url 기준으로 변수설정해서 url 가져오기
        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1032&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 한페이지에 있는 기사 url을 list형태로 반환
        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:  # 기사가 없을 경우
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        # url_list안에 있는 모든 기사들 크롤링
        for url in url_list:

            # url_list에 None이 있을경우
            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)
            time.sleep(2)  # 로딩되는 시간 설정(2초)
            driver.get(url)
            time.sleep(2)

            # 각 언론사의 html 구조에 맞게 기사 제목과 내용 크롤링
            try:
                soup.find('h1', id='articleTtitle')
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.find('h1', id='articleTtitle').text)
                tags = soup.select_one('#container > div.main_container > div.art_cont > div.art_body').find_all('p')
                data = [clean_text(x.text) for x in tags]
                data_list.append(' '.join(data))

            except:  # html 구조가 다를경우
                try:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    head_list.append(soup.find('h1', id='article_title').text)
                    tags = soup.select_one('#articleBody').find_all('p')
                    data = [clean_text(x.text) for x in tags]
                    data_list.append(' '.join(data))

                except:  # html구조가 오류났을 경우
                    print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 국민일보
def kmib(query, driver_path, page):
    head_list = []
    data_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '국민일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1005&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)
            time.sleep(2)
            driver.get(url)
            time.sleep(2)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.select_one('#sub > div.sub_header > div > div.nwsti > h3').text)
                tags = soup.select_one("#articleBody").text
                data = tags.strip()
                data = data.strip('\t')
                data = clean_text(data)
                data_list.append(data)

            except:
                print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output



# 내일신문
def naeil(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '내일신문'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=2312&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)
            time.sleep(2)
            driver.get(url)
            time.sleep(2)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.select_one('#contentArea > div.caL2 > div > div.articleArea > h3').text)
                tags = soup.select_one("#contents").text
                data = tags.strip()
                data = data.strip('\t')
                data = clean_text(data)
                data_list.append(data)

            except:
                print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 동아일보
def donga(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '동아일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1020&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')

            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.select_one('#container > div.article_title > h1').text)
                tags = soup.select_one('#content > div > div.article_txt').text
                tags = clean_text(tags)
                data_list.append(tags)

            except:
                try:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    head_list.append(soup.select_one('#content > div.article_title > h2').text)
                    tags = soup.select_one('#ct').text
                    tags = clean_text(tags)
                    data_list.append(tags)

                except:
                    print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 매일일보
def m_i(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '매일일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=2385&nso=so%3Ar%2Cp%3Aall%2Ca%3Aall&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')

            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return ()
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(
                    soup.select('#user-container > div.custom-pc.float-center.max-width-1130 > header > div > div')[
                        0].text)
                tags = soup.find(id='article-view-content-div').find_all('p')
                data = [clean_text(x.text) for x in tags]
                data_list.append(' '.join(data))

            except:
                print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 문화일보
def munhwa(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '문화일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '%EB%89%B4%EC%8A%A4&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1021&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')

            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.find('span', class_='title').text)
                data = soup.select('#NewsAdContent')[0].text
                data = data.strip()
                data = data.strip('\t')
                data = clean_text(data)
                data_list.append(data)

            except:
                try:
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    head_list.append(soup.find('h3', id='articleTitle').text)
                    data = soup.select('#articleBodyContents')[0].text
                    data = data.strip()
                    data = data.strip('\t')
                    data = clean_text(data)
                    data_list.append(data)

                except:
                    print("None_type")
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 서울신문
def seoul(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '서울신문'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '%EB%89%B4%EC%8A%A4&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1081&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)
            time.sleep(2)
            driver.get(url)
            time.sleep(2)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.select_one('#viewWrapDiv > div.S20_title > div.S20_article_tit > h1').text)
                tags = soup.select_one("#atic_txt1").text
                data = tags.strip()
                data = data.strip('\t')
                data = clean_text(data)
                data_list.append(data)

            except:
                print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 세계일보
def segye(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '세계일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1022&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.select('#title_sns')[0].text)
                data = soup.find('article', class_='viewBox').text
                data = data.strip()
                data = clean_text(data)
                data_list.append(data)

            except:
                print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 아시아투데이
def asiatoday(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '아시아투데이'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=2268&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > sec6tion > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(soup.select('#section_top > div > h3')[0].text)
                data = soup.find('div', class_='news_bm').text
                data = data.strip()
                data = clean_text(data)
                data_list.append(data)

            except:
                print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 전국매일신문
def alldays(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '전국매일신문'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=2844&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            try:
                driver = webdriver.Chrome(executable_path=driver_path)
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head = clean_text(soup.find('div', class_="article-head-title").text)
                head_list.append(head)
                tags = soup.select_one('#article-view-content-div').find_all('p')
                data = [clean_text(x.text) for x in tags]
                data_list.append(' '.join(data))

            except:
                print("None_type")
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 조선일보
def joseon(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '조선일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1023&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            try:
                driver = webdriver.Chrome(executable_path=driver_path)
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head = clean_text(
                    soup.find_all("h1", class_="article-header__headline | font--primary text--black")[0].text)
                head_list.append(head)
                tags = soup.find_all('p',
                                     class_=' article-body__content article-body__content-text | text--black text font--size-sm-18 font--size-md-18 font--primary')
                data = [clean_text(x.text) for x in tags]
                data_list.append(' '.join(data))

            except:
                print("None_type")
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 중앙일보
def chungang(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '중앙일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1025&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            try:
                driver = webdriver.Chrome(executable_path=driver_path)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head = clean_text(soup.select('#article_title')[0].text)
                head_list.append(head)
                text = soup.find('div', id='article_body').text
                text = clean_text(text)
                data_list.append(text)

            except:
                print("None_type")
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 천지일보
def newscj(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '천지일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=2041&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            try:
                driver = webdriver.Chrome(executable_path=driver_path)
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head = clean_text(soup.find('div', class_="article-head-title").text)
                head_list.append(head)
                tags = soup.select_one('#article-view-content-div').find_all('p')
                data = [clean_text(x.text) for x in tags]
                data_list.append(' '.join(data))

            except:
                print("None_type")
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 한겨례
def hani(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '한겨례'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1028&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            try:
                driver = webdriver.Chrome(executable_path=driver_path)
                driver.get(url)
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head = clean_text(soup.find('span', class_='title').text)
                head_list.append(head)
                tags = soup.select_one('#a-left-scroll-in > div.article-text > div').find_all('div', class_='text')
                data = [clean_text(x.text) for x in tags]
                data_list.append(' '.join(data))

            except:
                print("None_type")
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 한국일보
def hankook(query, driver_path, page):
    data_list = []
    head_list = []

    current_page = 1
    last_page = (int(page) - 1) * 10 + 1

    domain = '한국일보'

    while current_page < last_page:

        driver = webdriver.Chrome(executable_path=driver_path)

        url_domain = 'https://search.naver.com/search.naver?where=news&query='
        news_domain = '%EB%89%B4%EC%8A%A4&sm=tab_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1469&nso=&is_sug_officeid=0'
        url = url_domain + query + '&%2Ca%3A&start=' + str(current_page) + news_domain
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        try:
            news_list = soup.select('#main_pack > section > div > div.group_news > ul')
            url_list = []
            news_list = news_list[0].find_all('li')
            for url in news_list:
                url_list.append(str(url.find_all('a')[0].get('data-url')))

        except:
            print('기사가 없습니다.')
            driver.close()
            return 0
        driver.close()

        for url in url_list:

            if url == 'None':
                continue

            driver = webdriver.Chrome(executable_path=driver_path)  # for Windows
            driver.get(url)
            time.sleep(2)

            try:
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                head_list.append(clean_text(soup.find('h2').text))
                tags = soup.select_one(
                    'body > div.wrap > div.container.end.end-uni > div.end-body > div > div.col-main.read').find_all(
                    'p')
                data = [clean_text(x.text) for x in tags]
                data_list.append(data)

            except:
                print('None_type')
            driver.close()
        current_page += 10

    output = pd.DataFrame({'언론사': [domain] * len(head_list),
                           '제목': head_list,
                           '내용': data_list})
    return output


# 원하는 keyword와 페이지 수 설정해서 크롤링
def crawling_news(query,driver_path,max_page):
    biz_df = biz_khan(query,driver_path,max_page)
    kmib_df = kmib(query,driver_path,max_page)
    naeil_df = naeil(query,driver_path,max_page)
    donga_df = donga(query,driver_path,max_page)
    mi_df = m_i(query,driver_path,max_page)
    munhwa_df = munhwa(query,driver_path,max_page)
    seoul_df = seoul(query,driver_path,max_page)
    segye_df = segye(query,driver_path,max_page)
    asia_df = asiatoday(query,driver_path,max_page)
    alldays_df = alldays(query, driver_path,max_page)
    joseon_df = joseon(query, driver_path,max_page)
    chungang_df = chungang(query, driver_path,max_page)
    cj_df = newscj(query,driver_path,max_page)
    hani_df = hani(query,driver_path,max_page)
    hk_df = hankook(query,driver_path,max_page)

    # dataframe 합칠때 None인 데이터들은 구별해주기 위해 list만듬
    df_list = [biz_df, kmib_df, naeil_df, donga_df, mi_df, munhwa_df, seoul_df, segye_df, asia_df, alldays_df,
               joseon_df, chungang_df, cj_df, hani_df, hk_df]

    # dataframe안이 str형일때만 apoend
    names = []
    for name in df_list:

        if type(name) != int:
            names.append(name)

    # 각각의 news df 합치기, 제목중복되는것들은 drop시켜주고, 제목과 언론사는 필요없으니 drop
    news_df = pd.concat(names)
    news_df.drop_duplicates(['제목'], inplace=True, ignore_index=True)
    news_df = news_df.drop(['제목'], axis=1)
    news_df = news_df.drop(['언론사'], axis=1)

    return news_df


# 라벨링할 문장 split하는 함수
def create_news_df_split(df_len,news_df):
    text = []
    count = 0  # 의미없는변수 (except를 위해만듬)
    tp=''
    for x in range(0, df_len):

        try:  # '다'를 기준으로 문장을 나눔
            tp = news_df['내용'][x]
            tp = tp.split('다.')
            tp = [x + '다' for x in tp]
            tp = clean_text(tp)
            print(tp)

        except:
            count += 1

        text.append(tp)
    text = list(itertools.chain(*text))

    df = pd.DataFrame([x for x in text])

    return df


##############메인#################

#
# 각자 chromedriver.exe 경로 수정
if __name__ == '__main__':
    driver_path = './chromedriver.exe'

    news_df = crawling_news('친환경',2)

    df_len = len(news_df)
    news_df.to_csv('친환경_news.csv', encoding='utf-8-sig')

    news_split_df=create_news_df_split(df_len)
    news_split_df.to_csv('친환경_news_split.csv',encoding='utf-8-sig')
