# -*- coding: utf-8 -*-
import MySQLdb,json

#in init function please change the config to fit your own requirement
#fetchone(): return type: None/dict
#fetchall(): return type: tuple(may be empty tuple)
#all function below return a value or a list

class dbapi:
	def __init__(self):
		self.host="localhost"
		self.user="comhelp"
		self.passwd="20140629"
		self.dbname="community"
		self.charset="utf8"
		self.db=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.dbname,charset=self.charset)

	def getUserByUserId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from user where id=%s"
		param=(userid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getUserByUserName(self,username):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from user where name=%s"
		param=(username,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def CheckRelationbyId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from relation where usrid=%s"
		param=(userid,)
		cursor.execute(sql,param)
		result=cursor.fetchall()
		cursor.close()
		return result

	def getUsermassegeByUserId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from user ,info where user.id=%s and info.id=%s"
		param=(userid,userid)
		cursor.execute(sql,param)
		result=cursor.fetchall()
		cursor.close()
		return result

	def getEventByEventId(self,eventid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from event where id=%s"
		param=(eventid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def getEventsByUserId(self,userid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from event where usrid=%s"
		param=(userid,)
		cursor.execute(sql,param)
		result=cursor.fetchall()
		cursor.close()
		return list(result)

	def getEventsByUserName(self,username):
		user=self.getUserByUserName(username)
		if(not user):
			return []
		return self.getEventsByUserId(user["id"])

	#check if cardid exist
	#exist return dict
	#not exist return none
	def getInfoBycardid(self,cardid):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from info where cardid=%s"
		param=(cardid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	#register a new user
	#pre condiction:no user.name,info.cardid duplicate
	#after : insert new user,new info
	def register(self,content):
		cursor = self.db.cursor()
		sql = "insert into user(name,kind,password) values(%s,%s,%s)"
		param = (content["username"],content["kind"],content["password"])
		cursor.execute(sql,param)
		self.db.commit()
		
		cursor.execute('SELECT LAST_INSERT_ID()')
		result=cursor.fetchone()
		print result[0]

		sql = "insert into info(id,cardid,name,sex,age,address,illness,credit,score) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		param = (result[0],content["cardid"],content["realname"],content["sex"],content["age"],content["address"],content["illness"],0,0)
		cursor.execute(sql,param)
		self.db.commit()
				
		cursor.close()
		return 
 
	#insert support mseeage in event
	#pre condiction:user.id，event.id exist;event.state = 0
	#after: uptate assist in event
	def supportmessageinsert(self,content):
		cursor = self.db.cursor()
		sql ="update event set assist= %s where id = %s"
		param = (content["assist"],content["eventid"])
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return

	def getRelationByUserId(self, u_id, r_id):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="SELECT * FROM relation WHERE usrid = '" + u_id + "' AND cid = '" + r_id + "'"
		cursor.execute(sql)
		row = int(cursor.rowcount)
		cursor.close()
		return row

	#update user cid by uid
	#untest
	def UpdateCidByuid(self,cid,uid):
		cursor = self.db.cursor()
		sql = "update user set cid = %s where id = %s"
		param = (cid,uid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return
		
	#insert support mseeage in event
	#pre condiction:user.id，event.id exist;event.state = 0
	#after: uptate assist in event
	def supportmessageinsert(self,content):
		cursor = self.db.cursor()
		sql ="update event set assist= %s where id = %s"
		param = (content["assist"],content["eventid"])
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return

    #get all relativeName by user.id
    #return a list contain all relations(including uid)
	def getAllRelativeNamebyUid(self,uid):
		cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql = "select * from relation where usrid = %s"
		param = (uid,)
		rlist = []
		rlist.append(uid)
		cursor.execute(sql,param)
		for row in cursor.fetchall():
			rlist.append(row["cid"])
		return rlist

	# change a event sate to 1
	#in order to end a event
	def changeEventState(self,eid):
		cursor = self.db.cursor()
		sql ="update event set state= %s where id = %s"
		param = (1,eid)
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return


	'''Yeqin Zheng, 09/07/2014'''
	def getRelationByUsername(self, u_name, r_name):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getUserByUserName(r_name)
		r_id = str(result["id"])
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="SELECT * FROM relation WHERE usrid = '" + u_id + "' AND cid = '" + r_id + "'"
		cursor.execute(sql)
		row = int(cursor.rowcount)
		cursor.close()
		return row

	def deleteRelationByUsername(self, u_name, r_name):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getUserByUserName(r_name)
		r_id = str(result["id"])
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="DELETE FROM relation WHERE usrid = '" + u_id + "' AND cid = '" + r_id + "'"
		cursor.execute(sql)
		self.db.commit()
		cursor.close()

	def addRelationByUsername(self, u_name, r_name):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getUserByUserName(r_name)
		r_id = str(result["id"])
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="INSERT INTO relation (usrid, cid, kind) VALUES ('" + u_id + "', '" + r_id + "', '1')"
		cursor.execute(sql)
		cursor.close()

	def addaidhelper(self, u_name, e_id):
		result = self.getUserByUserName(u_name)
		u_id = str(result["id"])
		result = self.getEventByEventId(e_id)
		if result["state"] == 0:
			return "0"
		else:
			cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
			sql="INSERT INTO helper (eid, usrid) VALUES ('" + e_id + "', '" + u_id + "')"
			cursor.execute(sql)
			cursor.close()
			return "1"
	'''.'''

	#Anton Zhong
	def getUserIdByUserName(self,username):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select id from user where name=%s"
		param=(username,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def addEventByUserName(self,username,message):
		usrid=self.getUserIdByUserName(username)
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		if(not usrid):
			return {"errorCode":403,"errorDesc":"No Such User: "+username}
		else:
			if(not("kind" in message and "content" in message)):
				return {"errorCode":403,"errorDesc":"Messge Incomplete"}
			else:
				sql="insert into event (usrid,kind,state,content) values (%s,%s,%s,%s)"
				param=(usrid["id"],message["kind"],0,message["content"])
				if("assist" in message):
					sql="insert into event (usrid,kind,state,content,assist) values (%s,%s,%s,%s,%s)"
					param=(usrid["id"],message["kind"],0,message["content"],message["assist"])
				cursor.execute(sql,param)
				self.db.commit()

				#return last insert id
				cursor.execute("select last_insert_id()")
				return {"errorCode":200,"errorDesc":"","eventid":cursor.fetchone()["last_insert_id()"]}
		cursor.close()

	#07/09
	#seach user by sex,age,kind and return the row of table user
	# it has 8 options
	def searchUserbySexAgeKind(self,content):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		if(content['sex']):
			if(content['age']):
				if(content['kind']):
					sql="select user.id from user,info where info.sex=%s and info.age=%s and user.kind=%s"
					param=(content['sex'],content['age'],content['kind'])
				else:
					sql="select user.id from user,info where info.sex=%s and info.age=%s"
					param=(content['sex'],content['age'])
			else:
				if(content['kind']):
					sql="select user.id from user,info where info.sex=%s and user.kind=%s"
					param=(content['sex'],content['kind'])
				else:
					sql="select user.id from user,info where info.sex=%s"
					param=(content['sex'],)
		else:
			if(content['age']):
				if(content['kind']):
					sql="select user.id from user,info where info.age=%s and user.kind=%s"
					param=(content['age'],content['kind'])
				else:
					sql="select user.id from user,info where info.age=%s"
					param=(content['age'],)
			else:
				if(content['kind']):
					sql="select user.id from user,info where user.kind=%s"
					param=(content['kind'],)
				else:
					data=[{'state':0}]#input is null return state 0
		            result=json.dumps(data)
					return result
		cursor.execute(sql,param)
		result1=cursor.fetchall()
		if(result1):
			userlist=[]
			for x in result1:
				userlist.append(self.getUserByUserId(x['id']))
			data=[{'state':1},userlist]#return the user table successly
		else:
			data=[{'state':2}]#the user not exist,return state 2
		result=json.dumps(data)
		return result

	#update the password by userid and userpassword
	def UpdatePassword(self,content):
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		if(content['passwd']):
			sql="update user set passwd=%s where id=%s"
			param=(content['passwd'],content['id'])
			cursor.execute(sql,param)
			self.db.commit()
			data=[{'state':1}]#update success return state 1
		    result=json.dumps(data)
			return result
		else:
			data=[{'state':0}]#input is null return state 0
		    result=json.dumps(data)
			return result
		cursor.close()


	#Anton Zhong
	def getHelperByEventIdAndUserName(self,eid,username):
		usrid=self.getUserIdByUserName(username)
		#No such user return none
		if(not usrid):
			return None
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select * from helper where eid=%s and usrid=%s"
		param=(eid,usrid["id"])
		cursor.execute(sql,param)
		result=cursor.fetchone()
		cursor.close()
		return result

	def checkHelperByEventIdAndUserName(self,eid,username):
		usrid=self.getUserIdByUserName(username)
		if(not usrid):
			return False
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="select usrid from helper where eid=%s"
		param=(eid,)
		cursor.execute(sql,param)
		result=cursor.fetchone()
		if(not result):
			return False
		return True

	def addSupportByEventIdAndUserName(self,eid,username,message):
		if(not self.checkHelperByEventIdAndUserName(eid,username)):
			return {"errorCode":403,"errorDesc":"No Such Helper "+str(username)+" in event "+str(eid)}
		if(not ("content" in message) ):
			return {"errorCode":403,"errorDesc":"Messge Incomplete"}
		else:
			cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
			sql="insert into support (eid,usrid,content) values (%s,%s,%s)"
			param=(eid,self.getUserIdByUserName(username)["id"],message["content"])
			cursor.execute(sql,param)
			self.db.commit()
			cursor.execute("select last_insert_id()")
			result=cursor.fetchone()
			cursor.close()
			return {"errorCode":200,"errorDesc":"","supportid":result["last_insert_id()"]}

	def setCreditByEventIdAndUserName(self,eid,username,credit):
		if(not self.checkHelperByEventIdAndUserName(eid,username)):
			return {"errorCode":403,"errorDesc":"No Such Helper "+str(username)+" in event "+str(eid)}
		cursor=self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		sql="update helper set credit = %s where eid=%s and usrid=%s"
		usrid=self.getUserIdByUserName(username)
		param=(credit,eid,usrid["id"])
		cursor.execute(sql,param)
		self.db.commit()
		cursor.close()
		return {"errorCode":200,"errorDesc":""}
	#07/10

	def __del__(self):
		self.db.close()
