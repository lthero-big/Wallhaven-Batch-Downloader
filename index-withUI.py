import os
import sys
import time
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4389.90 Safari/531.36'
    ,
    'Cookie': '_pk_id.1.01b8=ea68c6fef4de8841.1656407868.; remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IkdPWkphbmQ4Wm04XC9NM1pmVFwvNXdCdz09IiwidmFsdWUiOiJLMWVSbzVYVTlUbnNaNUtrMzlcL2g5Z1NDcFI1MHlyenVhT2ttakxrWnZiYWhWOGhlbGxBR1ZIUUp0RE1UdlJMK2VqTDNwM3c1YkxhV1NKWUw3Z3liMm1rdDBmczJlcVhrTjBkZ2c0MDU4dHZBc1AzdW5PZHRhUFZZXC8yQzYwVjM1Mmw5WVE2aWI3ZytcL3VUZWgyK3Q1OE1hOW16Y3QzYjZreUcwUXloZVZRK29wUlNYc3JvY0plUW01WTF2bk80cmMiLCJtYWMiOiJhZjE4YmUzNzRhZjFmMmEzZWJmNTkxMzNiMGI4OWYxYTk2MGQ3NzUyYzIyYzE5YzRkMDcwMWI2YjBmNmQ4M2Y0In0%3D; _pk_ses.1.01b8=1; XSRF-TOKEN=eyJpdiI6IkJrQWd2RVBqRVI0RVJHSTh6RjZrekE9PSIsInZhbHVlIjoiRTRsZWNvRW1tYTVIS2xmNWV1cWxicWQzVDBzMjIxYnZVdGFuRWhYbUtkRTdWWDVjVHhTd1R5OHdia2dpTWRZbCIsIm1hYyI6IjQ4NDc3ZmNkNWU5NGE5ZDlmOGNkY2UxZjkwOGYyYjYwMDIxMTgyZGMwY2RiMTg5ZDdlOGJlZmIwNGQ3YzAzNDgifQ%3D%3D; wallhaven_session=eyJpdiI6IkhFZGhmNjdpb1dtejJqMk9xWU1Udmc9PSIsInZhbHVlIjoibFljMUIybnlmVW41ZGhcL1dYNjVWbUtpXC9vQitmbG5Ka2NpS0ZKNmdNUkttUDdXOVI2YW5MOTBIYlRSTXhIVXVwIiwibWFjIjoiNDYzMWRhNjI4Yzg4MWMyMjkxN2NiZjk0NzBlNzg2OGVlMzhjOTRhYTBlMGE0YzhjOWVhYjYwOTdkYTg4Y2I3ZiJ9'}
cent = 0

class eachPageThread(threading.Thread):
    def __init__(self, url, file_name, form):
        threading.Thread.__init__(self)
        self.form = form
        self.eachPageUrl = url
        self.file_path = file_name

    def run(self):
        try:
            eachPageCollection = []
            content = open_url(self.eachPageUrl)
            soup = BeautifulSoup(content, 'lxml')
            images = soup.find('section', class_="thumb-listing-page")
            for li in images.find_all('li'):
                string = str(li.a['href'])
                eachPageCollection.append(string)

            threadingSet = []
            for eachImage in eachPageCollection:
                name = eachImage.split('/')[-1]
                eachImageUrl = 'https://w.wallhaven.cc/full/%s/wallhaven-%s.jpg' % (name[0:2], name)
                html = requests.head(eachImageUrl)
                res = html.status_code
                ImagePosixFlag = 0
                if res == 404:
                    eachImageUrl = eachImageUrl[0:-3] + 'png'
                    ImagePosixFlag = 1

                t = threading.Thread(target=downloadEachImage, args=(eachImageUrl, name, self.file_path, ImagePosixFlag))
                threadingSet.append(t)
                t.start()

                ui.set_down_nums('已经下载 ' + str(cent) + ' 张')

            for eachThread in threadingSet:
                eachThread.join()
        except:
            return

    def get_enumerate(self):
        return threading.enumerate()


def downloadEachImage(url, name, file_path, flag):
    global cent
    fix_file_name = '%s/%s.jpg' % (file_path, name)
    if flag == 1:
        fix_file_name = '%s/%s.png' % (file_path, name)

    if not os.path.exists(fix_file_name):
        print("正在下载 %s" % fix_file_name)
        with open(fix_file_name, 'wb') as f:
            img = requests.get(url, headers=headers).content
            f.write(img)
        semalock.acquire()
        cent += 1
        semalock.release()
    else:
        print("发现%s存在，未下载" % fix_file_name)


def open_url(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    return html


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(794, 497)
        self.mesb = QMessageBox
        # 类型动漫。。
        self.mark = [1, 1, 0]
        # SFW
        self.mark_2 = [1, 1, 0]
        self.file = ''

        # date_added按时间
        self.sorting = 'toplist'
        self.topRange = '1M'
        self.categories = '110'
        self.purity = '110'
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
        self.spinBox_nums_common.setMaximum(500)
        self.spinBox_nums_common.setObjectName("spinBox_nums_rmf")

        self.spinBox_start_num = QtWidgets.QSpinBox(Form)
        self.spinBox_start_num.setGeometry(QtCore.QRect(280, 430, 61, 31))
        self.spinBox_start_num.setMinimum(1)
        self.spinBox_start_num.setMaximum(500)
        self.spinBox_start_num.setObjectName("spinBox_start_num")

        self.spinBox_nums_end = QtWidgets.QSpinBox(Form)
        self.spinBox_nums_end.setGeometry(QtCore.QRect(450, 430, 61, 31))
        self.spinBox_nums_end.setMinimum(1)
        self.spinBox_nums_end.setMaximum(500)
        self.spinBox_nums_end.setObjectName("spinBox_nums_end")


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

        # ==========SFW  Sketchy   NSFW  ==============

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
        self.comboBox_condition.setItemText(4, _translate("Form", "随机下载"))
        self.comboBox_condition.currentIndexChanged.connect(lambda: self.updata_sorting())


        self.checkBox_Sketchy.setText(_translate("Form", "Sketchy"))
        self.checkBox_SFW.setText(_translate("Form", "SFW"))
        self.checkBox_NSFW.setText(_translate("Form", "NSFW"))
        self.Button_condition_start.setText(_translate("Form", "开始按条件下载"))
        self.checkBox_general.setText(_translate("Form", "常规"))
        self.checkBox_anime.setText(_translate("Form", "动漫"))
        self.checkBox_people.setText(_translate("Form", "真人"))
        # self.label.setText(_translate("Form", "输入指定网站可以从指定页面向后按 ！开始！ 下载，不输入指定网站按 ！开始条件下载 ！ \n\t\t\t 一次下载大约23张 \n\t\t 若长时间不下载，可以重新点击开始尝试"))

    def updateEndSpinBoxNum(self):
        self.spinBox_nums_end.setMaximum(int(self.spinBox_start_num.text()) + 19)

    def get_filename(self, form):
        self.file = QFileDialog.getExistingDirectory(form, "选择文件夹", ".")
        if self.file != '':
            self.mesb.about(form, '对不起！', '选择成功  ' + self.file)
        else:
            self.mesb.about(form, '对不起！', '选择失败  ')

    def testIsFinish(self,theThread,form):
        while True:
            if len(theThread[0].get_enumerate()) == 2:
                break
            # print('当前运行线程：', len(theThread[0].get_enumerate()))
            time.sleep(1)
        print("全部下载完成")
        ui.Button_condition_start.setEnabled(True)
        ui.Button_start.setEnabled(True)
        ui.Button_choose_file.setEnabled(True)

    def thread_it(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def downLoad(self,url,num,file_path,form):
        start = int(url[-1])
        allPagesUrl = [url]
        if int(num) >= 2:
            for i in range(start + 1, int(num) + start):
                allPagesUrl.append(url[0:-1] + str(i))

        eachPageThreadSet=[]
        for eachPageUrl in allPagesUrl:
            t = eachPageThread(eachPageUrl, file_path, form)
            eachPageThreadSet.append(t)
            t.setDaemon(True)
            t.start()

        # 守望线程，判断是否全部下载完成
        args = [eachPageThreadSet, form]
        t2 = threading.Thread(target=self.testIsFinish, args=args)
        t2.setDaemon(True)
        t2.start()

        ui.Button_condition_start.setEnabled(False)
        ui.Button_start.setEnabled(False)
        ui.Button_choose_file.setEnabled(False)

        ui.mesb.about(form, '对不起！', '开始下载 稍等片刻~~~')



    def start(self, form):
        if self.file != '':
            if self.Page_input.text() != '':
                try:
                    global cent
                    cent -= cent
                    self.downLoad(self.Page_input.text(), self.spinBox_nums_common.text(), self.file, form)
                except():
                    self.mesb.about(form, '对不起！', '出错,重启后再下载')
            else:
                self.mesb.about(form, '对不起！', '先输入指定页面再开始')
        else:
            self.mesb.about(form, '对不起！', '先选择路径')

    def update_categories(self, check_box):
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
        choice_time = self.comboBox_time.currentText()
        if choice_time == '近一个月的':
            self.topRange = '1M'
        elif choice_time == '最新的':
            self.topRange = '1d'
        elif choice_time == '近三个月的':
            self.topRange = '3M'
        elif choice_time == '近六个月的':
            self.topRange = '6M'
        else:
            self.topRange = '1y'

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
                global cent
                cent -= cent
                fixed_url = 'https://wallhaven.cc/' + 'search?categories=' + self.categories + '&purity=' + self.purity + '&topRange=' + \
                            self.topRange + '&sorting=' + self.sorting + '&order=desc' + '&page=' + self.spinBox_start_num.text()  # +self.purity
                if int(self.spinBox_nums_end.text()) - int(self.spinBox_start_num.text()) < 0:
                    num = 1
                else:
                    num = int(self.spinBox_nums_end.text()) - int(self.spinBox_start_num.text()) + 1
                if num>20:
                    self.mesb.about(form, '对不起！', '一次性最多下载20页，过多容易导致程序异常')
                else:
                    self.downLoad(fixed_url,num,self.file,form)
            except():
                self.mesb.about(form, '对不起！', '出错,重启后再下载')
        else:
            self.mesb.about(form, '对不起！', '先选择路径')


if __name__ == '__main__':
    lock = threading.Lock()
    semalock=threading.Semaphore(1)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
