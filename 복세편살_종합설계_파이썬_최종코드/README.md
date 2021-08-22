# Quant, Investing Helper(파이썬 코드 관련 readme 파일입니다.) 
__KOSPI 783개의 종목의 재무제표와 보조지표를 활용한 종목 추천__
```
python
├─ indicator.py                # 보조지표 생성 함수 저장
├─ python-stock-crawler.py     # 주가 데이터 매일 수집할수있도록 구현
├─ const.py     # 시각화 및 개발 및 분석에 자주 사용하는 함수
├─ quant_strategy.py # 주식 종목추천 전략 및 백테스트 모듈 저장
│  
├─ jupyter notebook
│  └─ 1. 연도별 재무데이터프레임 생성.ipynb   # 재무데이터 정제
│  └─ 2. 전략 구현하기.ipynb  # 종목추천에 활용할 전략
│  └─ 3. 백테스트 구현 및 결과확인.ipynb  #백테스트 결과 확인
│  └─ k-means 지지선 산출.ipynb
├─ R_script
│  └─ 1. KOSPI_ticker.R
│  └─ 2. 재무 및 가치지표 수집.R
│  └─ 3. 재무 및 가치지표 정리하기.R
└─ README.md
```

.ipynb(jupyter notebook) 파일로 python 모듈을 활용한 결과 및 과정을 정리하였습니다. 모듈의 실행 과정 또한 .ipynb를 참고하시면 됩니다.

##### &#10004; 필요한 python Library
```
$ pip install beautifulsoup4
$ pip install pandas
$ pip install numpy
$ pip install pyplot
$ pip install matplotlib
$ pip install yahoo-finance
$ pip install selenium
```

