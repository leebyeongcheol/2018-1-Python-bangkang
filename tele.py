# coding=utf-8

import sys
import telepot
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import webbrowser
import traceback
import time
import spam

API_KEY = 'yFY%2BS0tRfVUf8ol%2FUjDARwS71qiyeewzzn7w%2Bv9JEQDV%2FmlRIbfelfcqdu5iTMyIWALgQ4GuFnmxtepshr7maw%3D%3D'
TOKEN = '495825663:AAGLpyWUPwDO89RLbI-I-Tv63DzGYAGMozE'
bot = telepot.Bot(TOKEN)
MAX_MSG_LENGTH = 300


def locName(locParam):
    locname = ('서울', '부산', '대구', '인천',
               '광주', '대전', '울산', '경기',
               '강원', '충북', '충남', '전북',
               '전남', '경북', '경남', '제주',
               '세종')

    loc = ('%EC%84%9C%EC%9A%B8', '%EB%B6%80%EC%82%B0', '%EB%8C%80%EA%B5%AC', '%EC%9D%B8%EC%B2%9C',
           '%EA%B4%91%EC%A3%BC', '%EB%8C%80%EC%A0%84', '%EC%9A%B8%EC%82%B0', '%EA%B2%BD%EA%B8%B0',
           '%EA%B0%95%EC%9B%90', '%EC%A0%84%EC%A3%BC', '%EC%9D%B8%EC%B2%9C', '%EA%B0%95%EB%A6%89',
           '%EC%A0%84%EB%82%A8', '%EA%B2%BD%EB%B6%81', '%EA%B2%BD%EB%82%A8', '%EC%A0%9C%EC%A3%BC',
           '%EC%84%B8%EC%A2%85')

    for i in range(len(locname)):
        #print(spam.strlen("test"))
        if (locParam == locname[i]):
            return loc[i]

    return '-1'

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def getData(chat_id,station):
    stationname = locName(station)

    if (stationname != '-1'):
        url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?' \
              'serviceKey=yFY%2BS0tRfVUf8ol%2FUjDARwS71qiyeewzzn7w%2Bv9JEQDV%2FmlRIbfelfcqdu5iTMyIWALgQ4GuFnmxtepshr7maw%3D%3D' \
              '&numOfRows=40&pageSize=40&pageNo=1&startPage=1'\
              '&sidoName='+stationname+'&searchCondition=HOUR'

        resultXML = urlopen(url)
        result = resultXML.read()

        xmlsoup = BeautifulSoup(result, 'html.parser')

        data = pd.DataFrame()
        dataList = xmlsoup.findAll("item")

        #print(dataList)
        outList = []

        for i in dataList:
            temp = pd.DataFrame({"시간기준 ": [i.datatime.string], "시/군/구": [i.cityname.string],
                                 "PM10": [i.pm10value.string + "㎍/m³"], "PM2.5": [i.pm25value.string+ "㎍/m³"]})

            data = pd.concat([data, temp], ignore_index=True)

            outList = [i.datatime.string, i.cityname.string, i.pm10value.string,
                       i.pm25value.string]
            print(outList)

            sendMessage(chat_id, '시간기준 : '+outList[0]+'\n'+'시/군/구 : '+outList[1]+'\n'+'PM1.0 : '+outList[2]+'㎍/m³'+'\n'+'PM2.5 : '+outList[3]+'㎍/m³'+'\n')

        if (len(data)!=0):
            sendMessage(chat_id, '병철이')
            print(data)
        else:
            sendMessage(chat_id, '정보가 없습니다.\n조회 [시/도이름]을 입력하세요.')
    else:
        sendMessage(chat_id, '정보가 없습니다.\n조회 [시/도이름]을 입력하세요.')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('조회') and len(args)>1:
        print('try to 조회', args[1])
        getData(chat_id,args[1])
    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n조회 [도이름]을 입력하세요.')


bot.message_loop(handle)

#print('Listening...')

while 1:
    time.sleep(10)