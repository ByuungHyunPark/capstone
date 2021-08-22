import pandas as pd
import numpy as np
import const

def return_kospi_ticker():
    kospi_ticker_df = pd.read_csv('KOSPI_ticker.csv', encoding='EUC-KR', index_col=0)
    kospi_ticker_df['종목코드'] = kospi_ticker_df['종목코드'].map(lambda x : '%06d'%x)
    return kospi_ticker_df
    
def fs_preperation():
    """
    2017~2020 년도의 재무데이터 병합 (전체 종목별, 237개의 재무데이터 포함)
    fs(Financial Statement)
    Args:
      - 
    Return:
        fs_df(pd.DataFrame) : 재무데이터 2017~2020 병합
    """
    df_2017 = pd.read_csv('data/fs_2017.csv')
    df_2017['ticker'] = df_2017['ticker'].map(lambda x:'%06d'%x)
    df_2017 = df_2017.set_index('ticker')

    df_2018 = pd.read_csv('data/fs_2018.csv')
    df_2018['ticker'] = df_2018['ticker'].map(lambda x:'%06d'%x)
    df_2018 = df_2018.set_index('ticker')

    df_2019 = pd.read_csv('data/fs_2019.csv')
    df_2019['ticker'] = df_2019['ticker'].map(lambda x:'%06d'%x)
    df_2019 = df_2019.set_index('ticker')

    df_2020 = pd.read_csv('data/fs_2020.csv')
    df_2020['ticker'] = df_2020['ticker'].map(lambda x:'%06d'%x)
    df_2020 = df_2020.set_index('ticker')

    fs_df = pd.concat([df_2017, df_2018, df_2019, df_2020], axis=1)

    year_col = [2017]*237 + [2018]*237 + [2019]*237 + [2020]*237
    fs_df.columns = [year_col, list(df_2020.columns) * 4]
    for index_date in [2017, 2018, 2019, 2020]:
        f_score_df = fs_df[(index_date)]
        ROA = fs_df[(index_date, '지배주주순이익')] / fs_df[(index_date, '자산')]
        CFO = fs_df[(index_date, '영업활동으로인한현금흐름')] / fs_df[(index_date, '자산')]
        ACCURUAL = CFO - ROA

        #재무성과
        LEV = fs_df[(index_date, '장기차입금')] / fs_df[(index_date, '자산')]
        LIQ = fs_df[(index_date, '유동자산')] / fs_df[(index_date, '유동부채')]
        OFFER = fs_df[(index_date, '유상증자')]

        # 운영 효율성
        MARGIN = fs_df[(index_date, '매출총이익')] / fs_df[(index_date, '매출액')]
        TURN = fs_df[(index_date, '매출액')] / fs_df[(index_date, '자산')]

        fs_df[(index_date,'ROA')] = ROA
        fs_df[(index_date,'CFO')] = CFO
        fs_df[(index_date,'ACCURUAL')] = ACCURUAL
        fs_df[(index_date,'LEV')] = LEV
        fs_df[(index_date,'LIQ')] = LIQ
        fs_df[(index_date,'OFFER')] = OFFER
        fs_df[(index_date,'MARGIN')] = MARGIN
        fs_df[(index_date,'TURN')] = TURN
    return fs_df


def invest_preperation():
    """
    2017~2020 년도의 PBR, PCR, PER, PSR 가치지표 생성
    
    Return : 
        invest_df(pd.DataFrame) : 가치지표 데이터 결합
    """
    invest_2017 = pd.read_csv('data/KOSPI_value_2017.csv')
    invest_2017['ticker'] = invest_2017['ticker'].map(lambda x : '%06d'%x)
    invest_2017 = invest_2017.set_index('ticker')

    invest_2018 = pd.read_csv('data/KOSPI_value_2018.csv')
    invest_2018['ticker'] = invest_2018['ticker'].map(lambda x : '%06d'%x)
    invest_2018 = invest_2018.set_index('ticker')

    invest_2019 = pd.read_csv('data/KOSPI_value_2019.csv')
    invest_2019['ticker'] = invest_2019['ticker'].map(lambda x : '%06d'%x)
    invest_2019 = invest_2019.set_index('ticker')

    invest_2020 = pd.read_csv('data/KOSPI_value_2020.csv')
    invest_2020['ticker'] = invest_2020['ticker'].map(lambda x : '%06d'%x)
    invest_2020 = invest_2020.set_index('ticker')

    invest_df = pd.concat([invest_2017,
                           invest_2018, 
                           invest_2019,
                           invest_2020
                        ], axis = 1)

    year_col = [2017]*4 + [2018]*4 + [2019]*4 + [2020]*4
    invest_df.columns = [year_col, ['PBR','PCR','PER','PSR'] * 4]

    return invest_df


def return_price_df():
    """
    2017년부터의 종가데이터만 Return
    index : 날짜
    Column : 종목코드(digit6)
    """
    price_df = pd.read_csv('data/KOSPI_price.csv', index_col=0)
    price_df['종목코드'] = price_df['종목코드'].map(lambda x : '%06d'%x)
    price_df = price_df[['날짜','종목코드','종가']]
    price_df['날짜'] = pd.to_datetime(price_df['날짜'].astype(str))
    price_df = pd.pivot_table(data = price_df, index='날짜', columns='종목코드')['종가']
    return price_df