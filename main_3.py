from xml.dom.minidom import *
import urllib.request
import base64
from tkinter import *
from tkinter import font
import tkinter.messagebox
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import spam

g_Tk = Tk()
g_Tk.geometry("750x500+750+200")
DataList = []

myServerKey = "1EV5%2F0ZUld5RHLecMPsw127dsW%2B6rsTJ38ep3vOR8lr6%2BEP37QjoJ7UySPDFNcyQq67lWLPlRMZEj1KSHGe%2F0g%3D%3D"
#myLocationBoxData = ['서울','부산','대구','인천','광주','대전','울산','경기','강원','충북','충남','전북','경북','경남','제주','세종']
myLocationBoxData = "0"

def LoadXML():
    #serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?ServiceKey="
    serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey="
    #servervalue = "&sidoName=" + urlencode(self.LocationBoxData) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
    servervalue = "&numOfRows=999&pageSize=999&pageNo=1&startPage=1&sidoName=" + urlencode(myLocationBoxData) + "&searchCondition=HOUR"
    areaData = openAPItoXML(serverurl, myServerKey, servervalue)
    #t1 = print(getPasingData(areaData,"item"))

def Base64_Encode(s):
    return base64.b64encode(s.encode('utf-8'))

def Base64_Decode(b):
    return base64.b64decode(b).decode('utf-8')

def urlencode(string):
    # URL 인코딩
    return urllib.parse.quote(string)

def urldecode(string):
    # URL 디코딩
    return urllib.parse.quote(string)

def openAPItoXML(server, key, value):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    # ↑ User-Agent를 입력하지 않을경우 naver.com 에서 정상적인 접근이 아닌것으로 판단하여 차단을 한다.
    data = ""
    urldata = server + key + value
    with opener.open(urldata) as f:
        data = f.read(300000).decode('utf-8') # 300000bytes 를 utf-8로 변환하여 읽어온다.  변환이 없을경우 unicode로 받아온다.
    return data

def getPasingData(xmlData, motherData):
    doc = parseString(xmlData)
    cityList = doc.getElementsByTagName(motherData)
    citySize = len(cityList)
    list = []
    global Contentdata
    Contentdata = ""

    for index in range(citySize):
        mphms = cityList[index].getElementsByTagName("dataTime")
        list.append(str("시간기준 : "+ mphms[0].firstChild.data))
        Contentdata += str("시간기준 : "+ mphms[0].firstChild.data) + str("\n")

        mphms = cityList[index].getElementsByTagName("cityName")
        list.append(str("시/군/구 : " + mphms[0].firstChild.data))
        Contentdata += str("시/군/구 : " + mphms[0].firstChild.data) + str("\n")

        mphms = cityList[index].getElementsByTagName("pm10Value")
        list.append(str("PM10 : " + mphms[0].firstChild.data) + "㎍/m³")
        Contentdata += str("PM10 : " + mphms[0].firstChild.data + "㎍/m³") + str("\n")

        mphms = cityList[index].getElementsByTagName("pm25Value")
        list.append(str("PM2.5 : " + mphms[0].firstChild.data + "㎍/m³" + "\n"))
        Contentdata += str("PM2.5 : " + mphms[0].firstChild.data + "㎍/m³") + str("\n\n")


    return list

def addParsingDicList(xmlData, motherData, childData):
    # 파싱된 데이터를 리스트에 넣어서 리턴 한다.
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    siGunGuCdSize = len(siGunGuList)
    list = []
    for index in range(siGunGuCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        list.append(str(mphms[0].firstChild.data))
    return list

def addParsingDataString(xmlData, motherData, childData):
    # 파싱된 데이터를 string 형태로 리턴 한다.
    doc = parseString(xmlData)
    siGunGuList = doc.getElementsByTagName(motherData)
    siGunGuCdSize = len(siGunGuList)
    for index in range(siGunGuCdSize):
        mphms = siGunGuList[index].getElementsByTagName(childData)
        if childData == "imageUrl1":
            return str(mphms[1].firstChild.data)
        else:
            return str(mphms[0].firstChild.data)

def InitTopText():
    TempFont = font.Font(g_Tk, size=18, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="미세먼지 시군구별 실시간 조회")
    MainText.pack()
    MainText.place(x=130)


def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=125, y=50)

    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    SearchListBox = Listbox(g_Tk, font=TempFont,
                            activestyle='none',
                            width = 8, height = 1, borderwidth = 12,
                            relief = 'ridge',
                            yscrollcommand = ListBoxScrollbar.set)

    SearchListBox.insert(1, "서울")
    SearchListBox.insert(2, "부산")
    SearchListBox.insert(3, "대구")
    SearchListBox.insert(4, "인천")
    SearchListBox.insert(5, "광주")
    SearchListBox.insert(6, "대전")
    SearchListBox.insert(7, "울산")
    SearchListBox.insert(8, "경기")
    SearchListBox.insert(9, "강원")
    SearchListBox.insert(10, "충북")
    SearchListBox.insert(11, "충남")
    SearchListBox.insert(12, "전북")
    SearchListBox.insert(13, "전남")
    SearchListBox.insert(14, "경북")
    SearchListBox.insert(15, "경남")
    SearchListBox.insert(16, "제주")
    SearchListBox.insert(17, "세종")
    SearchListBox.pack()
    SearchListBox.place(x=10, y=50)
    ListBoxScrollbar.config(command=SearchListBox.yview)


def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    InputLabel = Entry(g_Tk, font=TempFont, width=10, borderwidth=12, relief='ridge')
    InputLabel.pack()
    InputLabel.place(x=150, y=50)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=18, weight='bold', family='Consolas')
    SearchButton = Button(g_Tk, font=TempFont, text="검색", command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=290, y=50)


def SearchButtonAction():
    global InputLabel
    global SearchListBox
    global myLocationBoxData
    myLocationBoxData = str(InputLabel.get())
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    #iSearchIndex = SearchListBox.curselection()[0]
    #iSearchIndex = SearchListBox.curselection()[0]
    SearchLibrary()
    RenderText.configure(state='disabled')



def SearchLibrary():
    serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey="
    servervalue = "&numOfRows=999&pageSize=999&pageNo=1&startPage=1&sidoName=" + urlencode(myLocationBoxData) + "&searchCondition=HOUR"
    areaData = openAPItoXML(serverurl, myServerKey, servervalue)
    req = (getPasingData(areaData, "item"))

    for item in req:
        RenderText.insert(INSERT, item)
        print(item)
        RenderText.insert(INSERT, "\n")


def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=50)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=45, height=24, borderwidth=12,
                      relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=150)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')


def InitEmailText():
    TempFont = font.Font(g_Tk, size=11, weight='bold', family='Consolas')
    MainText = Label(g_Tk, font=TempFont, text="E-Mail\nAddress")
    MainText.pack()
    MainText.place(x=10,y =105)

def InitSendEmailLabel():
    global EmailLabel
    TempFont = font.Font(g_Tk, size=10, weight='bold', family='Consolas')
    EmailLabel = Entry(g_Tk, font=TempFont, width=26, borderwidth=12, relief='ridge')
    EmailLabel.pack()
    EmailLabel.place(x=80, y=105)

def InitSendEmailButton():
    TempFont = font.Font(g_Tk, size=18, weight='bold', family='Consolas')
    MailButton = Button(g_Tk, font=TempFont, text="전송", command=SendEmailButtonAction)
    MailButton.pack()
    MailButton.place(x=290, y=100)

def SendEmailButtonAction():
    global EmailLabel
    global SearchListBox
    global myLocationBoxData
    global Contentdata
    Mailadd = str(EmailLabel.get())
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    #iSearchIndex = SearchListBox.curselection()[0]
    #iSearchIndex = SearchListBox.curselection()[0]
    #SearchLibrary()
    sendMail(Mailadd, "실시간 미세먼지 오염도 정보", Contentdata)
    RenderText.configure(state='disabled')


def sendMail(ReviceMail, Subject, Content):
    s = smtplib.SMTP("smtp.gmail.com",587) #SMTP 서버 설정
    s.starttls() #STARTTLS 시작
    s.login( Base64_Decode(spam.getemail()),Base64_Decode("ZWhvd2wxMjM="))
    contents = Content
    msg = MIMEText(contents, _charset='euc-kr')
    msg['Subject'] = Subject
    msg['From'] = Base64_Decode(spam.getemail())
    msg['To'] = ReviceMail
    s.sendmail( Base64_Decode(spam.getemail()) , ReviceMail, msg.as_string())



InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
SearchLibrary()

InitEmailText()
InitSendEmailButton()
InitSendEmailLabel()
#InitSortListBox()
#InitSortButton()

LoadXML()

g_Tk.mainloop()