import xml.etree.ElementTree as ET
class score:
	def __init__(self):
		self.config=dict()
		_config=ET.parse(os.path.abspath("./static/config.xml"))
		root=_config.getroot()
		levels=root.findall("./score/level")
		for level in levels:
			num=int(level[0].text)
			minScore=int(level[1].text)
			maxScore=int(level[2].text)

			self.config[num]=dict()
			self.config[num]['min']=minScore
			self.config[num]['max']=maxScore

	def getRankByScore(self,s):
		for num in self.config:
			if s<=self.config[num]['max'] and s>=self.config[num]['min']:
				result=dict()
				result['scoreMin']=self.config[num]['min']
				result['scoreMax']=self.config[num]['max']
				result['scoreLevel']=num
				return result
		print "error in getRankByScore("+str(s)+")"

	# 1:new user login for the first time +5/5
	# 2:user login for the first time every day +1/1
	# 3:caller give helper credit +2/50
	# 4:helper join in support +3/Infinity
	# 5:helper send support message +1/30
	# 6:user online for more than 12 hours a day +2/2

	# 7:helper earn the highest credit in a event +5/Infinity
	# allow more than one helper earn it in the same event

	# 8:send harmful support message -10/Infinity
	# 9:send useless event message -20/Infinity
	# 10:helper quit the event while the event does not end -1/Infinity
	# 11:caller give no credit to the helper after the event end for five days -10/infinity

	def updateScoreByCase(self,uid,cond,dbapi):
		def func1(u,d):
			d.operateScoreById(u,5)
			print "func1"
		def func2(u,d):
			d.operateScoreById(u,1)
			print "func2"
		def func3(u,d):
			d.operateScoreById(u,2)
			print "func3"
		def func4(u,d):
			d.operateScoreById(u,3)
			print "func4"
		def func5(u,d):
			d.operateScoreById(u,1)
			print "func5"
		def func6(u,d):
			d.operateScoreById(u,2)
			print "func6"
		def func7(u,d):
			d.operateScoreById(u,5)
			print "func7"
		def func8(u,d):
			d.operateScoreById(u,-10)
			print "func8"
		def func9(u,d):
			d.operateScoreById(u,-20)
			print "func9"
		def func10(u,d):
			d.operateScoreById(u,-1)
			print "func10"
		def func11(u,d):
			d.operateScoreById(u,-10)
			print "func11"

		if cond>=1 and cond<=11:
			funcName="func"+str(cond)
			(eval(funcName))(uid,dbapi)
		else:
			print "arguments incorrect"

if __name__ == '__main__':
	test=util()
	print test.getRankByScore(700)