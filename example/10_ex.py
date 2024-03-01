import requests as rq
from bs4 import BeautifulSoup
import re

from io import BytesIO
import pandas as pd

# 10-1_ex_01
url = "https://finance.naver.com/sise/sise_deposit.nhn"
data = rq.get(url)
data_html = BeautifulSoup(data.content)
parse_day = data_html.select_one(
    "div.subtop_sise_graph2 > ul.subtop_chart_note > li > span.tah"
).text

print("paras_data : ", parse_day)

# 10-1_ex_02
biz_day = re.findall("[0-9]+", parse_day)
biz_day = "".join(biz_day)

print("biz_day : ", biz_day)


# 10-2_ex_01
gen_otp_url = "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
gen_otp_stk = {
    "locale": "ko_KR",
    "mktId": "STK",
    "trdDd": biz_day,
    "money": "1",
    "csvxls_isNo": "false",
    "name": "fileDown",
    "url": "dbms/MDC/STAT/standard/MDCSTAT03901",
}

headers = {"Referer": "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader"}
otp_stk = rq.post(gen_otp_url, gen_otp_stk, headers=headers).text

print("otp_stk : ", otp_stk)


# 10-2_ex_02
down_url = "http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"
down_sector_stk = rq.post(down_url, {"code": otp_stk}, headers=headers)
# print(down_sector_stk.content)

# print(BytesIO(down_sector_stk.content))
sector_stk = pd.read_csv(BytesIO(down_sector_stk.content), encoding="EUC-KR")

print(sector_stk.head())


# 10-2_ex_03
gen_otp_ksq = {
    "locale": "ko_KR",
    "mktId": "KSQ",
    "trdDd": biz_day,
    "money": "1",
    "csvxls_isNo": "false",
    "name": "fileDown",
    "url": "dbms/MDC/STAT/standard/MDCSTAT03901",
}

otp_ksq = rq.post(gen_otp_url, gen_otp_ksq, headers=headers).text

down_sector_ksq = rq.post(down_url, {"code": otp_ksq}, headers=headers)
sector_ksq = pd.read_csv(BytesIO(down_sector_ksq.content), encoding="EUC-KR")

print(sector_ksq.head())
