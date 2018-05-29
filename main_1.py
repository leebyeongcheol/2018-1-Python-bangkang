from xml.dom.minidom import *
import urllib.request
import base64
from tkinter import *
from tkinter import font
import  tkinter.messagebox

g_Tk = Tk()
g_Tk.geometry("400x600+750+200")

myServerKey = "1EV5%2F0ZUld5RHLecMPsw127dsW%2B6rsTJ38ep3vOR8lr6%2BEP37QjoJ7UySPDFNcyQq67lWLPlRMZEj1KSHGe%2F0g%3D%3D"
myLocationBoxData = "서울"

def LoadXML():
    #serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?ServiceKey="
    serverurl = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?serviceKey="
    #servervalue = "&sidoName=" + urlencode(self.LocationBoxData) + "&numOfRows=999&pageSize=999&pageNo=1&startPage=1"
    servervalue = "&numOfRows=999&pageSize=999&pageNo=1&startPage=1&sidoName=" + urlencode(myLocationBoxData) + "&searchCondition=HOUR"
    areaData = openAPItoXML(serverurl, myServerKey, servervalue)

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
    TempFont = font.Font(g_Tk, size=20, weight = 'bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[시군구별 실시간 평균조회]")
    MainText.pack()
    MainText.place(x=20)

def InitSearchListBox():
    global SearchListBox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=150, y=50)

    TempFont = font.Font(g_Tk, size=20, weight='bold', family='Consoal')
    SearchListBox = Listbox(g_Tk, font=TempFont,
                            activestyle='none'
                            ,width=10,height=1,borderwidth=12,
                            relief='ridge'
                            ,yscrollcommand=ListBoxScrollbar.set)

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
    SearchListBox.place(x=10,y=50)
    ListBoxScrollbar.config(command=SearchListBox.yview)

#def InitInputLabel():
    #global  InputLabel
    #TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    #InputLabel = Entry(g_Tk, font = TempFont, width = 26, borderwidth = 12, relief = 'ridge')
    #InputLabel.pack()
    #InputLabel.place(x=10, y=105)

#def InitSearchButton():
    #TempFont = font.Font(g_Tk, size=12, weight='bold', family='Consolas')
    #SearchButton = Button(g_Tk, font = TempFont, text = "검색", command = SearchButtonAction)
    #SearchButton.pack()
    #SearchButton.place(x=330, y=110)

#def SearchButtonAction():
    #global SearchListBox

    #RenderText.configure(state='normal')
    #RenderText.delete(0.0, END)
    #iSearchIndex = SearchListBox.curselection()[0]
    #if iSearchIndex == 0 : LoadXML()
    #elif iSearchIndex == 1 : pass


InitTopText()
InitSearchListBox()
#InitInputLabel()
#InitSearchButton()
#InitRenderText()
#InitSendEmailButton()
#InitSortListBox()
#InitSortButton()


LoadXML()
g_Tk.mainloop()