
def get_all_out_edges(out_edges, what_is_its_relation, whose):
	temp = []
	try:
		for j in out_edges[whose]:
			if "cc" in j[0] or "conj" in j[0] or ("case" in j[0] and "nmod" not in what_is_its_relation):
				continue
			temp.append(j)
		return temp
	except:
		return []

def get_all_in_edges(in_edges, whose):
	temp = []
	for j in in_edges[whose]:
		temp.append(j)
	return temp

#NOTE: Ignoring conjunction edges at this moment
def get_all_out_edges_recursivly(out_edges,what_is_its_relation,whose):
	temp = get_all_out_edges(out_edges,what_is_its_relation,whose)
	temp1 = temp
	if len(temp1) == 0:
		return []
	else:
		for i in temp1:
			temp1 = temp1 + get_all_out_edges_recursivly(out_edges,i[0], i[1])
		return temp1

def get_particular_relations(edges, whose, what):
	if what not in edges:
		return False
	results = []
	for instances in edges[what]:
		if instances[0] == whose:
			results.append(instances[1])
	if len(results) == 0:
		return False
	return results

def final_ordering(lead,to_order):
	index = lead.rfind('-')
	lead = (lead[0:index],int(lead[index+1:]))
	temp = []
	for i in to_order:
		index = i[1].rfind('-')
		temp.append((i[1][0:index],int(i[1][index+1:])))
	temp.append(lead)
	temp = sorted(temp,key=lambda x: x[1])
	output = ""
	for j in temp:
		output = output + j[0] + " "
	return output[:-1]
