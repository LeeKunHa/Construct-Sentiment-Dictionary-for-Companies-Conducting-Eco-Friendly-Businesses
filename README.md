# 친환경 사업을 진행하는 기업 이미지를 위한 감정사전 구축

김진성 박채희 신한영 이건하 이아영 한현수



## 설치환경

IDE: Pycharm

사용언어 : python

### 라이브러리

- konlpy : **Jpype 설치를 안한 경우만** 

  https://www.lfd.uci.edu/~gohlke/pythonlibs/#jpype 에서 파이썬 버전에 알맞는 Jpype 설치 후 JAVA_HOME 환경변수로 Jpype directory 설정 (관련 문서 :https://konlpy-ko.readthedocs.io/ko/v0.4.3/install/#id2)

- Mecab : **Visual studio 2019가 없는 경우만**

  https://visualstudio.microsoft.com/ko/vs/older-downloads/ 에서 '재배포 가능 패키지 및 빌드 도구' 의 'Microsoft Build Tools 2015 업데이트 3' 다운로드 및 설치 (관련 블로그 :https://somjang.tistory.com/entry/Windows-%EC%97%90%EC%84%9C-Mecab-mecab-%EA%B8%B0%EB%B0%98-%ED%95%9C%EA%B5%AD%EC%96%B4-%ED%98%95%ED%83%9C%EC%86%8C-%EB%B6%84%EC%84%9D%EA%B8%B0-%EC%84%A4%EC%B9%98%ED%95%98%EB%8A%94-%EB%B0%A9%EB%B2%95)

- 그 후 설치해야 할 라이브러리의 정보와 버전이 있는 requirement.txt 를 Pycharm의 터미널에서 ``pip install -r requirement.txt`` 실행



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









