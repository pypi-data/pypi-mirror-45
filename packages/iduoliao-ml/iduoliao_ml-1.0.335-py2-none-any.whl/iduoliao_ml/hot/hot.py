#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
from .. import imatrix
from numpy import *

#TODO:存了两份 考虑怎么合并
SubjectIndexs = {
	"count": 0,
	"play": 1,
	"replay": 2,
	"conv": 3
}

WorksIndexs = {
	"play": 0,
	"like": 1,
	"shareF": 2,
	"shareI": 3,
	"replay": 4,
	"longTime": 5,
	"subAdd": 6,
	"playTimeAvg": 7,
	"conv": 8,
	"duration": 9,
	"size": 10
}

SubjectTotalWeight = 0.3

SubjectWeight = {
	'count': 20,
	'play': 1,
	'replay': 5
}

WorksWeight = {
	'play': 1,
	'like': 10,
	'shareF': 15,
	'shareI': 20,
	'replay': 5,
	'longTime': 10,
	'subAdd': 20
}

TimeDecay = {
	'half': 168,
	'flutter': 48.0
}

SameAidDecay = 0.0

Weight = {
	"conv": 0.4,
	"like": 0.05,
	"share": 0.1,
	"longPlay": 0.4,
	"sub": 0.05
}

Trust = {
	"resShow": 1000,
	"play": 100,
	"timeCount": 150
}

def calWorksScore(worksList):
	if len(worksList) == 0:
		return

	worksArgs = []
	for works in worksList:
		works.play = works.resShowPlay
		resShowTrust = min(works.resShow, Trust['resShow']) * 1.0  / Trust['resShow']
		playTrust = min(works.play, Trust['play']) * 1.0  / Trust['play']
		timeCountTrust = min(works.timeCount, Trust['timeCount']) * 1.0  / Trust['timeCount']
		unsubPlayTrust = min(works.unsubPlay, Trust['play']) * 1.0  / Trust['play']
		conv = 0 if works.resShow <= 0 else works.resShowPlay * 1.0 / works.resShow * resShowTrust
		likeRatio = 0 if works.play <= 0 else works.like * 1.0 / works.play * playTrust
		shareRatio = 0 if works.play <= 0 else works.share * 1.0 / works.play * playTrust
		longPlayRatio = 0 if works.timeCount <= 0 or works.duration <= 0 else works.timeTotal * 1.0 / works.timeCount / works.duration * getPlayCompleteWeight(works.duration) * timeCountTrust
		subRatio = 0 if works.unsubPlay <= 0 else works.sub * 1.0 / works.unsubPlay * unsubPlayTrust
		worksArgs.append([conv, likeRatio, shareRatio, longPlayRatio, subRatio])
	worksArgsMat = mat(worksArgs)
	worksArgsMat[worksArgsMat < 0] = 0
	worksMat = imatrix.inOneDivOffStray(worksArgsMat, 0.002)
	worksMatFinal = worksMat[:, 0] * Weight['conv'] + worksMat[:, 1] * Weight['like'] + worksMat[:, 2] * Weight['share'] + worksMat[:, 3] * Weight['longPlay'] + worksMat[:, 4] * Weight['sub']

	for index, works in enumerate(worksList):
		works.score = worksMatFinal[index, 0]
		works.nzConver = worksMat[index, 0]
		works.nzComplete = worksMat[index, 3]
		works.nzSubscribe = worksMat[index, 4]
		works.nzLike = worksMat[index, 1]
		works.nzShare = worksMat[index, 2]

def updateWeight(weight):
	global Weight
	Weight = weight

def calHotV2(worksList):
	calWorksScore(worksList)

	hotList = {}
	for index, works in enumerate(worksList):
		vid = works.vid
		hotData = {}
		hotData['vid'] = works.vid
		hotData['aid'] = works.aid
		hotData['title'] = works.title
		hotData['hot'] = works.score
		hotData['exposure'] = works.resShow
		hotData['converRatio'] = 0 if works.resShow <= 0 else min(works.resShowPlay * 1.0 / works.resShow, 1)
		hotData['completeRatio'] = 0 if works.timeCount <= 0 or works.duration <= 0 else min(works.timeTotal * 1.0 / works.timeCount / works.duration, 1)
		hotData['click'] = works.resShowPlay
		hotData['like'] = works.like
		hotData['share'] = works.share
		hotData['play'] = works.play
		hotData['subscribeRatio'] = 0 if works.unsubPlay <= 0 else works.sub * 1.0 / works.unsubPlay
		hotData['isNew'] = works.publishTime < 72 and works.resShow <= 1000
		hotData['nzConver'] = works.nzConver
		hotData['nzComplete'] = works.nzComplete
		hotData['nzSubscribe'] = works.nzSubscribe
		hotData['nzLike'] = works.nzLike
		hotData['nzShare'] = works.nzShare
		hotList[vid] = hotData

	hotListFinal = {}
	for index, item in enumerate(sorted(hotList.items(), key=lambda x: x[1]['hot'], reverse=True)):
		item[1]['ranking'] = index + 1
		hotListFinal[item[0]] = item[1]

	return hotListFinal

def getPlayCompleteWeight(duration):
	if duration <= 30:
		return 0.6 + duration / 30 * 0.2
	if duration <= 60:
		return 0.8 + (duration - 30) / 30 * 0.1
	if duration <= 120:
		return 0.9 + (duration - 60) / 60 * 0.05
	if duration <= 300:
		return 0.95 + (duration - 120) / 180 * 0.05
	return 1.0












def calHot(dauFactor, newShowMax, subjectDict, worksDict):
	subjectAids, subjectHotMat = calSubjectHot(subjectDict)
	worksVids, worksAids, worksHotMat, worksRate = calWorksHot(worksDict, dauFactor, newShowMax)

	shArray = []
	for index, aid in enumerate(worksAids):
		shArray.append([subjectHotMat[subjectAids.index(aid), 0] * worksDict[worksVids[index]]['durationAvgPlay']])

	shm = imatrix.inOneDiv(mat(shArray))
	whm = imatrix.inOneDiv(worksHotMat)

	#worksNew = {}
	for index, vid in enumerate(worksVids):
		baseHot = shm[index, 0] * SubjectTotalWeight #* len(subjectDict) / len(worksDict)
		actionHot = whm[index, 0]

		works = worksDict[vid]

		decayRatio = getDecayRatio(works['publishTime'])

		works['vid'] = vid
		works['totalHot'] = (baseHot + actionHot) * decayRatio
		works['baseHot'] = baseHot
		works['actionHot'] = actionHot
		works['decayRatio'] = decayRatio
		works['baseRate'] = worksRate[index, 0]

		works['isNew'] = works['publishTime'] < 72 and works['show'] <= newShowMax

	mHotList = {}
	aidDecays = {}
	for item in sorted(worksDict.items(), key=lambda x: x[1]['totalHot'], reverse=True):
		if index >= 50000:
			break
		works = item[1]
		aid = works['aid']
		if aidDecays.has_key(aid) and aidDecays[aid] < 0.25:
			aidDecays[aid] += SameAidDecay
		else:
			aidDecays[aid] = 0
		works['hot'] = int((1 - aidDecays[aid]) * works['totalHot'] * 100000) + calLowerBound(works['recShowPlay'], works['recShow'])
		mHotList[item[0]] = works

	hotList = {}
	for index, item in enumerate(sorted(mHotList.items(), key=lambda x: x[1]['hot'], reverse=True)):
		item[1]['ranking'] = index + 1
		hotList[item[0]] = item[1]
		'''
		for i in range(500):
			info = item[1].copy()
			info['vid'] = item[0] + str(i)
			hotList[item[0] + str(i)] = info
		'''

	#if hotList.has_key('5fe50cdd8028734584f0832d5338bfe5'):
	#	hotList['5fe50cdd8028734584f0832d5338bfe5']['hot'] = 200000

	return hotList

def calLowerBound(pos, n):
	if n == 0:
		return 0
	z = 1.96
	pos = min(pos, n)
	phat = 1.0 * pos / n
	return (phat + z * z/(2 * n)  -  z * math.sqrt((phat * (1 - phat) + z * z/(4 * n)) / n))/(1 + z * z / n)

def calSubjectHot(subjectDict):
	subjectAids = []
	subjectArgs = []
	for aid, subject in subjectDict.items():
		subjectAids.append(aid)
		subjectArgs.append(subject['statis'])
	subjectMat = imatrix.inOne(mat(subjectArgs))
	subjectHotMat = multiply((subjectMat[:, SubjectIndexs['count']] * SubjectWeight['count'] + subjectMat[:, SubjectIndexs['play']] * SubjectWeight['play'] + subjectMat[:, SubjectIndexs['replay']] * SubjectWeight['replay']), subjectMat[:, SubjectIndexs['conv']])
	return subjectAids, subjectHotMat

def calWorksHot(worksDict, dauFactor, newShowMax):
	worksVids = []
	worksAids = []
	worksArgs = []
	worksForceCredible = []
	for vid, works in worksDict.items():
		worksVids.append(vid)
		worksAids.append(works['aid'])
		worksArgs.append(works['statis'])
		worksForceCredible.append([1 if works['show'] > newShowMax else 0])
	worksMat = mat(worksArgs)
	worksBaseMat = imatrix.inOne(worksMat[:, [WorksIndexs['play'], WorksIndexs['like'], WorksIndexs['shareF'], WorksIndexs['shareI'], WorksIndexs['replay'], WorksIndexs['longTime'], WorksIndexs['subAdd']]])

	worksActionMat = worksBaseMat[:, WorksIndexs['play']] * WorksWeight['play'] + worksBaseMat[:, WorksIndexs['like']] * WorksWeight['like'] + worksBaseMat[:, WorksIndexs['shareF']] * WorksWeight['shareF'] + worksBaseMat[:, WorksIndexs['shareI']] * WorksWeight['shareI'] + worksBaseMat[:, WorksIndexs['replay']] * WorksWeight['replay']
	worksForceMat = multiply(multiply(multiply(worksBaseMat[:, WorksIndexs['longTime']] * WorksWeight['longTime'] + worksBaseMat[:, WorksIndexs['subAdd']] * WorksWeight['subAdd'], worksMat[:, WorksIndexs['playTimeAvg']]), worksMat[:, WorksIndexs['conv']]), mat(worksForceCredible))

	return worksVids, worksAids, worksActionMat * dauFactor + worksForceMat * (11 - dauFactor), getWorksRate(worksMat[:, [WorksIndexs['duration'], WorksIndexs['play']]])

def getDecayRatio(publishTime):
	return 1 - 1 / (1 + math.exp((TimeDecay['half'] - publishTime) / TimeDecay['flutter']))

def getWorksRate(mat):
	#TODO::目前还没有统计size
	total = mat[:,1].sum(axis=0)[0,0]
	avg = multiply(mat[:,0], mat[:,1]).sum(axis=0)[0,0] / total
	vari = sqrt(multiply(square(mat[:,0] - avg), mat[:,1]).sum(axis=0)[0,0] / total)
	return exp(-square(mat[:,0] - avg) / 2 / square(vari)) * (1 / math.sqrt(2 * math.pi) / vari)

'''

def calHot(subjectDict, worksDict, dau):
	worksVid = []
	worksAid = []
	matArray = []
	timeArray = []
	changeArray = []
	worksTotalTime = 0
	worksTimeCount = 0
	durationArray = []
	for works in worksDict.values():
		worksVid.append(works.vid)
		worksAid.append(works.subject.aid)
		matArray.append([len(works.playUids), works.like, len(works.shareFUids), len(works.shareIUids), len(works.replyPlayUids), len(works.longTimeUids), works.subAdd])
		timeArray.append([0 if works.timeCount == 0 else works.totalTime * 1.0 / works.timeCount])
		changeArray.append([0 if works.show == 0 else works.showPlay * 1.0 / works.show])
		worksTotalTime += works.totalTime
		worksTimeCount += works.timeCount
		durationArray.append([works.duration, len(works.playUids)])

	durationMat = mat(durationArray)
	durationTotal = durationMat[:,1].sum(axis=0)[0,0]
	durationAvg = multiply(durationMat[:,0], durationMat[:,1]).sum(axis=0)[0,0] / durationTotal
	durationVari = sqrt(multiply(square(durationMat[:,0] - durationAvg), durationMat[:,1]).sum(axis=0)[0,0] / durationTotal)
	durationRate = exp(-square(durationMat[:,0] - durationAvg) / 2 / square(durationVari)) * (1 / math.sqrt(2 * math.pi) / durationVari)
	#print(concatenate([durationRate, durationMat[:,0]], axis=1))

	worksTimeAvg = worksTotalTime * 1.0 / worksTimeCount

	timeMat = mat(timeArray) / worksTimeAvg
	changeMat = mat(changeArray)
	worksArgsMat = imatrix.inOne(mat(matArray))

	worksMat = mat(zeros((len(matArray), 3)))
	worksMat[:, 0] = worksArgsMat[:, 0] * 1 + worksArgsMat[:, 1] * 5 + worksArgsMat[:, 2] * 10 + worksArgsMat[:, 3] * 15 + worksArgsMat[:, 4] * 5
	worksMat[:, 1] = multiply(multiply(worksArgsMat[:, 5] * 10 + worksArgsMat[:, 6] * 20, timeMat), changeMat)

	rate = 0
	for index in range(1, 5):
		rate += (dau[index] - dau[index + 1]) * 1.0 / dau[index + 1]
	activeDiv = dau[1] * (1 + rate / 5) * 0.4
	a = 1 / (5.5 * activeDiv)
	factor = min(10, max(1, 1 / (a * dau[0])))

	worksMat = imatrix.inOne(worksMat)
	worksMatFinal = worksMat[:, 0] * factor + worksMat[:, 1] * (11 - factor)
	worksMatFinalOne = imatrix.inOne(worksMatFinal)

	subjectAids = []
	subjectArray = []
	for subject in subjectDict.values():
		subjectAids.append(subject.aid)
		subjectArray.append(subject.getArgs()[1:])

	subjectMat = mat(subjectArray)
	subjectMatOne = imatrix.inOne(subjectMat)

	subjectMatFinal = multiply((subjectMatOne[:, 0] * 20 + subjectMatOne[:, 1] * 1 + subjectMatOne[:, 2] * 5), subjectMat[:, 3]) * durationRate[index, 0]
	subjectMatFinalOne = imatrix.inOne(subjectMatFinal)

	worksHots = []
	for index, aid in enumerate(worksAid):
		worksInfo = []
		worksInfo.append(worksVid[index])
		worksInfo.append((worksMatFinalOne[index, 0] + subjectMatFinalOne[subjectAids.index(aid), 0] * 0.3) * worksDict[worksVid[index]].getDecayRatio())
		worksInfo.append(worksMatFinalOne[index, 0])
		worksInfo.append(subjectMatFinalOne[subjectAids.index(aid), 0])
		worksInfo.append(worksDict[worksVid[index]].getDecayRatio())
		worksInfo.append(durationRate[index, 0])
		worksInfo = worksInfo + worksDict[worksVid[index]].getArgs()[1:]
		worksHots.append(worksInfo)
	print(len(worksHots))
	return worksHots

	'''