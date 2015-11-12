import requests
import time
import datetime
import json
import nltk
import re 

def get_dump_for_n_days(index,n):
	url = "http://192.168.111.160:9200/"+index+"/_search"
	current_time = str(int(time.time()))
	past_time = str((datetime.date.today() - datetime.timedelta(n)).strftime("%s"))
	current_time = current_time + "000"
	past_time = past_time + "000"
	body = '{"size":500000,"sort":[{"datetime":{"order":"desc","unmapped_type":"boolean"}}],"query":{"filtered":{"query":{"query_string":{"analyze_wildcard":true,"query":"*"}},"filter":{"bool":{"must":[{"range":{"datetime":{"gte":'+past_time+',"lte":'+current_time+'}}}],"must_not":[]}}}},"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"fields":{"*":{}},"fragment_size":2147483647},"aggs":{"2":{"date_histogram":{"field":"datetime","interval":"1d","pre_zone":"+05:30","pre_zone_adjust_large_interval":true,"min_doc_count":0,"extended_bounds":{"min":1443951052846,"max":1445247052846}}}},"fields":["*","_source"],"script_fields":{},"fielddata_fields":["datetime"]}'
	r = requests.post(url,data=body)
	articles = json.loads(r.text)
	return json.dumps(articles["hits"])

def get_documents(indexes,days):
	documents = {}
	for index in indexes:
		articles = get_dump_for_n_days(index,days)
		articles = json.loads(articles)
		documents[index] = articles
	return documents

def get_headlines(indexes,days):
	documents = get_documents(indexes,days)
	headlines = {}
	for index in indexes:
		headlines[index] = []
	for index in documents:
		for document in documents[index]["hits"]:
			temp = document["_source"]["headline"].replace(u'\xa0', u' ').encode('ascii','ignore').replace("\n","")
			if temp not in headlines[index]:
				headlines[index].append(temp)
	return headlines

def convert_to_list(X):
	final_list = []
	for index in X:
		for Y in X[index]:
			final_list.append(Y)
	return final_list

def get_body(indexes,days):
	documents = get_documents(indexes,days)
	body = {}
	for index in indexes:
		body[index] = []
	for index in documents:
		for document in documents[index]["hits"]:
			temp = document["_source"]["body"].replace(u'\xa0', u' ').encode('ascii','ignore').replace("\n","")
			if temp not in body[index]:
				body[index].append(temp)
			else:
				pass
				#print "Already"
				#print temp
	return body

def get_body_and_headlines(indexes,days):
	documents = get_documents(indexes,days)
	body = {}
	for index in indexes:
		body[index] = []
	for index in documents:
		for document in documents[index]["hits"]:
			temp1 = document["_source"]["headline"].replace(u'\xa0', u' ').encode('ascii','ignore').replace("\n","")
			temp = document["_source"]["body"].replace(u'\xa0', u' ').encode('ascii','ignore').replace("\n","")
			m = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', temp)
			m = m[:3]
			temp = ''.join(m)
			temp = temp1 +". "+ temp
			if temp not in body[index]:
				body[index].append(temp)
			else:
				print "Already"
				print temp
	return body

