## 코드 설명



### Crawler / crawler.py

sns, 커뮤니티, 뉴스기사(naver_dailynews_crawler.py)를 통합해서 만든 코드이며,

크롤링 해올 페이지수를 입력하면, 해당 수치에 맞게 데이터를 크롤링 해옵니다.



#### 입력 예시 )



![](https://github.com/Data-campus-SloganAnalysis/Main/blob/main/img/1_.png?raw=true)



### Sentiment_dictionary / senti_dict.py

senti_dict는 라벨링된 데이터를 불용어처리 작업을 거친다음 명사 데이터만 추출 해서, 로지스틱 리그레션을 통해 긍정 부정 감성수치를 만들어줍니다.



#### 수치화된 긍정, 부정 단어 예시 )

![](https://github.com/Data-campus-SloganAnalysis/Main/blob/main/img/2_.png?raw=true)

![](https://github.com/Data-campus-SloganAnalysis/Main/blob/main/img/3_.png?raw=true)



### Visualization / visualization.py

visualization은 문장별로 나뉘어진 크롤링 데이터의 단어들간 유사도를 비교해, 앞서 senti_dict에서 분석한 감성수치와 함께 그래프로 나타내줍니다.



#### 입력 예시 )

![](https://github.com/Data-campus-SloganAnalysis/Main/blob/main/img/4_.png?raw=true)



#### 빈도 분석 결과 )

![](https://github.com/Data-campus-SloganAnalysis/Main/blob/main/img/5_.png?raw=true)



#### 최종 결과물 )



파란색 - 긍정 / 빨간색 - 부정

<img src ="https://github.com/Data-campus-SloganAnalysis/Main/blob/main/img/6_.png?raw=true" width="500px"/>









