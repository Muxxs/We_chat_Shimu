# -*- coding:utf-8 -*-

# -*- coding:utf-8 -*-

from flask import Flask
from flask import request
from flask import Flask,request,make_response
import time,hashlib,re,requests
import xml.etree.ElementTree as ET
import hashlib

app = Flask(__name__)
app.debug = True



def return_book(book):
    file=open("data.txt")
    for x in file.read().split("\n"):
        book_infor=x.split("|&|")
        if book==book_infor[0]:
            return "-------------\n" \
                   "---十-亩书屋---\n" \
                   "本书："+book+"\n" \
                              "京东价格："+book_infor[1]+"\n"+"本店价格："+book_infor[2]+"\n" \
                                                                               "-------------"
    return ""

@app.route('/weixin',methods=['GET','POST'])
def wechat():

    if request.method == 'GET':
        #这里改写你在微信公众平台里输入的token
        token = ''
        #获取输入参数
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        #字典排序
        list = [token, timestamp, nonce]
        list.sort()

        s = list[0] + list[1] + list[2]
        #å
        hascode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        #如果是来自微信的请求，则回复echostr
        if hascode == signature:
            return echostr
        else:
            return ""
    else: # 即如果为POST请求执行下面的代码
        xmlData = ET.fromstring(request.stream.read())
        msg_type = xmlData.find('MsgType').text
        if msg_type == 'text':
            ToUserName = xmlData.find('ToUserName').text
            FromUserName = xmlData.find('FromUserName').text
            Content = xmlData.find('Content').text
            Content= return_book(Content)
            if not Content=="":
                reply = '''<xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        </xml>'''
                response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content ) )
                response.content_type = 'application/xml'
                return response
            return "success"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=555)
