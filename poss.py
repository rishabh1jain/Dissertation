import util

def find_poss_rel(edges):
	if 'poss' in edges or "nmod:poss" in edges:
		return edges["nmod:poss"]
	else:
		return False

def find_poss(out_edges, in_edges, edges,sentence):
	relations = find_poss_rel(edges)
	if relations == False:
		return False
	else:
		for rel in relations:
			sub = rel[1]
			obj = rel[0]
			sub = [sub] + util.get_specific_edges(out_edges,sub,["det","neg","compound","mwe"])
			obj = [obj] + util.get_specific_edges(out_edges,obj,["det","neg","compound","mwe"])
			if sub[0] == 'w' or sub[0] == 'W':
				temp = in_edges[obj]
				temp = in_edges[temp[0][1]][0][1]
				sub = temp
			print util.final_ordering(sub),"|","has","|",util.final_ordering(obj)
