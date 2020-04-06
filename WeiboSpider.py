# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
import random
import time
import pandas as pd
import requests
import re


class Weibo:
    cookie = {
        "Cookie": "",
       }    #需填入cookies，登录weibo.cn，使用F12开发者工具找到cookie字段复制，具体操作网上很多教程
    agents = [
        "User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        ]

    def get_gjc(self):
        UA = random.choice(self.agents)
        header = {'User-Agent': UA}
        pattern = r'\d+'
        data = pd.DataFrame(columns = ("gjc", "user_name", "weibos", "post_time","zhuanfa", "num_zan", "num_forwarding", "num_comment"))
        gjc = input("请输入关键词：")
        url = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&sort=hot&page=1".format(gjc)
        #print(url)
        html = requests.get(url, cookies=self.cookie, headers=header)
        time.sleep(3)
        pl = BeautifulSoup(html.text, 'lxml').find('div', class_='pa', id='pagelist')
        if pl != None:
            num = int(pl.find_all('input')[0]['value'])
        else:
            num = 1
        print('***************共找到%s页数据*****************'% num)
        for n in range(1, num+1):
            url2 = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&sort=hot&page={}'.format(gjc ,n)  #获取关键词和话题的链接url
            print('***********正在爬取第%s页数据**************'%(n))
            html2 = requests.get(url2, cookies=self.cookie, headers=header)
            time.sleep(3)
            if BeautifulSoup(html2.text, 'lxml').find_all('div', class_='tip')[-1].get_text() == '热搜榜':
                print('**************没有找到任何内容***************')
                break
            selector = BeautifulSoup(html2.text, 'lxml').find_all('div', class_='c')
            if len(selector) > 5:
                for i in range(3, len(selector) - 2):
                    n = selector[i].find_all('div')
                    if len(n) == 3:
                        user_name = n[0].find('a', class_='nk').get_text()
                        weibos = n[2].get_text().split('  ')[0]
                        zhuanfa = n[0].find('span', class_='ctt').get_text()
                        all_num = n[2].find_all('a')
                        if all_num[-1].get_text() == '收藏':
                            num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                            num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                            num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                        else:
                            num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                            num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                            num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])
                        others = n[2].find('span', class_='ct').get_text().split(' ')
                        if others[0]:
                            post_time = str(others[0])
                    elif len(n) == 1:
                        user_name = n[0].find('a', class_='nk').get_text()
                        zhuanfa = ''
                        weibos = n[0].find('span', class_='ctt').get_text()
                        all_num = n[0].find_all('a')
                        if all_num[-1].get_text() == '收藏':
                            num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                            num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                            num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                        else:
                            num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                            num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                            num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])
                        others = n[0].find('span', class_='ct').get_text().split(' ')
                        if others[0]:
                            post_time = str(others[0])
                    elif len(n) == 2:
                        user_name = n[0].find('a', class_='nk').get_text()
                        z = n[1].find_all('span')
                        if len(z) >= 2:
                            weibos = n[1].get_text().split('  ')[0]
                            all_num = n[1].find_all('a')
                            zhuanfa = n[0].find('span', class_='ctt').get_text()
                            if all_num[-1].get_text() == '收藏':
                                num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                            else:
                                num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])
                        else:
                            weibos = n[0].find('span', class_='ctt').get_text()
                            zhuanfa = ''
                            all_num = n[1].find_all('a')
                            if all_num[-1].get_text() == '收藏':
                                num_zan = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-3].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-2].get_text())[0])
                            else:
                                num_zan = int(re.findall(pattern, all_num[-5].get_text())[0])
                                num_forwarding = int(re.findall(pattern, all_num[-4].get_text())[0])
                                num_comment = int(re.findall(pattern, all_num[-3].get_text())[0])

                        others = n[1].find('span', class_='ct').get_text().split(' ')
                        if others[0]:
                            post_time = str(others[0])
                    else:
                        continue
                    value = {
                        'gjc': gjc,
                        'user_name': user_name,
                        'weibos': weibos,
                        'zhuanfa': zhuanfa,
                        'post_time': post_time,
                        'num_zan': num_zan,
                        'num_forwarding': num_forwarding,
                        'num_comment': num_comment,
                    }
                    data = data.append(value, ignore_index=True)
                    print(weibos)
        data.to_csv("%s.csv" % gjc, encoding="utf_8_sig")
        print("*******************爬取结束！*****************")

if __name__ == '__main__':
    wb = Weibo()
    wb.get_gjc()
