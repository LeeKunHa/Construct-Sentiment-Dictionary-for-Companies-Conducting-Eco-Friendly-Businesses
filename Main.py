from Senti_dict import *
from visualization import *

import pandas as pd

if __name__ == "__main__":
    dict_data_path = './Data/dict.csv'
    stopwords_path = './Data/stopwords.txt'

    # 만약 감성사전, 단어빈도수 데이터 업데이트 필요 시에 사용
    #  update_dict()
    words_freq_update()

    sent_dict = pd.read_csv(dict_data_path,encoding='cp949')
    with open(file_path,'r') as op:
        stopwords = op.readlines()
        stopwords = stopwords[0].split(',')

    news_data = pd.read_csv('./Data/news_words_freq.csv',encoding='cp949')
    community_data = pd.read_csv('./Data/community_words_freq.csv',encoding='cp949')
    sns_data = pd.read_csv('./Data/sns_words_freq.csv',encoding='cp949')