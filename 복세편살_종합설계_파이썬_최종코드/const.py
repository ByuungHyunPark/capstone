import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
from datetime import datetime

kospi_ticker = pd.read_csv('KOSPI_ticker.csv', encoding='EUC-KR', index_col=0)
kospi_ticker['종목코드'] = kospi_ticker['종목코드'].map(lambda x :  '%06d'%x)


def ticker_list_to_name(ticker_list):
    """
    Args:
        ticker_list(list)
    Returns:
    """
    ticker_to_name = kospi_ticker[['종목코드','종목명']].set_index('종목코드').to_dict()['종목명']
    ticker_name_list = [ticker_to_name[i] for i in ticker_list]
    return ticker_name_list




#예시 : 삼성전자(005930)
def plot_to_json(stock_code, section = 'plot', folder_nm=''):
    """
    참고링크 : https://tariat.tistory.com/797
    Args:
        stock_code(str): 6자리의 종목 코드
        section(str)
            |plot| : return 없이 시각화만 그리기
            |save_json| : json으로 반환
    Returns:
        fig.to_json(json) : 시각화 가능한 json파일로 반환
        
    """
    stock_df = pd.read_csv(f'data/KOSPI_price/{stock_code}_price.csv')
    stock_df['날짜'] = pd.to_datetime(stock_df['날짜'].astype(str))
    stock_df = stock_df[stock_df['시가'] > 0] #결측치 제거
    fig = go.Figure(data=[go.Candlestick(x=stock_df['날짜'],
                    open=stock_df['시가'],
                    high=stock_df['고가'],
                    low=stock_df['저가'],
                    close=stock_df['종가'])])

    if section == 'plot':
        display(fig)
    elif section == 'json':
        return fig.to_json()
    elif section == 'html':
        plotly.offline.plot(fig, filename = f'html-result-chart/{folder_nm}/{stock_code}.html', auto_open=False)
        return fig.to_html()