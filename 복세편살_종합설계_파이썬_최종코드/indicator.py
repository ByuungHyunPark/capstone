import pandas as pd
import numpy as np

"""
1. MA : 이동평균선
2. RSI : 상대 강도 지수
3. MACD : 장기 지수이동평균선과 단기 지수이동평균선의 벌어진 차이를 활용하는 이동평균수렴확산지수
4. 변동성
"""

def ma(stock_df, period, column='종가'):
    '''
    설정한 period에 해당하는 이동평균선을 구하는 함수
    Args:
      stock_df(pd.DataFrame):종목별 주가 데이터프레임
      period(int):
    Return:
      stock_df(pd.DataFrmae):설정한period에 해당하는 이동평균선 Column 생성한 데이터프레임 반환
     
    '''
    ma_array = stock_df[column].rolling(window=period).mean()
    ma_col_name = f'MA_{period}'
    stock_df.loc[:, ma_col_name] = ma_array
    return stock_df


def rsi(stock_df, period=14, column='종가'):
    """
    - 상대 강도 지수(Relative Strength Index)의 약자
    - 가격의 상승압력과 하락압력간의 상대적인 강도를 나타내는 지수
    - RSI = 100 - (100 / (1+RS))
    Args:
      stock_df(pd.DataFrame):종목별 주가 데이터프레임4
      period(int) : RSI관련 논문은 보통 14로 설정
    Returns:
      stock_df(pd.DataFrame):RSI 열을 추가한 데이터프레임 반환  
    """
    delta = stock_df[column].diff(1)
    delta = delta.dropna()
    
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    stock_df['up'] = up
    stock_df['down'] = down
    
    AVG_Gain = stock_df['up'].rolling(window=period).mean()
    AVG_Loss = abs(stock_df['down'].rolling(window=period).mean())
    stock_df.drop(['up','down'], axis=1, inplace=True)
    RS = AVG_Gain / AVG_Loss
    RSI = 100.0 - (100.0 / (1.0 + RS))
    
    #데이터프레임에 RSI 지표 추가
    stock_df['RSI'] = RSI
    
    return stock_df


def macd(stock_df, period_long = 26, period_short = 12, period_signal = 9, column = '종가'):
    """    
    - moving average concergence divergence 의 약자로 단순하면서 신뢰성이 높은 지표
    - MACD  = 단기지수이동평균 - 장기지수이동평균
    Args:
        stock_df(pd.DataFrame)
        period_long(int) : default(26)
        period_short(int) : default(12)
        period_signal(int) : default(9)
    Returns:
        sotck_df(pd.DataFrmae) : [MACD, signal_Line, osiliaotr] 3개의 Column이 추가된 데이터프레임 반환
    """
    #단기 지수 이평선 계산
    shortMA = stock_df[column].rolling(window=period_short).mean()
    
    #장기 지수 이평선 계산
    longMA = stock_df[column].rolling(window=period_long).mean()

    # 이동평균 수렴/발산 계산
    MACD = shortMA - longMA
    
    #신호선 계산 (MACD의 이동평균선)
    signal_Line = MACD.rolling(window = period_signal).mean()
    
    
    #데이터프레임에 MACD, 신호Line 추가
    stock_df['MACD'] = MACD
    stock_df['signal_Line'] = signal_Line
    stock_df['oscillator'] = MACD - signal_Line
    
    return stock_df

def std_12m(stock_df, column='종가'):
    """
    일별 데이터를 활용하여, 12개월간의 종가 데이터의 표준편차를 활용하여, 각 종목별 변동성 지표 생성
    (1년 영업기준일 : 252)
    Args:
        stock_df(pd.DataFrmae)
        column(str) : default(종가), 종가의 변동성을 활용
    Returns:
        std_12m_value(int) : 각 종목의 12개월간의 변동성 값을 반환
    """
    std_12m_value = np.std(stock_df.loc[-252:, column])
    return std_12m_value