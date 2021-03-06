import ujson as json
import sys
import gzip
from collections import defaultdict, OrderedDict
import argparse
import os
import matplotlib.pyplot as plt
import numpy as np

direction = ["out", "in"]
nonPresenceField = ["content-type", "user-agent", "accept-language", "server", "code"]
skipField = ["body", "method", "version", "uri", "reason"]
timeScale = 0

def ProcessHTTP(inPathName, fileName, http):
	global timeScale
	json_file = "%s%s" % (inPathName, fileName)
	#print("processing HTTP for %s" %(json_file)) #verbose
	#read each line and convert it into dict
	total = 0
	lineno = 0
	with gzip.open(json_file,'r') as fp:
		for line in fp:
			lineno = lineno + 1
			#print lineno
			try:
				tmp = json.loads(line)
			except:
				continue
			if ('version' in tmp) or ("http" not in tmp):
				continue
			#assert(int(tmp["dp"]) == 80 or int(tmp["sp"]) == 80)
			resp = tmp["http"]
			total += len(resp)
			startTime = tmp["time_start"]
			if timeScale == 0:
				timeline = 0
			else:
				timeline = (startTime)/(timeScale*60)*(timeScale*60)
			if timeline not in http:
				http[timeline] = defaultdict()
			for h in resp:
				for d in direction:
					if d not in h:
						continue
					for kv in h[d]:
						#assert(len(kv.keys())==1)
						key = (list(kv.keys()))[0]
						field = key.lower()
						if field in skipField:
							continue
						value = kv[key] 
						if field in nonPresenceField:
							if field not in http[timeline]:
								http[timeline][field] = defaultdict()
							#handle the value
							if field == "server":
								value = (value.split(' '))[0]
								value = (value.split('/'))[0]
								if value[0:3] == "ECS":
									value = "ECS"
							elif field == "user-agent":
								value = (value.split(' '))[0]
							elif field == "content-type":
								if value[0:19] == "multipart/form-data":
									value = "multipart/form-data"
							#record value
							try:
								http[timeline][field][value] += 1
							#if value not in http[timeline][field]: 
							except KeyError:
								http[timeline][field][value] = 1	
						else:
							try:
								http[timeline][field] += 1
							#if field not in http[timeline]:
							except KeyError:
								http[timeline][field] = 1
								
	try:
		http["totalHTTP"] += total
	#if "totalHTTP" not in http:
	except KeyError:
		http["totalHTTP"] = total
		

def saveToJson(outPathName, fileName, http):
	#print(http[0].items())
	#http = OrderedDict(sorted(http.items(), key=lambda t: t[0]))
	fname = "%s%s_%s_HTTP.json" % (outPathName, (fileName.split('.'))[0], str(timeScale))
	#print("save JSON to " + fname) #verbose
	with open(fname, 'w') as fp:
		json.dump(http, fp)
		

def Analyze(inputFolder):
	global timeScale
	#setup input folder and output folders
	if inputFolder == None or not os.path.isdir(inputFolder):
		print("No valid input folder!")
		return
	else:
		joyFolder = inputFolder
		if not joyFolder.endswith('/'):
			joyFolder += '/'
	parentFolder = os.path.abspath(os.path.join(joyFolder, os.pardir))
	if not parentFolder.endswith('/'):
		parentFolder += '/'
	HTTP_JSON_Folder = "%sHTTP_JSON/" % parentFolder
#	HTTP_Figure_Folder = "%sHTTP_Figure/" % parentFolder
	if not os.path.exists(HTTP_JSON_Folder):
		os.mkdir(HTTP_JSON_Folder)
#	if args.figure:
#		if not os.path.exists(HTTP_Figure_Folder):
#			os.mkdir(HTTP_Figure_Folder)

	#check timeScale
#	if args.timeScale == None:
	timeScale = 0
#	else:
#		timeScale = int(args.timeScale)

	#check if output JSON
#		if args.allFile == True: 
#			http = defaultdict()
#			allFileName = ""
	files = os.listdir(joyFolder)
	for item in files:
#			if args.allFile == True: 
#				allFileName += (item.split('.'))[0] + "-"
		try:
			http = defaultdict()
			ProcessHTTP(joyFolder, item, http)
			saveToJson(HTTP_JSON_Folder, item, http)
		except:
			print("error, skip")
			continue
#		if args.allFile == True:
#			allFileName +=  ".json"
#			saveToJson(HTTP_JSON_Folder, allFileName, http)

