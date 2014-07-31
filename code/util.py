# -*- coding: utf-8 -*-
import json,os,base64
import datetime

class util:
	def setAvatar(self,username,filestring,dbapi):
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"wb")
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()

	def getAvatar(self,username,dbapi):
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"rb")
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		return result

	def setAvatarbyUid(self,uid,filestring):
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"wb")
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()

	def getAvatarbyUid(self,uid):
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"rb")
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		return result

	def setVideobyEid(self,uid,videostring):
		newdir = raw_input('./static/Video/'+str(uid))
		os.mkdir(newdir)
		video=open(os.path.abspath('./static/Video/'+str(uid)+'/'+str(uid)+'.3gp'),"wb")
		video.write(base64.standard_b64decode(videostring))
		video.close()

	def setAudiobyEid(self,uid,videostring):
		newdir = raw_input('./static/Audio/'+str(uid))
		os.mkdir(newdir)
		audio=open(os.path.abspath('./static/Audio/'+str(uid)+'/'+str(uid)+'.amr'),"wb")
		audio.write(base64.standard_b64decode(videostring))
		audio.close()

	def setCreditforHelper(self,event,askuser,helper,credit,dbapi):
		flag1 = 0
		flag2 = 0
		if event['kind'] == 3:
			if helper['vocation'] == 1:
				flag1 = 1
			if helper['age'] >= 40:
				flag2 = 1
		elif event['kind'] == 1:
			if helper['vocation'] == 2:
				flag1 = 1
			if helper['age'] >= 20 and helper['age'] <= 50:
				flag2 = 1

		#本次事件中得出的信用
		_Credit = 0.0

		#beta = 1.0 #定义成用户的属性
		#gama1 = 0.01 #
		#gama2 = 0.03 #

		if (credit * 2 * 0.1) <= 0.4:
			helper['beta'] -= helper['gama2']
		else:
			helper['beta'] += helper['gama1']

		#计算出本次事件的信用
		_Credit = (0.05 * flag1 + 0.05 * flag2) + (credit * 2 * 0.1)
		if _Credit > 1:
			_Credit = 1
		if helper['beta'] > 0 and helper['beta'] < 1:
			_Credit *= helper['beta']
		elif helper['beta'] <= 0:
			_Credit = 0
		else:
			helper['beta'] = 1

		T_preCredit = dbapi.getpreviousEvent(askuser['id'], helper['id'])
		#return T_preCredit
		Cov = askuser['credit']
		Cr = helper['credit']

		curCredit = 0.0
		Reputation = 0.0
		timeInterval = 0.0
		if T_preCredit == None:
			curCredit = _Credit
			if Cov >= 0.4:
				Reputation = _Credit
			else:
				Reputation = _Credit * 0.8
			#return str(curCredit) + ',' + str(Reputation)
		else:
			timeInterval = (datetime.datetime.now() - T_preCredit['time']).days
			#return timeInterval
			Factor = 1 / pow(timeInterval + 1, 1 / 3.0)
			#Factor = 0.8
			if Factor != 1:
				curCredit = Factor * T_preCredit['credit'] + (1 - Factor) * _Credit
				Reputation = Factor * Cr + (1 - Factor) * _Credit
				if Cov <= 0.4:
					Reputation *= 0.8
				#return str(T_preCredit['credit']) + ',' + str(Factor) + ',' + str(_Credit) + ',' + str(curCredit) + ',' + str(Reputation)
			else:
				curCredit = _Credit
				if Cov >= 0.4:
					Reputation = _Credit
				else:
					Reputation = _Credit * 0.8
				#return str(curCredit) + ',' + str(Reputation)

		dbapi.updateUserCredit(helper['id'], Reputation)
		#return dbapi.getUserInfobyUid(helper['id'])

		if T_preCredit == None:
			dbapi.insertpreviousEvent(askuser['id'], helper['id'], curCredit, event['endtime'])
			#return dbapi.getpreviousEvent(askuser['id'], helper['id'])
		else:
			dbapi.updatepreviousEvent(askuser['id'], helper['id'], curCredit, event['endtime'])
