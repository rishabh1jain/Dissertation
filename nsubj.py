import util 
	
def extract_relevant_predicate_relations(out_edges_dict,pred,out_edges):
#In most of the cases, the predicates are aux + verb or aux + adj.
	if "aux" in out_edges_dict[pred]:
		return out_edges_dict[pred]["aux"]
	else:
		return []

def find_nsubj_rel(edges,out_edges_dict):
	if 'nsubj' in edges:
		return edges["nsubj"]
	else:
		return False

def convert_out_edges(out_edges):
	out_edges_dict = {}
	for key in out_edges:
		out_edges_dict[key] = {}
		for i in out_edges[key]:
			rel = i[0]
			dep = i[1]
			if rel not in out_edges_dict[key]:
				out_edges_dict[key][rel] = []
			out_edges_dict[key][rel].append(dep)
	return out_edges_dict

def get_first_argument(nsubj_dep,out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges):
	return [nsubj_dep] + util.get_all_out_edges_with_exception_recursively(out_edges,nsubj_dep,["appos"])

def get_predicate(nsubj_gov,out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges):
	predicate = [nsubj_gov]
	if "aux" in enhanced_out_edges[nsubj_gov]: #Aux and the verb would always be together. The futher permutation will be done later when finding second argument
		predicate = predicate + (enhanced_out_edges[nsubj_gov]["aux"])
		if "neg" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["neg"]
		return False,predicate
	if "cop" in enhanced_out_edges[nsubj_gov]: #To handle cases when root is adjective
		predicate = enhanced_out_edges[nsubj_gov]["cop"]
		if "neg" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["neg"]
		return True, predicate
	return False, predicate

def getcomplexpredicates(nsubj_gov,pred_with_aux,out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges):
	results = []
	"""
	TODOs:
	1. If a verb has ccomp incoming edge then dont include 'mark'. Include Context. And exclude 'mark'
	2. If a xcomp has xcomp dependency then include first xcomp in predicate and use second xcomp as the second argument. (Recursive actually)
	3. dobj with each of its nmod dependents
	4. nmod as the second argument
	"""
	#1. All the dependents of nsubjgov
	results.append([pred_with_aux,util.get_all_out_edges_with_exception_recursively(out_edges,nsubj_gov,["cop","nsubj","aux","neg"])])
	#2. Only dobj and dobj's dependents
	if "dobj" in enhanced_out_edges[nsubj_gov]:
		for each_dobj in enhanced_out_edges[nsubj_gov]["dobj"]:
			temp = [each_dobj] + enhanced_all_dependencies[each_dobj]
			results.append([pred_with_aux,temp])
	#3. Each advcl

	for relation in enhanced_out_edges[nsubj_gov]:
		if "advcl" in relation:
			for each_advcl in enhanced_out_edges[nsubj_gov][relation]:
				temp = [each_advcl] + enhanced_all_dependencies[each_advcl]
				results.append([pred_with_aux,temp])
				#advcl without its nmod
				temp = [each_advcl] + util.get_all_out_edges_with_exception_recursively(out_edges,each_advcl,["nmod","xcomp"])
				results.append([pred_with_aux,temp])

	#4. Each xcomp
	if "xcomp" in enhanced_out_edges[nsubj_gov]:
		for each_xcomp in enhanced_out_edges[nsubj_gov]["xcomp"]:
			temp = [each_xcomp] + enhanced_all_dependencies[each_xcomp]
			results.append([pred_with_aux,temp])
			#xcomp without its advcl,advmod and xcomp
			temp = [each_xcomp] + util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,["advmod","ccomp","xcomp"])
			results.append([pred_with_aux,temp])
			#TODO: xcomp's dobj as second argument
			temp1 = util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,["advmod","ccomp","xcomp"])

	#5. Each ccomp
	if "ccomp" in enhanced_out_edges[nsubj_gov]:
		for each_ccomp in enhanced_out_edges[nsubj_gov]["ccomp"]:
			temp = [each_ccomp] + enhanced_all_dependencies[each_ccomp]
			results.append([pred_with_aux,temp])

	#6. Each nmod
	for relation in enhanced_out_edges[nsubj_gov]:
		if "nmod" in relation:
			for each_nmod in enhanced_out_edges[nsubj_gov][relation]:
				temp = [each_nmod] + enhanced_all_dependencies[each_nmod]
				results.append([pred_with_aux,temp])

	#7. Each advmod
	if "advmod" in enhanced_out_edges[nsubj_gov]:
		for each_advmod in enhanced_out_edges[nsubj_gov]["advmod"]:
			temp = [each_advmod] + enhanced_all_dependencies[each_advmod]
			results.append([pred_with_aux,temp])


	return results

def find_nsubj(out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges):
	out_edges_dict = convert_out_edges(out_edges)
	relations = find_nsubj_rel(edges,out_edges_dict)
	results = []
	w_words = ["which", "whom","where","when"]
	for rel in relations:
		sub = rel[1]
		#TODO: See if there can be differennt combination of first arguments AND ITS DEPENDENTS.
		first_argument = get_first_argument(sub,out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges)
		is_cop_present, predicate = get_predicate(rel[0], out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges)
		#1. Presence of Cop relation : e.g. He is faster than me #To handle adjective cases.
		if is_cop_present == True: #Then there would be at least two results
			results.append([predicate,[rel[0]] + util.get_all_out_edges_with_exception_recursively(out_edges,rel[0],["cop","nsubj"])])
			predicate = util.get_all_left_out_edges_with_exception_recursively(out_edges,rel[0],["nsubj"])
			second_argument = [rel[0]] + util.get_all_right_out_edges_with_exception_recursively(out_edges,rel[0],[])
			results.append([predicate, second_argument])
			print results
		else:
			#case of presence of auxillary verbs or no cop of auxillary.
			#Checking if its a clausal complement TODO: RELCL
			is_ccomp = False
			is_relcl = False
			if rel[0] in in_edges:
				for inedge in in_edges[rel[0]]:
					if inedge[0] == 'ccomp':
						is_ccomp = True
					elif inedge[0] == 'acl:relcl':
						is_relcl = True

			if is_ccomp == False and is_relcl == False:
				results = getcomplexpredicates(rel[0],predicate, out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges)

			elif is_ccomp == True:
				
				#Remove 'mark' from outedges and #Remove mark element from enhanced_all_dependencies
				temp_out_edges = out_edges
				temp_enhanced_all_dependencies = enhanced_all_dependencies
				is_mark = False
				mark_value = None
				if rel[0] in out_edges:
					for k in range(len(out_edges[rel[0]])):
						if out_edges[rel[0]][k][0] == 'mark':
							is_mark = True #Mark may be absent when ccomp is present
							mark_value = out_edges[rel[0]][k][1]
							break

				if is_mark == True:
					temp_out_edges[rel[0]].pop(k)
					temp_enhanced_all_dependencies[rel[0]].remove(mark_value)
					results = getcomplexpredicates(rel[0],predicate, temp_out_edges, in_edges, edges,sentence, temp_enhanced_all_dependencies, enhanced_out_edges)

			elif is_relcl == True:	
				#TODO
				pass
			

		grand_finale = []
		for result in results:
			k = util.final_ordering(first_argument),util.final_ordering(result[0]),"|", util.final_ordering(result[1])
			if k not in grand_finale:
				print util.final_ordering(first_argument),"|",util.final_ordering(result[0]),"|", util.final_ordering(result[1])
				grand_finale.append(k)
		

		
		