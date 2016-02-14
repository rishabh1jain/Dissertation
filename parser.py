from corenlp import *
corenlp = StanfordCoreNLP(corenlp_path="./stanford-corenlp-full-2015-04-20/")

import json
import appo
import poss
import nsubj
import relcl
import util

words = []
def parse_dependency(temp):
	out_edges = {}
	in_edges = {}
	edges = {}
	enhanced_out_edges = {}
	all_dependencies = {}
	global words
	parse = corenlp.parse(temp)
	parse = json.loads(parse)
	parse = parse["sentences"][0]["indexeddependencies"]
	del parse[0]
	print parse
	for relation in parse:
		rel = relation[0]
		dep = relation[2]
		gov = relation[1]
		if gov not in out_edges:
			out_edges[gov] = []
		out_edges[gov].append((rel, dep))
		if dep not in in_edges:
			in_edges[dep] = []
		in_edges[dep].append((rel, gov))
		if rel not in edges:
			edges[rel] = []
		edges[rel].append((gov,dep))
		if dep not in words:
			words.append(dep)
		if gov not in words:
			words.append(gov)
		if gov not in enhanced_out_edges:
			enhanced_out_edges[gov] = {}
		if rel not in enhanced_out_edges[gov]:
			enhanced_out_edges[gov][rel] = []
		enhanced_out_edges[gov][rel].append(dep)
	return out_edges,in_edges,edges,enhanced_out_edges

def get_all_dependencies(enhanced_out_edges,out_edges,in_edges,edges):
	temp = {}
	global words
	for word in words:
		temp[word] = util.get_all_out_edges_recursivly(out_edges,word)
	return temp

"""
def find_appositions(sentence):
	out_edges, in_edges, edges, enhanced_out_edges = parse_dependency(sentence)
	enhanced_all_dependencies = get_all_dependencies(enhanced_out_edges,out_edges,in_edges,edges)
	appo.find_appo(out_edges, in_edges, edges,sentence)

def find_possessive(sentence):
	out_edges, in_edges,edges =	parse_dependency(sentence)
	poss.find_poss(out_edges, in_edges, edges,sentence)

def find_nsubj_relations(sentence): #Thsi will findnormal nsubj relation along with ccomp and relcl
	out_edges, in_edges, edges, enhanced_out_edges = parse_dependency(sentence)
	enhanced_all_dependencies = get_all_dependencies(enhanced_out_edges,out_edges,in_edges,edges)
	nsubj.find_nsubj(out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges)	

def find_relcl_relations(sentence):
	out_edges, in_edges,edges =	parse_dependency(sentence)
	relcl.find_relcl(out_edges, in_edges, edges,sentence)	
"""

def get_relations(sentence):
	out_edges, in_edges, edges, enhanced_out_edges = parse_dependency(sentence)
	enhanced_all_dependencies = get_all_dependencies(enhanced_out_edges,out_edges,in_edges,edges)
	
	nsubj.find_nsubj(out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges)
	appo.find_appo(out_edges, in_edges, edges,sentence)
	poss.find_poss(out_edges, in_edges, edges,sentence)



while(True):
	get_relations(raw_input())

"""
1. Passive nsubjpass
2. When are you going to meet him?
"""
