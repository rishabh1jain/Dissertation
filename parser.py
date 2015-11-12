from corenlp import *
corenlp = StanfordCoreNLP(corenlp_path="./stanford-corenlp-full-2015-04-20/")

import json
import appo
import poss
import nsubj
import relcl

def parse_dependency(temp):
	out_edges = {}
	in_edges = {}
	edges = {}
	POS = {}
	parse = corenlp.parse(temp)
	parse = json.loads(parse)
	POS_temp =  parse["sentences"][0]["parsetree"]

	parse = parse["sentences"][0]["indexeddependencies"]
	del parse[0]
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
	return out_edges,in_edges,edges

def find_appositions(sentence):
	out_edges, in_edges,edges =	parse_dependency(sentence)
	#print edges
	appo.find_appo(out_edges, in_edges, edges,sentence)

def find_possessive(sentence):
	out_edges, in_edges,edges =	parse_dependency(sentence)
	poss.find_poss(out_edges, in_edges, edges,sentence)

def find_nsubj_relations(sentence):
	out_edges, in_edges,edges =	parse_dependency(sentence)
	nsubj.find_nsubj(out_edges, in_edges, edges,sentence)	

def find_relcl_relations(sentence):
	out_edges, in_edges,edges =	parse_dependency(sentence)
	relcl.find_relcl(out_edges, in_edges, edges,sentence)	

while(True):
	find_relcl_relations(raw_input())

