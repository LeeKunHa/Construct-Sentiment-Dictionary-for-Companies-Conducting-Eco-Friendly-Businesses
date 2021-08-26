from Visualization import visualization
from Crawler import crawler as cr
from Sentiment_dictionary import Senti_dict as sd

import pandas as pd

if __name__ == "__main__":
    dict_data_path = './Data/dict.csv'
    stopwords_path = './Data/stopwords.txt'
    # 만약 감성사전, 단어빈도수 데이터 업데이트 필요 시에 사용
    #cr.run_crawler()

    sd.update_dict()
    visualization.words_freq_update()
    # 감성사전, 불용어 정보
    sent_dict = pd.read_csv(dict_data_path,encoding='cp949')
    with open(stopwords_path,'r') as op:
        stopwords = op.readlines()
        stopwords = stopwords[0].split(',')

    # 시각화에 필요한 단어 빈도수 그래프
    news_data = pd.read_csv('./Data/news_words_freq.csv',encoding='cp949')
    community_data = pd.read_csv('./Data/community_words_freq.csv',encoding='cp949')
    sns_data = pd.read_csv('./Data/sns_words_freq.csv',encoding='cp949')

    do = ''
    while not(do in ['뉴스','sns','커뮤니티']):
        do = input('뉴스, sns, 커뮤니티 중에 결정해주세요\n')
    inputs = []
    while(True):
        if do == '뉴스':
            keyword = input('검색어를 입력하세요. 마치고 싶으면 # 을 입력하세요\n')
            if keyword != '#':
                inputs.append(keyword)
            else:
                visualization.draw(news_data, sent_dict, inputs, 8)
                break
        elif do == 'sns':
            keyword = input('검색어를 입력하세요. 마치고 싶으면 # 을 입력하세요\n')
            if keyword != '#':
                inputs.append(keyword)
            else:
                visualization.draw(sns_data, sent_dict, inputs, 8)
                break
        else:
            keyword = input('검색어를 입력하세요. 마치고 싶으면 # 을 입력하세요\n')
            if keyword != '#':
                inputs.append(keyword)
            else:
                visualization.draw(community_data, sent_dict, inputs, 8)
                break