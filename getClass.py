# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import http.cookiejar
import re
from PIL import Image, ImageFont, ImageDraw
import os

class JWCHandle():
    def __init__(self,stuName,stuPasswd):
        url = 'http://jwc.jxnu.edu.cn/Default_Login.aspx?preurl='
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('Host', 'jwc.jxnu.edu.cn'),
                             ('Accept-Encoding', 'gzip,deflate'),
                             ('Connection', 'keep-alive'),
                             ('Origin','http://jwc.jxnu.edu.cn'),
                             ('Content-Type',' application/x-www-form-urlencoded'),
                             ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                             ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'),
                             ('Accept-Language', 'zh-CN,zh;q=0.8'),
                             ('Upgrade-Insecure-Requests','1'),
                             ('Cache-Control', 'max-age=0')]
        contant = self.opener.open(url).read().decode('utf-8')
        __VIEWSTATE = re.findall(r'id="__VIEWSTATE" value="(.*?)"',contant)[0]
        __EVENTVALIDATION = re.findall(r'id="__EVENTVALIDATION" value="(.*?)"',contant)[0]
        value = {'__EVENTTARGET':'',
                 '__EVENTARGUMENT': '',
                 '__LASTFOCUS': '',
                 '__VIEWSTATE':__VIEWSTATE,
                 '__EVENTVALIDATION':__EVENTVALIDATION,
                 'StuNum': stuName,
                 'TeaNum':'',
                 'Password': stuPasswd,
                 'login':'登录'}
        postData = urllib.parse.urlencode(value).encode()
        self.opener.open(url, postData)

    def getContant(self,url):
        contant = self.opener.open(url).read().decode('utf-8')
        return contant

    def getClassItem(self,url):
        contant = self.opener.open(url).read().decode('utf-8')
        Itemlist_1 = re.findall(r'<DIV align="center">(.*?)</DIV>',contant)
        for i in range(2):
            Itemlist_1.remove('&nbsp;')
        for i in range(7):
            del Itemlist_1[0]
        for i in range(3,6):
            try:
                Itemlist_1.remove(str(i))
            except:
                continue
        del Itemlist_1[-1]
        Itemlist_1.remove('<FONT face="Arial, Helvetica, sans-serif">中 午</FONT>')
        Itemlist_1.remove('下午')
        Itemlist_1.remove('晚上')
        for i in range(len(Itemlist_1)):
            if Itemlist_1[i] == '&nbsp;':
                Itemlist_1[i] = ''
            else:
                Itemlist_1[i] = Itemlist_1[i] .split('<br>')
                Itemlist_1[i][0] = Itemlist_1[i][0].split('（')
        return Itemlist_1

    def drawPic(self,Item):
        imgFile = 'base.jpg'
        img = Image.open(imgFile)
        imgBrush = ImageDraw.Draw(img)
        font = ImageFont.truetype(os.path.join("fonts", "font.ttf"), 80)
        x,y,z = 640,500,0
        for i in range(7):
            for j in range(7):
                if Item[z] == '':
                    x += 380
                    z += 1
                else:
                    imgBrush.text((x, y), str(Item[z][0][0]), font=font, fill="#000000")
                    y += 80
                    imgBrush.text((x, y), str(Item[z][1]), font=font, fill="#000000")
                    x += 380
                    y -= 80
                    z += 1
            x = 640
            y += 180
        img.save("text.jpg")


if __name__ == "__main__":
    URL = 'http://jwc.jxnu.edu.cn/Default_Login.aspx?preurl='
    URL2 = r'http://jwc.jxnu.edu.cn/User/default.aspx?&code=111&&uctl=MyControl\xfz_kcb.ascx&MyAction=Personal'
    stuName = '*********'
    stuPasswd = '*********'
    #stuName = input('请输入学号： ')
    #stuPasswd = input('请输入密码： ')
    print('正在生成......')
    JWC = JWCHandle(stuName,stuPasswd)
    ItemList = JWC.getClassItem(URL2)
    JWC.drawPic(ItemList)
    print('图片生成成功')
