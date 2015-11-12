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
		print rel
		#gov_compound = util.get_particular_relations(edges,rel[0],"compound")
		#gov_nn = util.get_particular_relations(edges,rel[0],"nn")
		gov_out_edges = util.get_all_out_edges_recursivly(out_edges,"lead",rel[0])
		dep_out_edges = util.get_all_out_edges_recursivly(out_edges,"lead",rel[1])
		gov_out_edges = list(set(gov_out_edges) - set(dep_out_edges))
		print gov_out_edges
		print dep_out_edges
		for i in range(len(gov_out_edges)):
			if gov_out_edges[i][0]=='appos':
				break
		del gov_out_edges[i]

		arg1 = util.final_ordering(rel[0], gov_out_edges)		
		arg2 = util.final_ordering(rel[1], dep_out_edges)
		print sentence
		print '<',arg1,",", "be",",", arg2,">"
		#print "-----"


