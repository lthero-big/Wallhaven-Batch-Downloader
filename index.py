import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from random import choice
import threading
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from bs4 import BeautifulSoup

headers = {
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'same-origin',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4389.90 Safari/531.36'
    ,
    'Cookie': '_pk_id.1.01b8=77a4ffbc245ad3f3.1627430491.; _pk_ses.1.01b8=1; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IldDOVJSOFM3RitkSWptVDk1VVVLNEE9PSIsInZhbHVlIjoiR3F4MElyU2w5ek1WaFRoWkN6VWRTSktxSWJGMFlJbTZObnBlV0xvV1o2XC96WGRyY1JoOUxUeFwvOTZ2a2VWNXNoRE5LdXd3SlFCd3E1Y2xRZEtUaitqeDcrNVordUxDUmJZZUFkU3NocDh3aHBrbGV4SHBWck1PeVMxY2FIWEV2YzVxMVwvclVmQmNYdW1SdmRyT294MjFRT2tlUngySkdzd0V5eWlmTTBBYXpcLzBaS0xJTTZhcUVGSk5XZEtsbEc3VCIsIm1hYyI6ImE5ZmEyNWY1ZTc2ODIyYjk0OWUwZmNmYjBiZjQ1YzA4NDVhMzc5YjY4NWEyMDEyOGMxYTVjZDJkYjFiODIyMzMifQ%3D%3D; XSRF-TOKEN=eyJpdiI6Ikw2ZnN1dlErT0dGOEpRaTRLdUN3WHc9PSIsInZhbHVlIjoiNzd4c2xJQzNiTkJ0VHp4K0QrUm4yNU56Y2xWN1F4SGRpRXYyR0NVcGpGOEFZTGRIVTFndzVZMndTdDloVmtIRSIsIm1hYyI6IjE1Yjc5N2E5ODdjZjBkMjQxM2Y5MGE5OTU5MGQxMzMyOTY0ZmVhNWE4YzVhMjc3OWU4Zjk3ZThkYmY2ZTA1NmYifQ%3D%3D; wallhaven_session=eyJpdiI6ImRLVHRvMXpYVURIN0FsT1pNZFlicWc9PSIsInZhbHVlIjoia0REOWFZODZLYjhCUW1ETjEwSk9vMCtHajVXM3BSemVFaHcrU0hoZHJEVVNsYm1FalRobkJZRkE1YkhVWldaRyIsIm1hYyI6ImMyM2NiNWNjZGFhMGMyNzU0ZTRkMDNhZDFlM2IwMmNhNzFhODM4Zjk2OGE2ZGRiZDUyZmMwZGIzNDM0YTA0OTEifQ%3D%3D'}

class myThread(threading.Thread):
    def __init__(self, page, num, file_name, form):
        threading.Thread.__init__(self)
        self.form = form
        self.page = page
        self.num = num
        self.file_path = file_name

    def run(self):
        try:
            start=int(self.page[-1])
            url = [self.page]
            if int(self.num) >= 2:
                url.append(self.page)
                for i in range(start, int(self.num) + 1):
                    url.append(self.page[0:-1] + str(i))
            collection = []
            for x in url:
                content = open_url(x)
                soup = BeautifulSoup(content, 'lxml')
                images = soup.find('section', class_="thumb-listing-page")
                for li in images.find_all('li'):
                    string = str(li.a['href'])
                    collection.append(string)
            cent = 0
            threadings = []
            for i in collection:
                ui.set_down_nums('已经下载 ' + str(cent) + ' 张')
                name = i.split('/')[-1]
                each_url = 'https://w.wallhaven.cc/full/%s/wallhaven-%s.jpg' % (name[0:2], name)
                html = requests.head(each_url)
                res = html.status_code
                flag = 0
                if res == 404:
                    each_url = each_url[0:-3] + 'png'
                    flag = 1
                t=threading.Thread(target=download, args=(each_url, name, self.file_path, flag))
                cent += 1
                threadings.append(t)
                t.start()
            for x in threadings:
                x.join()
        except:
            return


def download(url, name, file_path, flag):
    fix_file_name = '%s/%s.jpg' % (file_path, name)
    if flag == 1:
        fix_file_name = '%s/%s.png' % (file_path, name)
    with open(fix_file_name, 'wb') as f:
        img = requests.get(url, headers=headers).content
        f.write(img)

def open_url(url):
    list_ip = ['61.145.212.31', '59.124.224.180', '117.26.41.218', '183.6.183.35', '117.65.47.142']
    proxy = choice(list_ip)
    proxies = {
        "http": "http://{}".format(proxy), "https": "https://{}".format(proxy)
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    return html


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(794, 497)
        self.mesb = QMessageBox
        #类型动漫。。
        self.mark = [1, 1, 0]
        #SFW
        self.mark_2=[1,1,0]
        self.file = ''

        #date_added按时间
        self.sorting='toplist'
        self.topRange='1M'
        self.categories = '110'
        self.purity='110'
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Button_start = QtWidgets.QPushButton(Form)
        self.Button_start.setGeometry(QtCore.QRect(510, 50, 169, 61))
        self.Button_start.setFont(font)
        self.Button_start.setObjectName("Button_start")
        self.Button_start.clicked.connect(lambda: self.start(Form))


        self.Button_choose_file = QtWidgets.QPushButton(Form)
        self.Button_choose_file.setGeometry(QtCore.QRect(320, 240, 121, 61))
        self.Button_choose_file.setFont(font)
        self.Button_choose_file.setObjectName("Button_choose_file")
        self.Button_choose_file.clicked.connect(lambda: self.thread_it(self.get_filename(Form)))

        # 按条件下载
        self.Button_condition_start = QtWidgets.QPushButton(Form)
        self.Button_condition_start.setGeometry(QtCore.QRect(570, 380, 111, 51))
        self.Button_condition_start.setObjectName("Button_condition_start")
        self.Button_condition_start.clicked.connect(lambda: self.condition_down(Form))

        self.Page_input = QtWidgets.QLineEdit(Form)
        self.Page_input.setGeometry(QtCore.QRect(220, 66, 231, 31))
        self.Page_input.setText("")
        self.Page_input.setObjectName("Page_input")
        
        # 单张下载url
        self.Label_page = QtWidgets.QLabel(Form)
        self.Label_page.setGeometry(QtCore.QRect(20, 66, 181, 31))
        self.Label_page.setObjectName("Label_page")

        # 录下载张数
        self.Label_down_nums = QtWidgets.QLabel(Form)
        self.Label_down_nums.setGeometry(QtCore.QRect(510, 250, 171, 41))
        self.Label_down_nums.setObjectName("Label_down_nums")
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.Label_down_nums.setFont(font)

        self.spinBox_nums_common = QtWidgets.QSpinBox(Form)
        self.spinBox_nums_common.setGeometry(QtCore.QRect(220, 130, 61, 31))
        self.spinBox_nums_common.setMinimum(1)
        self.spinBox_nums_common.setMaximum(20)
        self.spinBox_nums_common.setObjectName("spinBox_nums_rmf")

        self.spinBox_nums_end = QtWidgets.QSpinBox(Form)
        self.spinBox_nums_end.setGeometry(QtCore.QRect(450, 430, 61, 31))
        self.spinBox_nums_end.setMinimum(1)
        self.spinBox_nums_end.setMaximum(20)
        self.spinBox_nums_end.setObjectName("spinBox_nums_end")

        self.spinBox_start_num = QtWidgets.QSpinBox(Form)
        self.spinBox_start_num.setGeometry(QtCore.QRect(280, 430, 61, 31))
        self.spinBox_start_num.setMinimum(1)
        self.spinBox_start_num.setMaximum(20)
        self.spinBox_start_num.setObjectName("spinBox_start_num")

        self.label_start_num = QtWidgets.QLabel(Form)
        self.label_start_num.setGeometry(QtCore.QRect(200, 440, 72, 15))
        self.label_start_num.setObjectName("label_start_num")
        self.label_end_num = QtWidgets.QLabel(Form)
        self.label_end_num.setGeometry(QtCore.QRect(370, 440, 72, 15))
        self.label_end_num.setObjectName("label_end_num")

        self.Label_nums = QtWidgets.QLabel(Form)
        self.Label_nums.setGeometry(QtCore.QRect(120, 130, 91, 21))
        self.Label_nums.setObjectName("Label_nums")

        self.comboBox_time = QtWidgets.QComboBox(Form)
        self.comboBox_time.setGeometry(QtCore.QRect(250, 360, 121, 31))
        self.comboBox_time.setObjectName("comboBox_time")
        self.comboBox_time.addItem("")
        self.comboBox_time.addItem("")
        self.comboBox_time.addItem("")
        self.comboBox_time.addItem("")
        self.comboBox_time.addItem("")

        self.comboBox_condition = QtWidgets.QComboBox(Form)
        self.comboBox_condition.setGeometry(QtCore.QRect(400, 360, 111, 31))
        self.comboBox_condition.setObjectName("comboBox_condition")
        self.comboBox_condition.addItem("")
        self.comboBox_condition.addItem("")
        self.comboBox_condition.addItem("")
        self.comboBox_condition.addItem("")
        self.comboBox_condition.addItem("")

        # General Anime People
        self.checkBox_general = QtWidgets.QCheckBox(Form)
        self.checkBox_general.setGeometry(QtCore.QRect(30, 349, 61, 19))
        self.checkBox_general.setAutoFillBackground(True)
        self.checkBox_general.setChecked(True)
        self.checkBox_general.setObjectName("checkBox_General")
        self.checkBox_general.stateChanged.connect(lambda: self.update_categories(self.checkBox_general))
        self.checkBox_anime = QtWidgets.QCheckBox(Form)
        self.checkBox_anime.setGeometry(QtCore.QRect(100, 349, 61, 19))
        self.checkBox_anime.setAutoFillBackground(True)
        self.checkBox_anime.setChecked(True)
        self.checkBox_anime.setTristate(False)
        self.checkBox_anime.setObjectName("checkBox_Anime")
        self.checkBox_anime.stateChanged.connect(lambda: self.update_categories(self.checkBox_anime))
        self.checkBox_people = QtWidgets.QCheckBox(Form)
        self.checkBox_people.setGeometry(QtCore.QRect(170, 349, 61, 19))
        self.checkBox_people.setAutoFillBackground(True)
        self.checkBox_people.setChecked(True)
        self.checkBox_people.setTristate(False)
        self.checkBox_people.setObjectName("checkBox_People")
        self.checkBox_people.stateChanged.connect(lambda: self.update_categories(self.checkBox_people))

        #==========SFW  Sketchy   NSFW  ==============

        self.checkBox_SFW = QtWidgets.QCheckBox(Form)
        self.checkBox_SFW.setGeometry(QtCore.QRect(20, 380, 51, 31))
        self.checkBox_SFW.setAutoFillBackground(True)
        self.checkBox_SFW.setChecked(True)
        self.checkBox_SFW.setObjectName("checkBox_SFW")
        self.checkBox_SFW.stateChanged.connect(lambda: self.update_purity(self.checkBox_SFW))
        self.checkBox_Sketchy = QtWidgets.QCheckBox(Form)
        self.checkBox_Sketchy.setGeometry(QtCore.QRect(80, 380, 81, 31))
        self.checkBox_Sketchy.setAutoFillBackground(True)
        self.checkBox_Sketchy.setChecked(True)
        self.checkBox_Sketchy.setTristate(False)
        self.checkBox_Sketchy.setObjectName("checkBox_Sketchy")
        self.checkBox_Sketchy.stateChanged.connect(lambda: self.update_purity(self.checkBox_Sketchy))
        self.checkBox_NSFW = QtWidgets.QCheckBox(Form)
        self.checkBox_NSFW.setGeometry(QtCore.QRect(170, 380, 61, 31))
        self.checkBox_NSFW.setAutoFillBackground(True)
        self.checkBox_NSFW.setTristate(False)
        self.checkBox_NSFW.setObjectName("checkBox_NSFW")
        self.checkBox_NSFW.stateChanged.connect(lambda: self.update_purity(self.checkBox_NSFW))

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(110, 200, 591, 51))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 310, 871, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(0, 210, 871, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(Form)
        self.comboBox_time.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def set_down_nums(self, text="已经下载张数"):
        _translate = QtCore.QCoreApplication.translate
        self.Label_down_nums.setText(_translate("Form", text))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "WallHaven壁纸批量下载 -- 吾爱发布 -- Lthero"))
        self.Button_start.setText(_translate("Form", "开始从此页面下载"))
        self.Button_choose_file.setText(_translate("Form", "选择文件夹"))
        self.Label_page.setText(_translate("Form", "输入wallhaven中的网址"))
        self.Label_nums.setText(_translate("Form", "下载页数"))
        self.set_down_nums()
        self.label_start_num.setText(_translate("Form", "起始页码"))
        self.label_end_num.setText(_translate("Form", "终止页码"))
        self.comboBox_time.setCurrentText(_translate("Form", "近一个月的"))
        self.comboBox_time.setItemText(0, _translate("Form", "最新的"))
        self.comboBox_time.setItemText(1, _translate("Form", "近一个月的"))
        self.comboBox_time.setItemText(2, _translate("Form", "近三个月的"))
        self.comboBox_time.setItemText(3, _translate("Form", "近六个月的"))
        self.comboBox_time.setItemText(4, _translate("Form", "近一年的"))
        self.comboBox_time.currentIndexChanged.connect(lambda: self.update_topRange())

        self.comboBox_condition.setItemText(0, _translate("Form", "Top榜单"))
        self.comboBox_condition.setItemText(1, _translate("Form", "收藏榜单"))
        self.comboBox_condition.setItemText(2, _translate("Form", "评论榜单"))
        self.comboBox_condition.setItemText(3, _translate("Form", "Hot榜单NSFW"))
        self.comboBox_condition.setItemText(4,_translate("Form", "随机下载"))
        self.comboBox_condition.currentIndexChanged.connect(lambda :self.updata_sorting())

        self.checkBox_Sketchy.setText(_translate("Form", "Sketchy"))
        self.checkBox_SFW.setText(_translate("Form", "SFW"))
        self.checkBox_NSFW.setText(_translate("Form", "NSFW"))
        self.Button_condition_start.setText(_translate("Form", "开始按条件下载"))
        self.checkBox_general.setText(_translate("Form", "常规"))
        self.checkBox_anime.setText(_translate("Form", "动漫"))
        self.checkBox_people.setText(_translate("Form", "真人"))
        #self.label.setText(_translate("Form", "输入指定网站可以从指定页面向后按 ！开始！ 下载，不输入指定网站按 ！开始条件下载 ！ \n\t\t\t 一次下载大约23张 \n\t\t 若长时间不下载，可以重新点击开始尝试"))

    def get_filename(self, form):
        self.file = QFileDialog.getExistingDirectory(form, "选择文件夹", ".")
        if self.file != '':
            self.mesb.about(form, '提示', '选择成功  ' + self.file)
        else:
            self.mesb.about(form, '提示', '选择失败  ')

    def thread_it(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def down_load(self, url,num, file_path, form):
        ui.mesb.about(form, '提示', '开始下载 稍等片刻~~~')
        thread1 = myThread(url,num, file_path, form)
        thread1.start()

    # def fix_time(self):
    #     'https://wallhaven.cc/'+'search?categories=111&purity=110&topRange=1y&sorting=toplist&order=desc'

    def start(self, form):
        if self.file != '':
            if self.Page_input.text()!='':
                try:
                    self.down_load(self.Page_input.text(), self.spinBox_nums_common.text(), self.file, form)
                except():
                    self.mesb.about(form, '提示', '出错,重启后再下载')
            else:
                self.mesb.about(form, '提示', '先输入指定页面再开始')
        else:
            self.mesb.about(form, '提示', '先选择路径')

    def update_categories(self,check_box):
        name = check_box.objectName()
        if check_box.isChecked():
            if name == 'checkBox_General':
                self.mark[0] = 1
            elif name == 'checkBox_Anime':
                self.mark[1] = 1
            elif name == 'checkBox_People':
                self.mark[2] = 1
        else:
            if name == 'checkBox_General':
                self.mark[0] = 0
            elif name == 'checkBox_Anime':
                self.mark[1] = 0
            elif name == 'checkBox_People':
                self.mark[2] = 0
        self.categories = ''
        for i in self.mark:
            self.categories = self.categories + str(i)

    def update_purity(self, check_box):
        name = check_box.objectName()
        if check_box.isChecked():
            if name == 'checkBox_SFW':
                self.mark_2[0] = 1
            elif name == 'checkBox_Sketchy':
                self.mark_2[1] = 1
            elif name == 'checkBox_NSFW':
                self.mark_2[2] = 1
        else:
            if name == 'checkBox_SFW':
                self.mark_2[0] = 0
            elif name == 'checkBox_Sketchy':
                self.mark_2[1] = 0
            elif name == 'checkBox_NSFW':
                self.mark_2[2] = 0
        self.purity = ''
        for i in self.mark_2:
            self.purity = self.purity + str(i)

    def update_topRange(self):
        choice_time=self.comboBox_time.currentText()
        if choice_time=='近一个月的':
            self.topRange='1M'
        elif choice_time=='最新的':
            self.topRange='1d'
        elif choice_time=='近三个月的':
            self.topRange='3M'
        elif choice_time=='近六个月的':
            self.topRange='6M'
        else:
            self.topRange='1y'

    def updata_sorting(self):
        choice_time = self.comboBox_condition.currentText()
        if choice_time == 'Top榜单的':
            self.sorting = 'toplist'
        elif choice_time == '收藏榜单':
            self.sorting = 'favorites'
        elif choice_time == '评论榜单':
            self.sorting = 'views'
        elif choice_time == 'Hot榜单NSFW':
            self.sorting = 'hot'
        else:
            self.sorting = 'random'


    def condition_down(self, form):
        if self.file != '':
            try:
                fixed_url = 'https://wallhaven.cc/' + 'search?categories=' + self.categories + '&purity=' +self.purity+ '&topRange=' + \
                            self.topRange + '&sorting='+self.sorting+'&order=desc'+'&page='+self.spinBox_start_num.text()#+self.purity
                if int(self.spinBox_nums_end.text())-int(self.spinBox_start_num.text())<0:
                    num=1
                else:
                    num=int(self.spinBox_nums_end.text())-int(self.spinBox_start_num.text())+1
                self.down_load(fixed_url, num, self.file, form)
            except():
                self.mesb.about(form, '提示', '出错,重启后再下载')
        else:
            self.mesb.about(form, '提示', '先选择路径')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
