'''
作者 lthero
网站 lthero.cn
'''
import requests
import threading
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
    def __init__(self, page, num, file_name):
        threading.Thread.__init__(self)
        self.page = page
        self.num = num
        self.file_path = file_name

    def run(self):
        try:
            start = int(self.page[-1])
            url = [self.page]
            if int(self.num) >= 2:
                url.append(self.page)
                for i in range(start, start+int(self.num) + 1):
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
                name = i.split('/')[-1]
                each_url = 'https://w.wallhaven.cc/full/%s/wallhaven-%s.jpg' % (name[0:2], name)
                html = requests.head(each_url)
                res = html.status_code
                flag = 0
                if res == 404:
                    each_url = each_url[0:-3] + 'png'
                    flag = 1
                t = threading.Thread(target=download, args=(each_url, name, self.file_path, flag))
                cent += 1
                threadings.append(t)
                t.start()
            for x in threadings:
                x.join()
        except:
            return


def download(url, name, file_path, flag):
    fix_file_name = '%s/%s.jpg' % (file_path, name)
    post_lei='.jpg'
    if flag == 1:
        fix_file_name = '%s/%s.png' % (file_path, name)
        post_lei = '.png'
    with open(fix_file_name, 'wb') as f:
        img = requests.get(url, headers=headers).content
        f.write(img)



def open_url(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    html = response.text
    return html


class No_UI(object):
    def __init__(self,path,sorting,toprange,purity='110',categories='110',start_page=1,num=1):
        self.file = path#'E:\文件安装测试\百度贴吧图片\Wallhaven'
        self.sorting = sorting#'toplist'
        #时间
        self.topRange = toprange#'3M'
        #SFW
        self.purity = purity#'001'
        #真人
        self.categories = categories#'110'
        #页数
        self.num=num
        #起始页数
        self.start_page=start_page

    def thread_it(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    def down_load(self, url, num, file_path):
        thread1 = myThread(url, num, file_path)
        thread1.start()

    def condition_down(self):
        if self.file != '':
            fixed_url = 'https://wallhaven.cc/' + 'search?categories=' + self.categories + '&purity=' + self.purity + '&topRange=' + \
                        self.topRange + '&sorting=' + self.sorting + '&order=desc' + '&page='+str(self.start_page)
            self.down_load(fixed_url, self.num, self.file)




if __name__ == '__main__':
    pa=input('输入路径')
    start_p=int(input('起始页数'))
    pages=int(input('输入要下载页数'))
    arr_stort=['date_added','toplist','favorites','views','hot','random']
    sorte=int(input('输入排序方式：0、date_added 1、toplist 2、favorites 3、views 4、hot 5、random\n'))
    arr_time=['1w','1M','3M','6M','1y','1d']
    times=int(input('输入时间：0、上周 1、近一个月的 2、近三个月的 3、近六个月的 4、一年 5、最新的\n'))
    pur=input('输入SFW  Sketchy NSFW  默认110\n')
    cat=input('输入普通  动漫   真人   默认110\n')
    cin=No_UI(pa,arr_stort[sorte],arr_time[times],pur,cat,start_p,pages)
    cin.condition_down()
