import util 

def find_appo_rel(edges):
	if 'appos' in edges:
		return edges["appos"]
	else:
		return False

def find_appo(out_edges, in_edges, edges,sentence):
	relations = find_appo_rel(edges)
	if relations == False:
		return False
	for rel in relations:
		arg1 = rel[0]
		arg2 = rel[1]
		arg1 = [arg1] + util.get_specific_edges(out_edges,rel[0],["det","neg","compound","mwe"])
		arg2 = [arg2] + util.get_specific_edges(out_edges,rel[1],["det","neg","compound","mwe"])
		print util.final_ordering(arg1),"|", "be","|", util.final_ordering(arg2)


