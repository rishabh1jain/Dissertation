def get_all_out_edges_recursivly_helper(out_edges,whose):
	temp = []
	if whose in out_edges:
		for j in out_edges[whose]:
			temp.append(j[1])
		return temp
	return temp
	
def get_all_out_edges_recursivly(out_edges,whose):
	temp = get_all_out_edges_recursivly_helper(out_edges,whose)
	immediate_out_edges = temp
	if len(immediate_out_edges) == 0: #The word itself has no dependents
		return []
	else:
		o = len(immediate_out_edges)
		i = 0
		while(i<o):
			immediate_out_edges = immediate_out_edges + get_all_out_edges_recursivly_helper(out_edges,immediate_out_edges[i])
			o = len(immediate_out_edges)
			i = i + 1
		return immediate_out_edges

def get_all_out_edges_with_exception_recursively_helper(out_edges,whose,exceptions,immediate):
	temp = []
	if whose in out_edges:
		for j in out_edges[whose]:
			if immediate is True and j[0] not in exceptions:
				temp.append(j[1])
			elif immediate is False:
				temp.append(j[1])
		return temp
	return temp

def get_all_out_edges_with_exception_recursively(out_edges,whose,exceptions):
	temp = get_all_out_edges_with_exception_recursively_helper(out_edges,whose,exceptions,True)
	immediate_out_edges = temp
	if len(immediate_out_edges) == 0: #The word itself has no dependents
		return []
	else:
		o = len(immediate_out_edges)
		i = 0
		while(i<o):
			immediate_out_edges = immediate_out_edges + get_all_out_edges_with_exception_recursively_helper(out_edges,immediate_out_edges[i],exceptions,False)
			o = len(immediate_out_edges)
			i = i + 1
		return immediate_out_edges

#This method will be used only with verbs and probably we wont need to put check on exceptions like on nsubj atm
def get_all_right_out_edges_with_exception_recursively_helper(out_edges, whose, exceptions, immediate,root_daddy_number):
	temp = []
	if whose in out_edges:
		for j in out_edges[whose]:
			if immediate is True and j[0] not in exceptions:
				index = j[1].rfind('-')
				this_word_number = int(j[1][index+1:])
				if this_word_number > root_daddy_number:
					temp.append(j[1])
			elif immediate is False:
				temp.append(j[1])		
		return temp
	return temp

def get_all_right_out_edges_with_exception_recursively(out_edges, whose, exceptions):
	root_daddy = whose
	index = root_daddy.rfind('-')
	root_daddy_number = int(root_daddy[index+1:])

	temp = get_all_right_out_edges_with_exception_recursively_helper(out_edges,whose,exceptions,True,root_daddy_number)
	immediate_out_edges = temp
	if len(immediate_out_edges) == 0: #The word itself has no dependents
		return []
	else:
		o = len(immediate_out_edges)
		i = 0
		while(i<o):
			immediate_out_edges = immediate_out_edges + get_all_right_out_edges_with_exception_recursively_helper(out_edges,immediate_out_edges[i],exceptions,False,root_daddy_number)
			o = len(immediate_out_edges)
			i = i + 1
		return immediate_out_edges


def get_all_left_out_edges_with_exception_recursively_helper(out_edges, whose, exceptions, immediate,root_daddy_number):
	temp = []
	if whose in out_edges:
		for j in out_edges[whose]:
			if immediate is True and j[0] not in exceptions:
				index = j[1].rfind('-')
				this_word_number = int(j[1][index+1:])
				if this_word_number < root_daddy_number:
					temp.append(j[1])
			elif immediate is False:
				temp.append(j[1])
		return temp
	return temp

def get_all_left_out_edges_with_exception_recursively(out_edges, whose, exceptions):
	root_daddy = whose
	index = root_daddy.rfind('-')
	root_daddy_number = int(root_daddy[index+1:])

	temp = get_all_left_out_edges_with_exception_recursively_helper(out_edges, whose, exceptions, True, root_daddy_number)
	immediate_out_edges = temp
	if len(immediate_out_edges) == 0: #The word itself has no dependents
		return []
	else:
		o = len(immediate_out_edges)
		i = 0
		while(i<o):
			immediate_out_edges = immediate_out_edges + get_all_left_out_edges_with_exception_recursively_helper(out_edges, immediate_out_edges[i], exceptions, False, root_daddy_number)
			o = len(immediate_out_edges)
			i = i + 1
		return immediate_out_edges

def get_all_in_edges(in_edges, whose):
	temp = []
	for j in in_edges[whose]:
		temp.append(j)
	return temp



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

def final_ordering(to_order):
	temp = []
	for i in to_order:
		index = i.rfind('-')
		temp.append((i[0:index],int(i[index+1:])))
	
	temp = sorted(temp,key=lambda x: x[1])
	output = ""
	for j in temp:
		output = output + j[0] + " "
	return output[:-1]

def remove_duplicates(l):
    return list(set(l))
