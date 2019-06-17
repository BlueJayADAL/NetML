import numpy as np
import pandas as pd
import random
import copy
import ujson as json
import math
import time
import os
import argparse
from collections import defaultdict, OrderedDict
from daalModel import LR, DF
from sklearn.externals import joblib
#SVM, ANN, RF
#from modelANNGPU import ANNGPU

## Import (Copy and Paste) data from the collectCommonDNS.py, collectCommonTLS.py and collectCommonHTTP.py
## The number of most common features could be varied
#40 common DNS Suffixes and 64 Common DNS TTLS
dnsCommon = {"ttls": {"0": 9, "1": 1, "2": 36, "3": 39, "4": 37, "5": 32, "6": 33, "7": 27, "8": 29, "9": 11, "10": 8, "11": 22, "12": 20, "13": 16, "14": 18, "15": 17, "16": 19, "17": 15, "18": 12, "19": 5, "20": 31, "21": 52, "22": 41, "23": 55, "24": 60, "25": 43, "26": 54, "27": 47, "52": 38, "29": 28, "30": 49, "51": 34, "32": 59, "33": 46, "35": 51, "37": 57, "40": 63, "28": 48, "42": 62, "299": 2, "300": 14, "45": 42, "46": 58, "47": 45, "48": 56, "49": 40, "178": 30, "179": 3, "180": 10, "53": 35, "54": 24, "55": 23, "56": 25, "57": 26, "58": 13, "59": 0, "60": 4, "41": 53, "599": 7, "50": 44, "44": 61, "119": 6, "125": 50, "126": 21}, "suffix": {"www": 14, "co": 15, "cn": 1, "do": 33, "cc": 34, "ca": 4, "site": 32, "io": 7, "in": 12, "cafe": 37, "COM": 31, "ru": 6, "pw": 25, "tv": 22, "top": 26, "net": 2, "gov": 39, "pro": 27, "website": 36, "me": 24, "fr": 8, "http": 35, "uk": 11, "club": 28, "de": 10, "jp": 3, "biz": 20, "br": 13, "x": 9, "org": 5, "ws": 18, "info": 21, "mobi": 19, "camp": 38, "us": 23, "ms": 17, "link": 16, "com": 0, "tt": 30, "se": 29}}
#115 common TLS ciphersuite and 22 Commnon TLS extensions
tlsCommon = {"clientCS": {"cca9": 14, "c02b": 4, "c02c": 9, "cca8": 15, "c02f": 5, "c030": 8, "c009": 11, "c00a": 12, "c013": 0, "c014": 1, "009c": 6, "009d": 10, "002f": 2, "0035": 3, "cc14": 22, "cc13": 23, "cc15": 24, "009e": 18, "0039": 16, "0033": 17, "c011": 19, "c007": 20, "0005": 21, "0004": 25, "000a": 7, "00ff": 13, "009f": 28, "0032": 26, "0038": 27, "dada": 54, "c028": 29, "c024": 30, "00a5": 75, "00a3": 67, "00a1": 76, "006b": 68, "006a": 69, "0069": 77, "0068": 78, "0037": 79, "0036": 80, "ccaa": 91, "c032": 31, "c02e": 32, "c02a": 33, "c026": 34, "c00f": 35, "c005": 36, "003d": 37, "c027": 38, "c023": 39, "00a4": 81, "00a2": 70, "00a0": 82, "0067": 71, "0040": 72, "003f": 83, "003e": 84, "0031": 85, "0030": 86, "c031": 40, "c02d": 41, "c029": 42, "c025": 43, "c00e": 44, "c004": 45, "003c": 46, "c00c": 89, "c002": 90, "c012": 47, "c008": 48, "0016": 73, "0013": 74, "0010": 87, "000d": 88, "c00d": 49, "c003": 50, "eaea": 65, "1a1a": 60, "caca": 58, "5a5a": 64, "3a3a": 52, "4a4a": 57, "8a8a": 62, "fafa": 55, "2a2a": 66, "6a6a": 63, "9a9a": 61, "0a0a": 51, "7a7a": 56, "aaaa": 53, "baba": 59, "5600": 92, "0088": 93, "0087": 94, "0086": 103, "0085": 104, "0084": 95, "009a": 96, "0099": 97, "0098": 105, "0097": 106, "0045": 98, "0044": 99, "0043": 107, "0042": 108, "0096": 100, "0041": 101, "0007": 102, "0015": 109, "0012": 110, "0009": 111, "0014": 112, "0011": 113, "0008": 114, "0006": 115, "0003": 116}, "clientExt": {"ff01": 10, "0000": 3, "0017": 6, "0023": 4, "000d": 2, "0005": 5, "000b": 0, "000a": 1, "0015": 12, "3374": 11, "0012": 8, "0010": 7, "7550": 9, "eaea": 23, "7a7a": 14, "1a1a": 19, "caca": 13, "fafa": 28, "dada": 22, "3a3a": 16, "0a0a": 20, "aaaa": 25, "6a6a": 18, "2a2a": 21, "9a9a": 24, "5a5a": 26, "4a4a": 17, "baba": 27, "8a8a": 15, "000f": 29}, "serverCS": {"cca8": 3, "c02f": 0, "c02b": 1, "009c": 4, "cca9": 2, "c030": 5, "009d": 7, "c014": 6, "002f": 11, "0035": 8, "c028": 9, "cc14": 10, "cc13": 12, "0005": 14, "c013": 15, "c02c": 16, "009e": 13, "0039": 17, "0004": 18, "000a": 20, "0033": 19, "009f": 21}, "serverExt": {"ff01": 0, "0017": 5, "000b": 1, "0023": 3, "0005": 6, "0010": 2, "0000": 4, "0012": 8, "7550": 7, "3374": 9, "000f": 10}}
#HTTP features
#httpCommon = {"code": {"200": 0, "302": 1, "304": 2, "301": 3}, "accept-language": {"en-US,en;q=0.8": 0}, "presence": {"origin": 71, "x-nws-log-uuid": 68, "content-length": 10, "code": 2, "accept-language": 5, "x-requester": 62, "fw-via": 48, "x-cache-lookup": 51, "if-modified-since": 58, "vary": 23, "x-varnish-hits": 42, "accept": 6, "upgrade-insecure-requests": 41, "x-daa-tunnel": 70, "dpool_lb7_header": 53, "via": 19, "strict-transport-security": 75, "x-hits": 59, "p3p": 30, "served-from": 33, "x-via": 32, "access-control-allow-methods": 37, "poolpool4": 64, "x-varnish-cache": 43, "sina-lb": 40, "poolpool3": 65, "user-agent": 4, "transfer-encoding": 27, "etag": 22, "x-requestid": 61, "location": 28, "dpool_header": 54, "cache-control": 12, "x-qhcdn": 72, "x-filesize": 60, "access-control-allow-headers": 36, "fw-cache-status": 50, "x-px": 49, "x-swift-savetime": 56, "x-varnish": 29, "accept-encoding": 3, "x-cache": 26, "access-control-expose-headers": 44, "x-via-cdn": 24, "set-cookie": 21, "accept-ranges": 16, "expires": 14, "eagleid": 46, "fw-global-ttl": 55, "last-modified": 13, "host": 1, "x-xss-protection": 52, "referer": 11, "pragma": 35, "network_info": 25, "date": 8, "access-control-allow-origin": 20, "timing-allow-origin": 31, "x-amz-meta-crc32": 63, "x-amz-cf-id": 76, "x-client-ip": 66, "ohc-response-time": 45, "x-swift-cachetime": 57, "content-encoding": 18, "age": 17, "access-control-max-age": 38, "fss-proxy": 34, "server": 9, "fss-cache": 74, "connection": 0, "sina-ts": 39, "keep-alive": 69, "cookie": 15, "x-frame-options": 73, "x-powered-by": 47, "content-type": 7, "x-server-ip": 67}, "server": {"mws": 7, "gws": 12, "squid": 9, "PWS": 4, "Microsoft-IIS": 8, "NWS_Oversea_AP": 14, "X2_Platform": 13, "nginx": 0, "JSP3": 3, "ECS": 2, "Tengine": 1, "openresty": 11, "Apache": 10, "Suda": 15, "JDWS": 5, "Sina": 6}, "user-agent": {"Mozilla/5.0": 0, "Dalvik/2.1.0": 1}, "content-type": {"image/jpeg": 0, "text/html": 1, "text/html; charset=utf-8": 5, "image/png": 2, "application/octet-stream": 9, "image/gif": 3, "text/html;charset=UTF-8": 10, "application/x-javascript": 4, "text/html; charset=UTF-8": 6, "application/json": 8, "application/javascript;charset=UTF-8": 11, "text/plain": 7}}
httpCommon = {"code": {"201": 9, "200": 0, "204": 4, "206": 8, "301": 3, "302": 1, "304": 2, "404": 7, "400": 5, "408": 6}, "accept-language": {"en-US,en;q=0.8": 0}, "presence": {"origin": 71, "fw-cache-status": 50, "content-length": 10, "code": 2, "accept-language": 5, "pragma": 35, "x-varnish-cache": 43, "x-cache-lookup": 51, "vary": 23, "fw-global-ttl": 55, "accept": 6, "upgrade-insecure-requests": 41, "x-daa-tunnel": 70, "dpool_lb7_header": 53, "via": 19, "x-hits": 59, "p3p": 30, "served-from": 33, "network_info": 25, "cookie": 15, "x-via": 32, "access-control-allow-methods": 37, "x-wap-profile": 78, "content-language": 83, "access-control-max-age": 38, "poolpool4": 64, "x-amz-expiration": 77, "fw-via": 48, "sina-lb": 40, "poolpool3": 65, "user-agent": 4, "x-via-cdn": 24, "lb_header": 79, "x-varnish-hits": 42, "location": 28, "dpool_header": 54, "cache-control": 12, "x-qhcdn": 72, "x-filesize": 60, "access-control-allow-headers": 36, "x-nws-log-uuid": 68, "x-px": 49, "x-varnish": 29, "accept-encoding": 3, "x-cache": 26, "access-control-expose-headers": 44, "transfer-encoding": 27, "set-cookie": 21, "accept-ranges": 16, "expires": 14, "eagleid": 46, "traceid": 82, "last-modified": 13, "host": 1, "x-xss-protection": 52, "x-requestid": 61, "x-requester": 62, "if-modified-since": 58, "date": 8, "access-control-allow-origin": 20, "x-li-pop": 80, "x-li-proto": 81, "timing-allow-origin": 31, "x-swift-cachetime": 57, "x-amz-cf-id": 76, "x-client-ip": 66, "x-swift-savetime": 56, "x-amz-meta-crc32": 63, "etag": 22, "content-encoding": 18, "age": 17, "strict-transport-security": 75, "fss-proxy": 34, "server": 9, "fss-cache": 74, "connection": 0, "sina-ts": 39, "keep-alive": 69, "referer": 11, "x-frame-options": 73, "x-powered-by": 47, "content-type": 7, "x-server-ip": 67, "ohc-response-time": 45}, "user-agent": {"Android": 2, "Mozilla/5.0": 0, "Dalvik/2.1.0": 1}, "server": {"Varnish": 22, "squid": 9, "X2_Platform": 13, "ATS": 18, "AmazonS3": 16, "mws": 7, "NWS_Oversea_AP": 14, "ECS": 2, "Apache": 10, "Sina": 6, "gws": 12, "proxygen": 19, "nginx": 0, "NWS_UGC_HY": 20, "Tengine": 1, "apache": 21, "JDWS": 5, "Suda": 15, "WeiBo": 17, "PWS": 4, "Microsoft-IIS": 8, "JSP3": 3, "openresty": 11}, "content-type": {"text/html; charset=GB2312": 14, "image/jpeg": 0, "application/json;charset=UTF-8": 18, "text/html; charset=UTF-8": 6, "image/png": 2, "text/html;charset=utf-8": 13, "text/html; charset=windows-1251": 12, "application/x-javascript": 4, "application/octet-stream": 9, "application/json": 8, "text/plain": 7, "application/javascript; charset=utf-8": 16, "text/html": 1, "text/html; charset=utf-8": 5, "application/javascript;charset=UTF-8": 11, "application/javascript": 17, "image/gif": 3, "text/html;charset=UTF-8": 10, "text/plain; charset=UTF-8": 19, "text/javascript": 20, "text/css": 15}}
##global variables for binary features
#DNS
numDNSFeature = 0
numCommonDNSTTL = 0
numCommonDNSSuffix = 0
#TLS
numTLSFeature = 0
numCommonTLSClientCS = 0
numCommonTLSClientExt = 0
numCommonTLSServerCS = 0
numCommonTLSServerExt = 0
#HTTP
numHTTPFeature = 0
numCommonHTTPPresence = 0
numCommonHTTPContentType = 0
numCommonHTTPUserAgent = 0
numCommonHTTPServer = 0
numCommonHTTPCode = 0
#times, lengths, byte-distribution
numTimesFeature = 0
numLengthsFeature = 0
numDistFeature = 0
#for enabled feature
dnsDir = ""
tlsDir = ""
httpDir = ""
metaDir = ""
timesDir = ""
lengthsDir = ""
distDir = ""
enableTLS = False
#for analyze the impact of each parameters
impact = []
#for the granularity of http window
timeScale = 0
#for the filter-out of TLS flows
filterOut=[]
#for initialization of the number of META features
#must be aligned with the calculation in analyzeMETA.py
def initNumTimesFeature():
	global impact
	global numTimesFeature
	numTimesFeature = 100
	print("numTimesFeature: " + str(numTimesFeature))
	tmp = []
	for i in range(0, numTimesFeature):
		tmp.append("Times_"+str(i))
	impact += tmp
def initNumLengthsFeature():
	global impact
	global numLengthsFeature
	numLengthsFeature = 100
	print("numLengthsFeature: " + str(numLengthsFeature))
	tmp = []
	for i in range(0, numLengthsFeature):
		tmp.append("Lengths_"+str(i))
	impact += tmp
def initNumDistFeature():
	global impact
	global numDistFeature
	numDistFeature = 256
	print("numDistFeature: " + str(numDistFeature))
	tmp = []
	for i in range(0, numDistFeature):
		tmp.append("Dist_"+str(i))
	impact += tmp


#for intialization of the number of DNS features
#must be aligned with the calculation below!
def initNumDNSFeature():
	global impact
	global numDNSFeature
	# ttls + suffix + alexa + length of domain name + num of numerical characters + num of wildcard or dot + num of IPs returned
	numDNSFeature = (numCommonDNSTTL+1) + (numCommonDNSSuffix+1) + 6 + 1 + 1 + 1 + 1
	print("numDNSFeature: " + str(numDNSFeature))
	#ttls
	tmp = [""] * (numCommonDNSTTL+1)
	for key in dnsCommon["ttls"].keys():
		index = dnsCommon["ttls"][key]
		tmp[index] = "TTLS_" + key
	tmp[numCommonDNSTTL] = "TTLS_Other"
	impact += tmp
	#suffix
	tmp = [""] * (numCommonDNSSuffix+1)
	for key in dnsCommon["suffix"].keys():
		index = dnsCommon["suffix"][key]
		tmp[index] = "Suffix_" + key
	tmp[numCommonDNSSuffix] = "Suffix_Other"
	impact += tmp
	#alexa
	tmp = ["Alexa_100", "Alexa_1000", "Alexa_10000", "Alexa_100000", "Alexa_1000000", "Alexa_None"]
	impact += tmp
	#length of domain name
	tmp = ["LenDomain"]
	impact += tmp
	#num of numerical characters
	tmp = ["NumNumericDomain"]
	impact += tmp
	#num of wildcard or dot
	tmp = ["NumNonAlphaNumericDomain"]
	impact += tmp
	#num of IPs returned
	tmp = ["IPReturned"]
	impact += tmp


def processDNS(dns):	
	global numCommonDNSTTL
	global numCommonDNSSuffix
	dnsDict = defaultdict()
	for key in dns.keys():
		if key == "totalDNS":
			continue
		d = dns[key]
		ips = d['ips']
		ttls = d['ttls']
		for i in range(0, len(ips)):
			ip = ips[i]
			#1 ttls
			ttl = str(ttls[i])
			if ttl in dnsCommon["ttls"]: 
				ttlIdx = dnsCommon["ttls"][ttl]
			else:
				ttlIdx = numCommonDNSTTL
			ttlList = [0] * (numCommonDNSTTL+1)
			ttlList[ttlIdx] = 1
			#2 suffix
			suffix = d['suffix']
			if suffix in dnsCommon["suffix"]:
				suffixIdx = dnsCommon["suffix"][suffix]
			else:
				suffixIdx = numCommonDNSSuffix
			suffixList = [0] * (numCommonDNSSuffix+1)
			suffixList[suffixIdx] = 1
			#3 alexa
			alexaList = [0]*6
			alexa = d['rank']
			if alexa == 100:
				alexaIdx = 0
			elif alexa == 1000:
				alexaIdx = 1
			elif alexa == 10000:
				alexaIdx = 2
			elif alexa == 100000:
				alexaIdx = 3
			elif alexa == 1000000:
				alexaIdx = 4
			else:
				alexaIdx = 5
			alexaList[alexaIdx] = 1
			#4 length of domain name
			lenDN = d['len']
			#5 num of numerical characters
			nNum = d['num']
			#6 num of wildcard or dot
			nNonAlphaNum = d['nonnum']
			#7 num of IPs returned
			nIPs = d['ipCount']
			#integration of all the DNS features
			#concatDNS = ttlList + suffixList + alexaList + [lenDN] + [nNum] + [nNonAlphaNum] + [nIPs]
			concatDNS = ttlList + suffixList + alexaList + [lenDN/float(100)] + [nNum/float(10)] + [nNonAlphaNum/float(10)] + [nIPs/float(10)]
			dnsDict[ip] = concatDNS
	return dnsDict

#for intialization of the number of TLS features
#must be aligned with the calculation below!
def initNumTLSFeature():
	global impact
	global numTLSFeature
	# client Ciphersuite + client Extension + server Ciphersuite + server Extension + \
	# client Public Key Length + number of server certificates + number of SAN names + validity in days + whether self-signed
	numTLSFeature = numCommonTLSClientCS + numCommonTLSClientExt + numCommonTLSServerCS + numCommonTLSServerExt + 1 + 1 + 1 + 1 + 1
	print("numTLSFeature: " + str(numTLSFeature))
	# client Ciphersuite
	tmp = [""] * numCommonTLSClientCS
	for key in tlsCommon["clientCS"].keys():
		index = tlsCommon["clientCS"][key]
		tmp[index] = "clientCS_" + key
	impact += tmp
	# client Extension
	tmp = [""] * numCommonTLSClientExt
	for key in tlsCommon["clientExt"].keys():
		index = tlsCommon["clientExt"][key]
		tmp[index] = "clientExt_" + key
	impact += tmp
	# server Ciphersuite
	tmp = [""] * numCommonTLSServerCS
	for key in tlsCommon["serverCS"].keys():
		index = tlsCommon["serverCS"][key]
		tmp[index] = "serverCS_" + key
	impact += tmp
	# server Extension
	tmp = [""] * numCommonTLSServerExt
	for key in tlsCommon["serverExt"].keys():
		index = tlsCommon["serverExt"][key]
		tmp[index] = "serverExt_" + key
	impact += tmp
	# client Public Key Length
	tmp = ["ClientKeyLen"]
	impact += tmp
	# number of server certificates
	tmp = ["NumServerCertificates"]
	impact += tmp
	# number of SAN names
	tmp = ["NumSubjectAltNames"]
	impact += tmp
	# validity in days
	tmp = ["Validity"]
	impact += tmp
	# whether self-signed
	tmp = ["SelfSigned"]
	impact += tmp


def processTLS(tls):
	global numCommonTLSClientCS
	global numCommonTLSClientExt
	global numCommonTLSServerCS
	global numCommonTLSServerExt
	tlsDict = defaultdict()
	for key in tls.keys():
		if key == "totalTLS":
			continue
		#1 client Ciphersuite 
		clientCSList = [0] * numCommonTLSClientCS
		clientCS = tls[key]['clientCS']
		for cs in clientCS:
			csIdx = tlsCommon["clientCS"][cs]
			clientCSList[csIdx] = 1
		#2 client Extension
		clientExtList = [0] * numCommonTLSClientExt
		clientExt = tls[key]['clientExt']
		for ext in clientExt:
			extIdx = tlsCommon["clientExt"][ext]
			clientExtList[extIdx] = 1
		#3 server Ciphersuite 
		serverCSList = [0] * numCommonTLSServerCS
		serverCS = tls[key]['serverCS']
		for cs in serverCS:
			csIdx = tlsCommon["serverCS"][cs]
			serverCSList[csIdx] = 1
		#4 server Extension
		serverExtList = [0] * numCommonTLSServerExt
		serverExt = tls[key]['serverExt']
		for ext in serverExt:
			extIdx = tlsCommon["serverExt"][ext]
			serverExtList[extIdx] = 1
		#5 client Public Key Length
		cKeyLen = tls[key]['clientKeyLen']
		#6 number of server certificates
		numCert = tls[key]['certCount']
		#7 number of SAN names
		numSAN = max(tls[key]['certSubAltNames']) if tls[key]['certSubAltNames'] != [] else 0 
		#8 validity in days
		numValid = max(tls[key]['certValidDays']) if tls[key]['certValidDays'] != [] else 0 
		#9 whether self-signed
		selfSigned = tls[key]['certSelfSigned']
		# Integration of all TLS features
		#tlsConcat = clientCSList + clientExtList + serverCSList + serverExtList + [cKeyLen] + [numCert] + [numSAN] + [numValid] + [selfSigned]
		tlsConcat = clientCSList + clientExtList + serverCSList + serverExtList + [cKeyLen/float(1000)] + [numCert/float(10)] + [numSAN/float(100)] + [numValid/float(10000)] + [selfSigned]
		tlsDict[key] = tlsConcat
	return tlsDict

#for intialization of the number of HTTP features
#must be aligned with the calculation below!
def initNumHTTPFeature():
	global impact
	global numHTTPFeature
	#presence + content-type + user-agent + server + code
	numHTTPFeature = (numCommonHTTPPresence+1) + (numCommonHTTPContentType+1) + (numCommonHTTPUserAgent+1) + (numCommonHTTPServer+1) + (numCommonHTTPCode+1)
	print("numHTTPFeature: " + str(numHTTPFeature))
	#presence
	tmp = [""] * (numCommonHTTPPresence+1)
	for key in httpCommon["presence"].keys():
		index = httpCommon["presence"][key]
		tmp[index] = "presence_" + key
	tmp[numCommonHTTPPresence] = "presence_Other" 
	impact += tmp
	#content-type
	tmp = [""] * (numCommonHTTPContentType+1)
	for key in httpCommon["content-type"].keys():
		index = httpCommon["content-type"][key]
		tmp[index] = "content-type_" + key
	tmp[numCommonHTTPContentType] = "content-type_Other"
	impact += tmp
	#user-agent
	tmp = [""] * (numCommonHTTPUserAgent+1)
	for key in httpCommon["user-agent"].keys():
		index = httpCommon["user-agent"][key]
		tmp[index] = "user-agent_" + key
	tmp[numCommonHTTPUserAgent] = "user-agent_Other"
	impact += tmp
	#server
	tmp = [""] * (numCommonHTTPServer+1)
	for key in httpCommon["server"].keys():
		index = httpCommon["server"][key]
		tmp[index] = "server_" + key
	tmp[numCommonHTTPServer] = "server_Other" 
	impact += tmp
	#code
	tmp = [""] * (numCommonHTTPCode+1)
	for key in httpCommon["code"].keys():
		index = httpCommon["code"][key]
		tmp[index] = "code_" + key
	tmp[numCommonHTTPCode] = "code_Other"
	impact += tmp

def processHTTP(http):	
	global numCommonHTTPPresence
	global numCommonHTTPContentType
	global numCommonHTTPUserAgent
	global numCommonHTTPServer
	global numCommonHTTPCode
	httpTime = OrderedDict()
	for timeline in http.keys():
		if timeline == "totalHTTP":
			continue
		#presence
		presenceList = [0] * (numCommonHTTPPresence+1)
		for field in http[timeline].keys():
			if field == "totalHTTP":
				continue
			if field in httpCommon["presence"]:
				index = httpCommon["presence"][field]
				presenceList[index] = 1
			else:
				presenceList[numCommonHTTPPresence] = 1
		#content-type
		contentTypeList = [0] * (numCommonHTTPContentType+1)
		if "content-type" in http[timeline]:
			for item in http[timeline]["content-type"].keys():
				if item in httpCommon["content-type"]:
					index = httpCommon["content-type"][item]
					contentTypeList[index] = 1
				else:
					contentTypeList[numCommonHTTPContentType] = 1
		#user-agent
		userAgentList = [0] * (numCommonHTTPUserAgent+1)
		if "user-agent" in http[timeline]:
			for item in http[timeline]["user-agent"].keys():
				if item in httpCommon["user-agent"]:
					index = httpCommon["user-agent"][item]
					userAgentList[index] = 1
				else:
					userAgentList[numCommonHTTPUserAgent] = 1
		#server
		serverList = [0] * (numCommonHTTPServer+1)
		if "server" in http[timeline]:
			for item in http[timeline]["server"].keys():
				if item in httpCommon["server"]:
					index = httpCommon["server"][item]
					serverList[index] = 1
				else:
					serverList[numCommonHTTPServer] = 1
		#code
		codeList = [0] * (numCommonHTTPCode+1)
		if "code" in http[timeline]:
			for item in http[timeline]["code"].keys():
				if item in httpCommon["code"]:
					index = httpCommon["code"][item]
					codeList[index] = 1
				else:
					codeList[numCommonHTTPCode] = 1
		#Integration of all HTTP features
		httpConcat = presenceList + contentTypeList + userAgentList + serverList + codeList
		httpTime[timeline] = httpConcat
	return httpTime

#tls is the iteration standard
def mergeFeatures(tls, tlsDict, dnsDict, httpDict, meta):
	global numDNSFeature
	global numTLSFeature
	global numHTTPFeature
	global numTimesFeature
	global numLengthsFeature
	global numDistFeature
	global timeScale
	global filterOut
	feature = []
	for key in tls.keys():
		if key == "totalTLS":
			continue
		dAddr = (key.split('@'))[-1]
		if filterOut != [] and dAddr in filterOut:
			#print "skip " + dAddr
			continue
		if timeScale == 0:
			timeline = str(0)
		else:
			timeline = str((tls[key]["ts_start"]) / (timeScale*60) * (timeScale*60))
		tmp = []
		#tls
		if enableTLS == True:
			tmp += tlsDict[key]
		#dns
		if dnsDir != "":
			if dAddr in dnsDict:
				tmp += dnsDict[dAddr]
			else:
				#tmp += [0]*numDNSFeature
				continue
		#http
		if httpDir != "":
			if timeline in httpDict:
				tmp += httpDict[timeline]
			else:
				continue
		#meta
		if timesDir != "":
			tmp += meta[key]["flowTimes"]
		if lengthsDir != "":
			tmp += meta[key]["flowLengths"]
		if distDir != "":
			tmp += meta[key]["flowByteDist"]
		assert(len(tmp) == (numDNSFeature + numTLSFeature + numHTTPFeature + numTimesFeature + numLengthsFeature + numDistFeature))
		feature.append(tmp)
	return feature

def prepFeature(tls, dns, http, meta):
	#tls
	if enableTLS == True:
		tlsDict = processTLS(tls)
	else:
		tlsDict = defaultdict()
	#dns
	if dnsDir != "":
		dnsDict = processDNS(dns)
	else:
		dnsDict = defaultdict()
	#http
	if httpDir != "":
		httpDict = processHTTP(http)
	else:
		httpDict = OrderedDict()
	feature = mergeFeatures(tls, tlsDict, dnsDict, httpDict, meta)
	return feature

def prepData(select, dataType):
	data = []
	for dataset in select:
		print('Prepare data for %s' %(dataset))
		#tls
		tlsFile = tlsDir + dataset + "_TLS.json"
		with open(tlsFile, 'r') as fpTLS:
			tls = json.load(fpTLS)
			#This is possible now, due to the segfault of Joy
			if tls == {}:
				continue
		#dns
		if dnsDir != "":
			dnsFile = dnsDir + dataset + "_DNS.json"
			with open(dnsFile, 'r') as fpDNS:
				dns = json.load(fpDNS)
		else:
			dns = {}
		#http
		if httpDir != "":
			httpFile = httpDir + dataset + "_"+str(timeScale) + "_HTTP.json"
			with open(httpFile, 'r') as fpHTTP:
				http = json.load(fpHTTP)
				http = OrderedDict(sorted(http.items(), key=lambda t: t[0]))
		else:
			http = OrderedDict()
		#meta
		if metaDir != "":
			metaFile = metaDir + dataset + "_META.json"
			with open(metaFile, 'r') as fpMETA:
				meta = json.load(fpMETA)
		else:
			meta = {}
		#Get all the features from TLS and DNS
		data += prepFeature(tls, dns, http, meta)
	# Generate label based upon benign or malware
	label = []
	if dataType == 0:
		label = [0] * len(data)
	elif dataType == 1:
		label = [1] * len(data)
	return (data, label)

def pullData(select):
	selectMap = json.load(open(select, 'r'))
	pos = prepData(selectMap["Benign"], 0)
	print('positive examples: %s' %(str(len(pos[0]))))
	neg = prepData(selectMap["Malware"], 1)
	print('negative examples: %s' %(str(len(neg[0]))))
	data = pos[0] + neg[0]
	label = pos[1] + neg[1]
	return (data, label)




def main():
	startTime = time.time()
	## Get the number of the most Common Features, since it is copied from these other files
	#DNS
	global dnsDir
	global numDNSFeature
	global numCommonDNSTTL
	global numCommonDNSSuffix
	numCommonDNSTTL = len(list(dnsCommon["ttls"].keys()))
	numCommonDNSSuffix = len(list(dnsCommon["suffix"].keys()))
	#TLS
	global tlsDir
	global enableTLS
	global numTLSFeature
	global numCommonTLSClientCS
	global numCommonTLSClientExt
	global numCommonTLSServerCS
	global numCommonTLSServerExt
	numCommonTLSClientCS = len(list(tlsCommon["clientCS"].keys()))
	numCommonTLSClientExt = len(list(tlsCommon["clientExt"].keys()))
	numCommonTLSServerCS = len(list(tlsCommon["serverCS"].keys()))
	numCommonTLSServerExt = len(list(tlsCommon["serverExt"].keys()))
	#HTTP
	global httpDir
	global numHTTPFeature
	global numCommonHTTPPresence
	global numCommonHTTPContentType
	global numCommonHTTPUserAgent
	global numCommonHTTPServer
	global numCommonHTTPCode
	numCommonHTTPPresence = len(list(httpCommon["presence"].keys()))
	numCommonHTTPContentType = len(list(httpCommon["content-type"].keys()))
	numCommonHTTPUserAgent = len(list(httpCommon["user-agent"].keys()))
	numCommonHTTPServer = len(list(httpCommon["server"].keys()))
	numCommonHTTPCode = len(list(httpCommon["code"].keys()))
	#META
	global metaDir
	global timesDir
	global lengthsDir
	global distDir
	global numTimesFeature
	global numLengthsFeature
	global numDistFeature
	#Impact
	global impact
	#timeScale
	global timeScale
	#filterOut
	global filterOut
	
	## setup parser
	parser = argparse.ArgumentParser(description="Classify the Flows Based Upon DNS and TLS Features", add_help=True)
	parser.add_argument('--workDir', action="store", help="The directory where we store the feature data")
	parser.add_argument('--select', action="store", help="The VALID selection JSON file with \
		                                            both key Malware and key Benign, \
		                                            values are list of datasets")
	parser.add_argument('--input', action="store", help="Test Input Parameters File")
	parser.add_argument('--output', action="store", help="Training Output Parameters File")
	parser.add_argument('--test', action="store_true", default=False, help="Whether Test")
	parser.add_argument('--analyze', action="store_true", default=False, help="Whether only analyze params file without real test")
	parser.add_argument('--classify', action="store_true", default=False, help="Whether Classify")
	parser.add_argument('--model', action="store", help="The machine learning model including LR, SVM and ANN")
	parser.add_argument('--dns', action="store_true", default=False, help="Whether enable DNS feature")
	parser.add_argument('--http', action="store_true", default=False, help="Whether enable HTTP feature")
	parser.add_argument('--tls', action="store_true", default=False, help="Whether enable TLS feature")
	parser.add_argument('--times', action="store_true", default=False, help="Whether enable inter-packet times feature")
	parser.add_argument('--lengths', action="store_true", default=False, help="Whether enable inter-packet lengths feature")
	parser.add_argument('--dist', action="store_true", default=False, help="Whether enable byte distribution feature")
	parser.add_argument('--timeScale', action="store", help="The granularity of time window of HTTP flow in minutes")
	parser.add_argument('--filterOut', action="store", help="The filter-out JSON file")
	args = parser.parse_args()
	#command example
	#python classify.py --workDir=./ --select=./selection/testc.json --classify --output=params.txt  --tls --dns --http
	#python classify.py --workDir=./ --select=./selection/testc.json --test --input=params.txt

	#check the time scale for http flows
	if args.timeScale == None:
		timeScale = 0
	else:
		timeScale = args.timeScale

	#check if the filter exists
	if args.filterOut != None:
		if not os.path.isfile(args.filterOut):
			print("No valid fiter-out JSON file")
			return
		else:
			filterOut = json.load(open(args.filterOut, 'r'))
			filterOut = set(filterOut)

	#check the work directory
	if args.workDir == None or not os.path.isdir(args.workDir):
		print('No valid work directory')
		return
	else:
		workDir = args.workDir
		if not workDir.endswith('/'):
			workDir += '/'
	#We use the TLS_JSON as the iteration standard, hence TLS_JSON directory must exist
	tlsDir = workDir + "TLS_JSON/" 
	if not os.path.isdir(tlsDir):
		print("No valid TLS_JSON directory")
		return

	#Check for classify and test
	if args.classify == False and args.test == False:
		print('At least test or classify')
		return
	if args.classify == True and args.test == True:
		print('Classify and Test cannot work at the same time')
		return
	if args.test == True and (args.input == None or os.path.isdir(args.input)):
		print('Test Needs Input Parameters File')
		return
	if args.classify == True and (args.output == None or os.path.isdir(args.output)):
		print('Classify Needs Output Parameters File')
		return

	#Classify Only
	if args.classify == True:
		#Check if select is enabled
		if args.select == None or not os.path.isfile(args.select):
			print('No valid selection JSON file')
			return

		#check if at least one of the features is enabled
		if args.dns == False and args.http == False and args.tls == False and args.times == False and args.lengths == False and args.dist == False:
			print("At least one feature is required!")
			return

		#tls feature
		if args.tls == True:
			enableTLS = True
			initNumTLSFeature()

		#dns feature  
		if args.dns == True:
			if not os.path.isdir(workDir + "DNS_JSON/"):
				print("No valid DNS_JSON directory")
				return
			else:
				dnsDir = workDir + "DNS_JSON/"
				initNumDNSFeature()
		
		#http feature
		if args.http == True: 
			if not os.path.isdir(workDir + "HTTP_JSON/"):
				print("No valid HTTP_JSON directory")
				return
			else:
				httpDir = workDir + "HTTP_JSON/"
				initNumHTTPFeature()

		#times, lengths and byte-distribution
		if args.times == True or args.lengths == True or args.dist == True:
			metaDir = workDir + "META_JSON/"
			if not os.path.isdir(metaDir):
				print("No valid META_JSON directory")
				return
			else:
				if args.times == True:
					timesDir = metaDir
					initNumTimesFeature()
				if args.lengths == True:
					lengthsDir = metaDir
					initNumLengthsFeature()
				if args.dist == True:
					distDir = metaDir
					initNumDistFeature()

		#check the model
		if args.model == None:
			mlModel = LR(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
		else:
			if args.model == "LR":
				mlModel = LR(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
				'''
			elif args.model == "SVM":
				mlModel = SVM(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
			elif args.model == "ANN":
				mlModel = ANN(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
			elif args.model == "ANNGPU":
				mlModel = ANNGPU(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
				'''
			elif args.model == "DF":
				mlModel = DF(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)	
			else:
				print(args.model + " is not supported!")
				return

		#Get the flow feature data
		processStart = time.time()
		d = pullData(args.select)
		processEnd = time.time()
		print("Data prep elapsed in %s seconds" %(str(processEnd - processStart)))
		# train the model
		acc = mlModel.train(d[0], d[1], args.output)
		print("Training and testing accuracy: " + str(acc))
	#Test only
	else:
		processStart = time.time()
		paramMap = json.load(open(args.input, 'r'))
		numTLSFeatureT = paramMap["feature"]["tls"]
		numDNSFeatureT = paramMap["feature"]["dns"]
		numHTTPFeatureT = paramMap["feature"]["http"]
		numTimesFeatureT = paramMap["feature"]["times"]
		numLengthsFeatureT = paramMap["feature"]["lengths"]
		numDistFeatureT = paramMap["feature"]["dist"]
		#tls feature
		if numTLSFeatureT != 0:
			enableTLS = True
			initNumTLSFeature()
			assert(numTLSFeatureT == numTLSFeature)

		#dns feature  
		if numDNSFeatureT != 0:
			if not os.path.isdir(workDir + "DNS_JSON/"):
				print("No valid DNS_JSON directory")
				return
			else:
				dnsDir = workDir + "DNS_JSON/"
				initNumDNSFeature()
				assert(numDNSFeatureT == numDNSFeature)
		
		#http feature
		if numHTTPFeatureT != 0: 
			if not os.path.isdir(workDir + "HTTP_JSON/"):
				print("No valid HTTP_JSON directory")
				return
			else:
				httpDir = workDir + "HTTP_JSON/"
				initNumHTTPFeature()
				assert(numHTTPFeatureT == numHTTPFeature)

		#times, lengths and byte-distribution
		if numTimesFeatureT != 0 or numLengthsFeatureT != 0 or numDistFeatureT != 0:
			metaDir = workDir + "META_JSON/"
			if not os.path.isdir(metaDir):
				print("No valid META_JSON directory")
				return
			else:
				if numTimesFeatureT != 0:
					timesDir = metaDir
					initNumTimesFeature()
					assert(numTimesFeatureT == numTimesFeature)
				if numLengthsFeatureT != 0:
					lengthsDir = metaDir
					initNumLengthsFeature()
					assert(numLengthsFeatureT == numLengthsFeature)
				if numDistFeatureT != 0:
					distDir = metaDir
					initNumDistFeature()
					assert(numDistFeatureT == numDistFeature)

		#check the model
		if args.model == None:
			mlModel = LR(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
		else:
			if args.model == "LR":
				mlModel = LR(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
				'''
			elif args.model == "SVM":
				mlModel = SVM(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
			elif args.model == "ANN":
				mlModel = ANN(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
			elif args.model == "ANNGPU":
				mlModel = ANNGPU(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)
				'''
			elif args.model == "DF":
				mlModel = DF(numTLSFeature, numDNSFeature, numHTTPFeature, numTimesFeature, numLengthsFeature, numDistFeature)	
			else:
				print(args.model + " is not supported!")
				return

		#if args.analyze == False:
		#Get the flow feature data
		
		d = pullData(args.select)
		processEnd = time.time()
		print("Data prep elapsed in %s seconds" %(str(processEnd - startTime)))
		# test the model
		acc = mlModel.test(np.array(d[0]), d[1])
		print("Testing accuracy: " + str(acc))
		'''
		else:
			assert(len(impact) == len(paramMap["coef_"]))
			threshHold = 0
			pos = []
			neg = []
			for i in range(0, len(impact)):
				val = paramMap["coef_"][i]
				if abs(val) > threshHold:
					if val > 0:
						pos.append((impact[i], val))
					else:
						neg.append((impact[i], val))
			pos.sort(key=lambda x: x[1], reverse=True)
			neg.sort(key=lambda x: x[1], reverse=False)
			print("pos impact: ")
			print pos
			print("neg impact: ")
			print neg
		'''
	endTime = time.time()
	print("Program elapsed in %s seconds" %(str(endTime - startTime)))


if __name__ == "__main__":
	main()
