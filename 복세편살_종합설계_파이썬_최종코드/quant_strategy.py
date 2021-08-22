import pandas as pd
import numpy as np
import const
from data_preperation import return_kospi_ticker
import FinanceDataReader as fdr
import matplotlib.pyplot as plt

KOSPI_ticker = return_kospi_ticker()

def get_fscore(fs_df, index_date, num):
    """
    Args:
        fs_df(pd.DataFrame) : 2017~2020 재무데이터
        index_date(int) :  연도 설정으로, 2017|2018|2019|2020 
        num(int) : 추천하고싶은 상위 종목의 개수
    Returns: 
        f_score_df(pd.DataFrame) : 상위 n개의 F-score를 갖는 값 출력
    """
    #수익성
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
    
    F_1 = ROA > 0
    F_2 = CFO > 0
    try:
        F_3 = (ROA - (fs_df[(index_date-1, '지배주주순이익')] / fs_df[(index_date-1, '자산')])) > 0
    except:
        #과거데이터 존재하지 않음
        F_3 = 0
    F_4 = ACCURUAL > 0
    try:
        F_5 = (LEV - (fs_df[(index_date-1, '장기차입금')] / fs_df[(index_date-1, '자산')])) <= 0 
    except:
        F_5 = 0
    try:
        F_6 = (LIQ - (fs_df[(index_date-1, '유동자산')] / fs_df[(index_date-1, '유동부채')])) > 0
    except:
        F_6 = 0
    F_7 = (OFFER <= 0) | OFFER.isna()
    try:
        F_8 = (MARGIN - (fs_df[(index_date-1, '매출총이익')] / fs_df[(index_date-1, '매출액')])) > 0
    except:
        F_8 = 0
    try:
        F_9 = (TURN - (fs_df[(index_date-1, '매출액')] / fs_df[(index_date-1, '자산')])) > 0
    except:
        F_9 = 0
        
    f_score_df['F_score'] = sum([F_1,F_2,F_3,F_4,F_5,F_6,F_7,F_8,F_9])
    f_score_df = f_score_df.sort_values(by='F_score', ascending=False)
    return f_score_df[:num]



#  complete 1 - PER기준으로 오름차순으로 정렬하여 주는 함수 
def low_per(invest_df, index_date, num):
    """
    ex) low_per(invest_df, 2018, 10)
    """
    per_sorted = invest_df[(index_date)].sort_values(by='PER')
    return per_sorted[:num]


# complete2 - high-roa
def high_roa(fs_df, index_date, num):
    """
    ex) high_roa(fs_df, index_data)
    """
    fs_df[(index_date, 'ROA')] = fs_df[(index_date, 'ROA')]
    fs_df[(index_date, 'ROA')] = pd.to_numeric(fs_df[(index_date, 'ROA')] )
    sorted_roa = fs_df.sort_values(by=(index_date, 'ROA'), ascending=False)
    return sorted_roa[index_date][:num]

# 마법공식 - PER, ROA
def magic_formula(fs_df, invest_df, index_date, num):
    """
    ex)magic_formula(fs_df, invest_df, 2019, 20)
    """
    per = low_per(invest_df, index_date, None)
    roa = high_roa(fs_df, index_date, None)
    per['per순위'] = per['PER'].rank()
    roa['roa순위'] = roa['ROA'].rank(ascending=False)
    magic = pd.merge(per, roa, how='outer', left_index=True, right_index=True)
    magic['마법공식 순위'] = (magic['per순위'] + magic['roa순위']).rank().sort_values()
    magic = magic.sort_values(by='마법공식 순위')
    magic = pd.merge(magic, KOSPI_ticker[['종목코드','업종명']], left_on='ticker', right_on='종목코드')
    magic.loc[:, 'stock_name'] = const.ticker_list_to_name(magic['종목코드'])
    magic = magic.loc[~magic['업종명'].isin(['기타금융','증권','보험','증권','은행']), :]

    return magic[:num]


def get_value_rank(invest_df, value_type, index_date, num):
    """
    ex) get_value_rank(invest_df, 'PER', 2018, 10)
    """
    invest_df[(index_date,  value_type)] = pd.to_numeric(invest_df[(index_date,  value_type)])
    value_sorted = invest_df.sort_values(by=(index_date,  value_type))[index_date]
    value_sorted[  value_type + '순위'] = value_sorted[value_type].rank()
    return value_sorted[[value_type, value_type + '순위']][:num]



def make_value_combo(value_list, invest_df, index_date, num):
    """
    ex) make_value_combo(['PER','PBR','PSR'], invest_df, 2018, 10) 
    """
    for i, value in enumerate(value_list):
        temp_df = get_value_rank(invest_df, value, index_date, None)
        if i == 0:
            value_combo_df = temp_df
            rank_combo = temp_df[value + '순위']
        else:
            value_combo_df = pd.merge(value_combo_df, temp_df, how='outer', left_index=True, right_index=True)
            rank_combo = rank_combo + temp_df[value + '순위']
    
    value_combo_df['종합순위'] = rank_combo.rank()
    value_combo_df = value_combo_df.sort_values(by='종합순위')
    
    return value_combo_df[:num]



def get_momentum_rank(price_df, index_date, num):
    """
    ex) get_momentum_rank(price_df, '2018-02-01', 252, 10)
    Args:
        index_date : 특정 날짜를 입력
        date_range : 수익률 계산 시점 (1년단위 수익률은 보통 252일)
    """
    momentum_df = pd.DataFrame(price_df.pct_change(252).loc[index_date])
    momentum_df.columns = ['모멘텀']
    momentum_df['모멘텀순위'] = momentum_df['모멘텀'].rank(ascending=False)
    momentum_df = momentum_df.sort_values(by='모멘텀순위')
    return momentum_df[:num]


def get_value_quality(invest_df, fs_df, index_date, num):
    """
    ex) get_value_quality(invest_df, fs_df, 2019, 10)
    """
    value = make_value_combo(['PER', 'PBR', 'PSR', 'PCR'], invest_df, index_date, None)
    quality = get_fscore(fs_df, index_date, None)
    value_quality = pd.merge(value, quality, how='outer', left_index=True, right_index=True)
    value_quality_filtered = value_quality.sort_values(by='F_score')
    vq_df = value_quality_filtered.sort_values(by='종합순위')
    return vq_df[:num]


def backtest_beta(price_df, strategy_df, start_date, N, section='df'):
    
    """
    Args:
        price_df(pd.DataFrame)
        strategy_df(pd.DataFrame) : 특정 전략을 통해 나온 종목 DataFrame
        start_date(int) : 연도 2017|2018|2019|2020
        section(str) : 
            |df| : return 추천 종목DataFrame
            |plot| : return 추천된 종목들의 코스피와 비교한 수익률
    """
    kospi_index = fdr.DataReader('KS11', start = str(start_date)+'-12', end=str(start_date+1)+'-12')
    ((kospi_index['Close'] / kospi_index['Close'].values[0]) - 1).plot(label='KOSPI_INDEX')
    initial_money = kospi_index['Close'].values[0] * 1000000
    try:
        strategy_df['종목명'] = const.ticker_list_to_name(strategy_df.index)
    except:
        strategy_df['종목명'] = const.ticker_list_to_name(strategy_df['code'])
    display(strategy_df)


    code_list = strategy_df.index
    
    if 0 in code_list:
        code_list = strategy_df['code']

    if start_date==2020:
        strategy_df['1년 수익률'] = price_df[code_list][str(start_date)+'-12':str(start_date+1)+'-06'].pct_change(periods=120).iloc[-1,:]
    else:
        strategy_df['1년 수익률'] = price_df[code_list][str(start_date)+'-12':str(start_date+1)+'-11'].pct_change(periods=240).iloc[-1,:]


    strategy_price = price_df[code_list][str(start_date)+'-12':str(start_date+1)+'-11']

    pf_stock_num = {}
    stock_amount = 0
    stock_pf = 0
    each_money = initial_money / len(strategy_df)
    strategy_price = strategy_price.dropna(axis=1)
    for code in strategy_price.columns:
        temp = int( each_money / strategy_price[code][0] )
        pf_stock_num[code] = temp
        stock_amount = stock_amount + temp * strategy_price[code][0]
        stock_pf = stock_pf + strategy_price[code] * pf_stock_num[code]

    cash_amount = initial_money - stock_amount

    backtest_df = pd.DataFrame({'주식포트폴리오':stock_pf})
    backtest_df['현금포트폴리오'] = [cash_amount] * len(backtest_df)
    backtest_df['종합포트폴리오'] = backtest_df['주식포트폴리오'] + backtest_df['현금포트폴리오']
    backtest_df['일변화율'] = backtest_df['종합포트폴리오'].pct_change()
    backtest_df['총변화율'] = backtest_df['종합포트폴리오']/initial_money - 1
    
    backtest_df['총변화율'].plot(label='Strategy')
    
    plt.xlabel('date')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    if section=='plot':
        return plt
    
    else:
        return backtest_df