library(httr)
library(rvest)
library(readr)
library(stringr)
library(magrittr)
library(dplyr)
library(readr)


#==================코스피 업종분류 현황 크롤링

gen_otp_url =
  'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_data = list(
  mktId = 'STK',
  trdDd = '20210108',
  money = '1',
  csvxls_isNo = 'false',
  name = 'fileDown',
  url = 'dbms/MDC/STAT/standard/MDCSTAT03901'
)
otp = POST(gen_otp_url, query = gen_otp_data) %>%
  read_html() %>%
  html_text()


down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
down_sector_KS = POST(down_url, query = list(code = otp),
                      add_headers(referer = gen_otp_url)) %>%
  read_html(encoding = 'EUC-KR') %>%
  html_text() %>%
  read_csv()

down_sector_KS





#================= 코스피 개별종목 지표 크롤링

gen_otp_url =
  'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_data = list(
  searchType = '1',
  mktId = 'STK',
  trdDd = '20210108',
  csvxls_isNo = 'false',
  name = 'fileDown',
  url = 'dbms/MDC/STAT/standard/MDCSTAT03501'
)
otp = POST(gen_otp_url, query = gen_otp_data) %>%
  read_html() %>%
  html_text()

down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
down_ind = POST(down_url, query = list(code = otp),
                add_headers(referer = gen_otp_url)) %>%
  read_html(encoding = 'EUC-KR') %>%
  html_text() %>%
  read_csv()

head(down_ind)
write.csv(down_ind, 'data/KOSPI_ind.csv')


#================= 최근 영업일 기준 크롤링
url = 'https://finance.naver.com/sise/sise_deposit.nhn'

biz_day = GET(url) %>%
  read_html(encoding = 'EUC-KR') %>%
  html_nodes(xpath =
               '//*[@id="type_1"]/div/ul[2]/li/span') %>%
  html_text() %>%
  str_match(('[0-9]+.[0-9]+.[0-9]+') ) %>%
  str_replace_all('\\.', '')


# 코스피 업종분류 OTP 발급
gen_otp_url =
  'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_data = list(
  mktId = 'STK',
  trdDd = biz_day, # 최근영업일로 변경
  money = '1',
  csvxls_isNo = 'false',
  name = 'fileDown',
  url = 'dbms/MDC/STAT/standard/MDCSTAT03901'
)
otp = POST(gen_otp_url, query = gen_otp_data) %>%
  read_html() %>%
  html_text()


# 코스피 업종분류 데이터 다운로드
down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
down_sector_KS = POST(down_url, query = list(code = otp),
                      add_headers(referer = gen_otp_url)) %>%
  read_html(encoding = 'EUC-KR') %>%
  html_text() %>%
  read_csv()


# SAVE
ifelse(dir.exists('data'), FALSE, dir.create('data'))
write.csv(down_sector_KS, 'data/KOSPI_sector.csv')

# 개별종목 지표 OTP 발급
gen_otp_url =
  'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
gen_otp_data = list(
  searchType = '1',
  mktId = 'STK',
  trdDd = biz_day, # 최근영업일로 변경
  csvxls_isNo = 'false',
  name = 'fileDown',
  url = 'dbms/MDC/STAT/standard/MDCSTAT03501'
)
otp = POST(gen_otp_url, query = gen_otp_data) %>%
  read_html() %>%
  html_text()

# 개별종목 지표 데이터 다운로드
down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
down_ind = POST(down_url, query = list(code = otp),
                add_headers(referer = gen_otp_url)) %>%
  read_html(encoding = 'EUC-KR') %>%
  html_text() %>%
  read_csv()

write.csv(down_ind, 'data/KOSPI_ind.csv')




#========================= 데이터 정리하기

down_sector = read.csv('data/KOSPI_sector.csv', row.names = 1,
                       stringsAsFactors = FALSE)
down_ind = read.csv('data/KOSPI_ind.csv',  row.names = 1,
                    stringsAsFactors = FALSE)

intersect(names(down_sector), names(down_ind))
setdiff(down_sector[, '종목명'], down_ind[ ,'종목명'])
# 두 데이터프레임의 Column이 동일하지 않은 경우가 많은데, 이를 제외하고 저장


KOSPI_ticker = merge(down_sector, down_ind,
                   by = intersect(names(down_sector),
                                  names(down_ind)),
                   all = FALSE
                    )

KOSPI_ticker[grepl('스팩', KOSPI_ticker[, '종목명']), '종목명']  
KOSPI_ticker[str_sub(KOSPI_ticker[, '종목코드'], -1, -1) != 0, '종목명']


# 스팩주, 우선주 제외됨
KOSPI_ticker = KOSPI_ticker[!grepl('스팩', KOSPI_ticker[, '종목명']), ]  
KOSPI_ticker = KOSPI_ticker[str_sub(KOSPI_ticker[, '종목코드'], -1, -1) == 0, ]

KOSPI_ticker


#========================= 최종적으로 KOSPI ticker저장 => 총 783개의 종목
rownames(KOSPI_ticker) = NULL
write.csv(KOSPI_ticker, 'data/KOSPI_ticker.csv')
