import json,os,base64
import xml.etree.ElementTree as ET
import datetime
class util:
	def __init__(self):
		self.score=dict()
		config=ET.parse(os.path.abspath("./static/config.xml"))
		root=config.getroot()
		levels=root.findall("./score/level")
		for level in levels:
			num=int(level[0].text)
			minScore=int(level[1].text)
			maxScore=int(level[2].text)

			self.score[num]=dict()
			self.score[num]['min']=minScore
			self.score[num]['max']=maxScore


	def setAvatar(self,username,filestring,dbapi):
		print "Start set Avatar"
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"wb")
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()
		print "End set Avatar"

	def getAvatar(self,username,dbapi):
		print "Start get Avatar"
		userid=dbapi.getUserByUserName(username)['id']
		avatar=open(os.path.abspath('./static/avatar/'+str(userid)+".png"),"rb")
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		print "End get Avatar"
		return result

	def setAvatarbyUid(self,uid,filestring):
		print "Start set Avatar"
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"wb")
		avatar.write(base64.standard_b64decode(filestring))
		avatar.close()
		print "End set Avatar"

	def getAvatarbyUid(self,uid):
		print "Start get Avatar"
		avatar=open(os.path.abspath('./static/avatar/'+str(uid)+".png"),"rb")
		result=""
		result=base64.standard_b64encode(avatar.read())
		avatar.close()
		print "End get Avatar"
		return result

	def setVideobyEid(self,uid,videostring):
		newdir = raw_input('./static/Video/'+str(uid))
		os.mkdir(newdir)
		video=open(os.path.abspath('./static/Video/'+str(uid)+'/'+str(uid)+'.3gp'),"wb")
		video.write(base64.standard_b64decode(videostring))
		video.close()
		print "set Video success"

	def setAudiobyEid(self,uid,videostring):
		newdir = raw_input('./static/Audio/'+str(uid))
		os.mkdir(newdir)
		audio=open(os.path.abspath('./static/Audio/'+str(uid)+'/'+str(uid)+'.amr'),"wb")
		audio.write(base64.standard_b64decode(videostring))
		audio.close()
		print "set Audio success"

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

		_Credit = 0.0
		beta = 0.5
		gama = 0.05
		if (credit * 2 * 0.1) < 0.3:
			_Credit = 0.7 * (0.5 * flag1 + 0.5 * flag2) + 0.3 * (1 - beta / 2) * (credit * 2 * 0.1)
		else:
			if 0.5 < beta + gama:
				_Credit = 0.7 * (0.5 * flag1 + 0.5 * flag2) + 0.3 * 0.5 * (credit * 2 * 0.1)
			else:
				_Credit = 0.7 * (0.5 * flag1 + 0.5 * flag2) + 0.3 * (beta + gama) * (credit * 2 * 0.1)

		T_preCredit = dbapi.getpreviousEvent(askuser['id'], helper['id'])
		#return T_preCredit
		Cov = askuser['credit']
		Cr = helper['credit']

		curCredit = 0.0
		Reputation = 0.0
		timeInterval = 0.0
		if T_preCredit == None:
			curCredit = _Credit
			Reputation = Cov * _Credit
			#return str(curCredit) + ',' + str(Reputation)
		else:
			timeInterval = (datetime.datetime.now() - T_preCredit['time']).days
			#return timeInterval
			Factor = 1 / pow(timeInterval + 1, 1 / 3.0)
			#Factor = 0.8
			if Factor != 1:
				curCredit = Factor * T_preCredit['credit'] + (1 - Factor) * _Credit
				Reputation = (1 - Cov * (1 - Factor)) * Cr + (1 - Factor) * Cov * _Credit
				#return str(T_preCredit['credit']) + ',' + str(Factor) + ',' + str(_Credit) + ',' + str(curCredit) + ',' + str(Reputation)
			else:
				curCredit = _Credit
				Reputation = Cov * _Credit
				#return str(curCredit) + ',' + str(Reputation)

		dbapi.updateUserCredit(helper['id'], Reputation)
		#return dbapi.getUserInfobyUid(helper['id'])

		if T_preCredit == None:
			dbapi.insertpreviousEvent(askuser['id'], helper['id'], curCredit, event['endtime'])
			#return dbapi.getpreviousEvent(askuser['id'], helper['id'])
		else:
			dbapi.updatepreviousEvent(askuser['id'], helper['id'], curCredit, event['endtime'])