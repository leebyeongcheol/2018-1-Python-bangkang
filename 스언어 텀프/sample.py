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

API_KEY = 'aTIaQ2xH3YX61QqRvQYCrHyJtrpYj7Omi1vFIfUCIzM4908KtnLBetjsGy99joagT9qF6OdjJK1qDsoOA6xKpw%3D%3D'
TOKEN = '619085954:AAG3STV0hdVrgdOQOPxe_semWPecQg4qbWQ'
bot = telepot.Bot(TOKEN)
MAX_MSG_LENGTH = 300


def locName(locParam):
    locname = ('서울', '부산', '순천', '동해',
               '속초', '무안', '양양', '목포',
               '광양', '전주', '인천', '강릉',
               '통영', '하남', '마산', '양평',
               '춘천', '청원', '상주', '평택',
               '제천', '논산', '냉정', '서천',
               '공주', '현풍', '대구')

    loc = ('%EC%84%9C%EC%9A%B8', '%EB%B6%80%EC%82%B0', '%EC%88%9C%EC%B2%9C', '%EB%8F%99%ED%95%B4',
           '%EC%86%8D%EC%B4%88', '%EB%B6%80%EC%82%B0', '%EC%96%91%EC%96%91', '%EB%AA%A9%ED%8F%AC',
           '%EA%B4%91%EC%96%91', '%EC%A0%84%EC%A3%BC', '%EC%9D%B8%EC%B2%9C', '%EA%B0%95%EB%A6%89',
           '%ED%86%B5%EC%98%81', '%ED%95%98%EB%82%A8', '%EB%A7%88%EC%82%B0', '%EC%96%91%ED%8F%89',
           '%EC%B6%98%EC%B2%9C', '%EC%B2%AD%EC%9B%90', '%EC%83%81%EC%A3%BC', '%ED%8F%89%ED%83%9D',
           '%EC%A0%9C%EC%B2%9C', '%EB%85%BC%EC%82%B0', '%EB%83%89%EC%A0%95', '%EC%84%9C%EC%B2%9C',
           '%EA%B3%B5%EC%A3%BC', '%ED%98%84%ED%92%8D', '%EB%8C%80%EA%B5%AC')

    for i in range(len(locname)):
        if (locParam == locname[i]):
            return loc[i]

    return '-1'

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def getData(chat_id,highway, dir):
    direction = locName(dir)

    if (direction != '-1'):
        url = 'http://data.ex.co.kr/exopenapi/business/curStateStation?' \
              'serviceKey=F2FZEsY0DuY88JwtPhY%2FnYIZDUZc3kPo90wd7MwY16EriFZORewjC0MQfGmOelfaLXjgSBOEfGZ6xdhBbt4HPA%3D%3D' \
              '&type=xml' \
              '&direction=' + direction + \
              '&numOfRows=40&pageSize=40&pageNo=1&startPage=1'

        resultXML = urlopen(url)
        result = resultXML.read()

        xmlsoup = BeautifulSoup(result, 'html.parser')

        data = pd.DataFrame()
        dataList = xmlsoup.findAll("list")

        outList = []

        for i in dataList:
            if (i.routename.string == highway):
                temp = pd.DataFrame({"주유소 이름": [i.serviceareaname.string], "고속도로": [i.routename.string],
                                     "디젤": [i.diselprice.string], "가솔린": [i.gasolineprice.string],
                                     "LPG": [i.lpgprice.string], "전화": [i.telno.string]})

                data = pd.concat([data, temp], ignore_index=True)

                outList = [i.serviceareaname.string, i.routename.string, i.diselprice.string,
                            i.gasolineprice.string, i.lpgprice.string, i.telno.string]

                sendMessage(chat_id, outList[0]+'\n'+outList[1]+'\n'+outList[2]+'\n'+outList[3]+'\n'+
                            outList[4]+'\n'+outList[5]+'\n')

        if (len(data)!=0):
            print(data)
        else:
            sendMessage(chat_id, '정보가 없습니다.\n조회 [고속도로명] [방향]을 입력하세요.')


    else:
        sendMessage(chat_id, '정보가 없습니다.\n조회 [고속도로명] [방향]을 입력하세요.')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('조회') and len(args)>1:
        print('try to 조회', args[1], args[2])
        getData(chat_id,args[1], args[2])
    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n조회 [고속도로명] [방향]을 입력하세요.')


bot.message_loop(handle)

print('Listening...')

while 1:
    time.sleep(10)