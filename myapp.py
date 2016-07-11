from flask import Flask,g,request,make_response,Response
import hashlib
import xml.etree.ElementTree as ET
import time
import urllib.request
import json

app = Flask(__name__)
#class myResponse(Response):
#    default_mimetype = 'text'

#class MyFlask(Flask):
#    response_class = myResponse

def getToken():
    appid = 'wx71afee28acc15dee'
    secret = '4d8fb7ef1b8a9a7acc35cfc717689f98'
    token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
    url_request = urllib.request.Request(url=token_url)
    url_contant = urllib.request.urlopen(url_request).read().decode('utf-8')
    access_token = json.loads(url_contant)['access_token']
    return access_token

@app.route('/')
def hello():
    return "Working"


@app.route('/wechat', methods = ['GET', 'POST'] )
def wechat_auth():
    if request.method == 'GET':
        token='zzzzzz'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s.encode('utf-8')).hexdigest() == signature):
            return make_response(echostr)
        else:
            return "Error"
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
        msgid = xml_rec.find('MsgId').text
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><MsgId><![CDATA[%s]]></MsgId></xml>"
        response = make_response(xml_rep % (fromu,tou,str(int(time.time())), content,msgid))
        response.content_type='application/xml'
        return response

@app.route('/reply')
def reply():
    token = getToken()
    return token

if __name__ == "__main__":
    app.run()


