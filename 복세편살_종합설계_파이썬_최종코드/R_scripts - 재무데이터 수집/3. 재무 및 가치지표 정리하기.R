library(stringr)
library(httr)
library(rvest)
library(readr)
library(stringr)
library(magrittr)
library(dplyr)

#==========1. 재무제표 수집 데이터 정리하기
KOSPI_ticker = read.csv('data/KOSPI_ticker.csv', row.names = 1)
KOSPI_ticker$'종목코드' =
  str_pad(KOSPI_ticker$'종목코드', 6, side = c('left'), pad = '0')

data_fs = list()

for (i in 1 : nrow(KOSPI_ticker)){
  
  name = KOSPI_ticker[i, '종목코드']
  data_fs[[i]] = read.csv(paste0('data/KOSPI_fs/', name,
                                 '_fs.csv'), row.names = 1)
}

#삼성전자는 237개의 재무제표 데이터 보유중..
fs_item = data_fs[[1]] %>% rownames()
length(fs_item)


fs_list = list()

for (i in 1 : length(fs_item)) {
  select_fs = lapply(data_fs, function(x) {
    # 해당 항목이 있을시 데이터를 선택
    if ( fs_item[i] %in% rownames(x) ) {
      x[which(rownames(x) == fs_item[i]), ]
      
      # 해당 항목이 존재하지 않을 시, NA로 된 데이터프레임 생성
    } else {
      data.frame(NA)
    }
  })
  
  # 리스트 데이터를 행으로 묶어줌 
  select_fs = bind_rows(select_fs)
  
  # 열이름이 '.' 혹은 'NA.'인 지점은 삭제 (NA 데이터)
  select_fs = select_fs[!colnames(select_fs) %in%
                          c('.', 'NA.')]
  
  # 연도 순별로 정리
  select_fs = select_fs[, order(names(select_fs))]
  
  # 행이름을 티커로 변경
  rownames(select_fs) = KOSPI_ticker[, '종목코드']
  
  # 리스트에 최종 저장
  fs_list[[i]] = select_fs
  
}

# 리스트 이름을 재무 항목으로 변경
names(fs_list) = fs_item


# fs_list에 237개의 list생성되는데, Rds파일로 저장하여 추후 활용
saveRDS(fs_list, 'data/KOSPI_fs.Rds')













#======================== 2. 가치지표 정리하기
KOSPI_ticker = read.csv('data/KOSPI_ticker.csv', row.names = 1)
KOSPI_ticker$'종목코드' =
  str_pad(KOSPI_ticker$'종목코드', 6, side = c('left'), pad = '0')

data_value = list()

for (i in 1 : nrow(KOSPI_ticker)){
  
  name = KOSPI_ticker[i, '종목코드']
  data_value[[i]] =
    read.csv(paste0('data/KOSPI_value/', name,
                    '_value.csv'), row.names = 1) %>%
    t() %>% data.frame()
  
}


data_value = bind_rows(data_value)
print(head(data_value))



data_value = data_value[colnames(data_value) %in%
                          c('PER', 'PBR', 'PCR', 'PSR')]

data_value = data_value %>%
  mutate_all(list(~na_if(., Inf)))

rownames(data_value) = KOSPI_ticker[, '종목코드']
print(head(data_value))



write.csv(data_value, 'data/KOSPI_value.csv')
