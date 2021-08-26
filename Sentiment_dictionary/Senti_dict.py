import pandas as pd
import re

from konlpy.tag import Okt
from eunjeon import Mecab
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegressionCV

from sklearn.metrics import accuracy_score


features = 5000
file_path = './data/stopwords.txt'
with open(file_path,'r') as op:
    stopwords = op.readlines()
    stopwords = stopwords[0].split(',')


def tokenizer(text):
    #okt = Okt()
    mecab = Mecab()
    poses = ['NNG', 'NNP', 'NNB', 'NR', 'NP']
    re.sub('[\W]',' ',text)
    result = []
    token_pos = mecab.pos(text)
    for word, pos in token_pos:
        if (pos in poses) and not(word in stopwords):
            result.append(str(word))
    return result



def update_dict():
    data = pd.read_csv('./Data/labeling_data.csv',encoding='utf-8-sig')
    x = data['내용'].astype('str')
    y = data['label']

    tfidf = TfidfVectorizer(max_features=features,tokenizer=tokenizer)
    x_tdm = tfidf.fit_transform(x)

    x_train, x_test, y_train, y_test = train_test_split(x_tdm,y,
                                                       test_size=0.3,
                                                       random_state=42)

    lr_clf = LogisticRegressionCV(max_iter=1000)
    lr_clf.fit(x_train,y_train)

    pred =lr_clf.predict(x_test)

    st_df = pd.DataFrame({'단어':tfidf.get_feature_names(),
                          '회귀계수':lr_clf.coef_.flat})
    st_df.tail()


    st_neg = st_df[st_df['회귀계수']<0].sort_values('회귀계수')
    ma = st_neg['회귀계수'].max()
    mi = st_neg['회귀계수'].min()
    st_neg['points']=st_neg['회귀계수'].apply(lambda x : ((x - mi)/(ma - mi) - 1))

    st_pos = st_df[st_df['회귀계수']>0].sort_values('회귀계수',ascending=False)
    ma = st_pos['회귀계수'].max()
    mi = st_pos['회귀계수'].min()
    st_pos['points']=st_pos['회귀계수'].apply(lambda x : ((x - mi)/(ma - mi)))

    st_df = st_pos.append(st_neg)
    st_df.to_csv('./data/dict'+str(features)+'.csv',encoding='utf-8-sig')

