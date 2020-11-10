#-*- coding:utf-8 -*-
import itchat
from itchat.content import TEXT

#全局变量
myUserName = ''
slaveUserName = ''

#定义收取文字信息的操作
#收到一般信息时自动转发到指定用户
#收到“to n nickname: message”格式时向指定昵称用户回复信息
@itchat.msg_register(TEXT)
def forward(msg):
	if msg['Text'][:3] == "to ":
		try:
			characters = int(msg['Text'][3])
		except ValueError:
			itchat.send_msg('#系统：格式错误',slaveUserName)
		except IndexError:
			itchat.send_msg('#系统：找不到联系人',slaveUserName)
		else:
			n=5+characters 
			name = msg['Text'][5:n]
			try:
				sendUserName = searchUserName (name)
			except IndexError:
				itchat.send_msg('#系统：找不到联系人',slaveUserName)
			else:
				m = n+2
				text = msg['Text'][m:]
				itchat.send(text, sendUserName)

	else:
		fromRemark = searchRemark(msg['FromUserName'])
		fromNick = searchNick(msg['FromUserName'])
		sendText = fromRemark + " (" + fromNick + ") sends you a message: "+msg['Text']
		itchat.send(sendText, slaveUserName)

#设置：自动转发至微信昵称
def setUserName():
	result = itchat.search_friends('陈思悦')
	global slaveUserName
	slaveUserName = result[0]['UserName']

#以username搜索备注名
def searchRemark(num):
	result = itchat.search_friends(userName=num)
	resultRemarkName = result['RemarkName']
	return resultRemarkName

#以username搜索微信昵称
def searchNick(num):
	result = itchat.search_friends(userName=num)
	resultNickName = result['NickName']
	return resultNickName 

#以微信昵称搜索username
def searchUserName(nick):
	result = itchat.search_friends(name=nick)
	resultUserName = result[0]['UserName']
	return resultUserName

#获取本账号username
def getUserName():
	result = itchat.search_friends()
	global myUserName
	myUserName = result['UserName']
	

itchat.auto_login(hotReload=True)
setUserName()
getUserName()
itchat.run()
itchat.dump_login_status()