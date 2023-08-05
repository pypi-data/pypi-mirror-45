#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json, time, urllib2
from .. import ilog, es, dataDispose
from hot import *

def startUpdate(isTest, configFileName):
	cycleUpdateHotList(configFileName, isTest)

def cycleUpdateHotList(configFileName, isTest):
	worksHistory, historyTime, endTime = getNewestHistory()
	oriWorksDict = {}
	while True:
		try:
			start = time.time()
			ilog.info('start:' + str(start) + '(' + time.strftime(es.esTimeFormatNoMs, time.localtime(start)) + ')')
			
			#距离上一次0点更新相差25小时再次更新 理论是临晨1点
			if start - historyTime > 25 * 60 * 60:
				#ilog.info('delete post works record: ' + ('success ' if dataDispose.deletePastWorksRecord() else 'fail '))
				ilog.info('update history actions: ' + ('success ' if dataDispose.updateHistoryActions() else 'fail '))
				time.sleep(20)
				worksHistory, historyTime, endTime = getNewestHistory()
				oriWorksDict = {}

			oriWorksDict = getNewestWorksList(oriWorksDict, worksHistory)
			
			endTime = onceUpdateHotList(oriWorksDict, endTime, configFileName, isTest)

			cost = time.time() - start
			ilog.info('-------------------------cost: ' + str(cost) + '---------------------------------')

			maxInterval = 150 if isTest else 600
			if cost < maxInterval:
				time.sleep(maxInterval - cost)
		except Exception as error:
			ilog.info('Error: (' + time.strftime(es.esTimeFormatNoMs, time.localtime(time.time())) + ')' + str(error))
			time.sleep(600)

def getNewestHistory():
	worksHistory = dataDispose.getWorksHistory()
	historyTime = 0 if len(worksHistory) == 0 else worksHistory.values()[0]['time']
	return worksHistory, historyTime, historyTime

def getNewestWorksList(oldOriWorksDict, worksHistory):
	oriWorksDict = {}
	for works in dataDispose.getWorksList():
		vid = works.vid
		if oldOriWorksDict.has_key(vid):
			oriWorksDict[vid] = oldOriWorksDict[vid]
		else:
			oriWorksDict[vid] = works
			if worksHistory.has_key(vid):
				works.updateHistory(worksHistory[vid])
	return oriWorksDict

def onceUpdateHotList(oriWorksDict, startTime, configFileName, isTest):
	endTime = updateHotList(oriWorksDict, startTime, readConfig(configFileName))
	#10秒后通知后台更新
	time.sleep(10)
	noticeServer(isTest)
	if not isTest:
		saveHotTopList()
	return endTime

def updateHotList(oriWorksDict, startTime, config):
	start = time.time()

	dbConfig = es.searchDbConfig()
	ilog.info('hotVids:' + str(len(dbConfig['hotVids'])))

	worksDict = {}
	for vid in dbConfig['hotVids']:
		if oriWorksDict.has_key(vid):
			worksDict[vid] = oriWorksDict[vid]

	endTime = int(time.time())
	newHits = es.searchStatisticsDataByBody("hot_actions", {"query": {"bool": {"must": [{"range": {"createTime": {"gte": startTime, "lt": endTime}}}]}}, "size": 10000})
	for hit in newHits:
		action = hit['_source']
		vid = action['vid']
		if worksDict.has_key(vid):
			worksDict[vid].updateAction(action)

	ilog.info('add new actions finished:' + str(time.time() - start))

	updateWeight(config['weight'])
	
	worksHots = calHotV2(worksDict.values())

	ilog.info('got hot list:' + str(time.time() - start))

	ilog.info('update works hot: ' + ('success ' if es.coverStatisticsData('works_hot', worksHots) else 'fail ') + str(time.time() - start))
	
	ilog.info('update redis works hot: ' + ('success ' if es.updateRedisWorksHots(getRedisWorksHots(worksHots)) else 'fail ') + str(time.time() - start))

	return endTime

def getOldHotVids(config):
	oldHotVids = []
	for hit in es.scrollSearch('works_video_read', 'video', {"query": {"bool": {"must": [{"terms": {"aid": config['aid']['white']}}], "must_not": [{"terms": {"vid": config['vid']['black']}}]}}, "size":1000}):
		oldHotVids.append(hit['_id'])
	return oldHotVids

def getLSWorksHots(worksHots):
	lsWorksHots = {}
	aids = []
	for vid, works in worksHots.items():
		aid = works['aid']
		if aid not in aids:
			aids.append(aid)
			if vid != "481d0641adc124a646ba3800f74153f4":
				lsWorksHots[vid] = works
			if len(aids) == 5:
				break
	return lsWorksHots

def getRedisWorksHots(worksHots):
	redisWorksHots = {}
	aids = []
	for vid, works in worksHots.items():
		aid = works['aid']
		if aid not in aids:
			aids.append(aid)
			redisWorksHots[vid] = works['hot']
	return redisWorksHots

def readConfig(configFileName):
	with open(configFileName, 'r') as f:
		config = json.loads(f.read())
	ilog.info('config: ' + str(config))
	return config

def noticeServer(isTest):
	try:
		noticeUpdate(1, isTest)
		noticeUpdate(2, isTest)
	except urllib2.HTTPError as error:
		ilog.info('urllib2.HTTPError: ' + str(error))

def noticeUpdate(listType, isTest):
	url = 'http://nttest.iduoliao.cn:8080' if isTest else 'https://micro.mitao.iduoliao.cn'
	data = {
		"head":{
     		"@type":"type.googleapis.com/ja.common.proto.AutReqHead",
  			"ver": 1,
  			"platform": 999,
  			"seqid": long(time.time() * 1000)
    	},
    	"type": listType
	}
	headers = {'Content-Type': 'application/json'}
	request = urllib2.Request(url=url+'/recommend/IRecommend/UpdateDataNotice', headers=headers, data=json.dumps(data))
	infoInfo = urllib2.urlopen(request).read()
	ilog.info('notice ' + ('hot' if listType == 1 else 'new') + ' list update resp: ' + str(infoInfo))
	return json.loads(infoInfo)['head']['status'] == 1

def saveHotTopList():
	body = {"sort": [{"ranking": {"order": "asc"}}],"size": 200}
	now = time.strftime('%Y-%m-%dT%H:%M:%S+0800', time.localtime(time.time()))
	print(now)
	topList = {}
	for index, hit in enumerate(es.searchStatisticsDataByBody('works_hot', body, False)):
		info = hit['_source']
		info['time'] = now
		topList[hit['_id'] + '$' + str(now)] = info
	es.updateStatisticsData('works_hot_tops', topList)








