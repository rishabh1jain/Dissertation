import util 

w_words = ["who","which","whom","why","what"]
def extract_relevant_predicate_relations(out_edges_dict,pred,out_edges):
#In most of the cases, the predicates are aux + verb or aux + adj.
	if "aux" in out_edges_dict[pred]:
		return out_edges_dict[pred]["aux"]
	else:
		return []

def find_nsubj_rel(edges,out_edges_dict):
	if 'nsubjpass' in edges:
		return edges["nsubjpass"]
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
	if "auxpass" in enhanced_out_edges[nsubj_gov] and not "cop" in enhanced_out_edges[nsubj_gov]: #Aux and the verb would always be together. The futher permutation will be done later when finding second argument
		predicate = predicate + (enhanced_out_edges[nsubj_gov]["auxpass"])
		if "neg" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["neg"]
		if "aux" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["aux"]	
		return False,predicate

	elif "cop" in enhanced_out_edges[nsubj_gov] and not "auxpass" in enhanced_out_edges[nsubj_gov]: #To handle cases when root is adjective
		predicate = enhanced_out_edges[nsubj_gov]["cop"]
		if "neg" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["neg"]
		if "aux" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["aux"]
		return True, predicate

	elif "cop" in enhanced_out_edges[nsubj_gov] and "auxpass" in enhanced_out_edges[nsubj_gov]: #To handle cases when root is adjective
		predicate = enhanced_out_edges[nsubj_gov]["cop"] + enhanced_out_edges[nsubj_gov]["auxpass"]
		if "neg" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["neg"]
		if "aux" in enhanced_out_edges[nsubj_gov]:
			predicate = predicate + enhanced_out_edges[nsubj_gov]["aux"]	
		return True, predicate

	return False, predicate

def get_context(outedges, parent, exception, results):
	temp_context = [parent] + util.get_all_out_edges_with_exception_word_recursively(outedges,parent,exception)
	for each_result in results:
		each_result.append(temp_context)
	return results

def process_noun(noun,pred_with_aux, out_edges, enhanced_all_dependencies, enhanced_out_edges, results):
	#Nouns have only one clausal dependent
	if noun in enhanced_out_edges:
		if "acl" in enhanced_out_edges[noun]:
			for each_acl in enhanced_out_edges[noun]["acl"]:
				temp = [noun] + util.get_specific_edges(out_edges,noun,["det","neg","compound","mwe"]) +[each_acl] + util.get_all_out_edges_with_exception_recursively(out_edges,each_acl,["xcomp"])
				results.append([pred_with_aux,temp])
				if "xcomp" in enhanced_out_edges[each_acl]:
					for each_xcomp in enhanced_out_edges[each_acl]["xcomp"]:
						temp = [noun] + util.get_specific_edges(out_edges,noun,["det","neg","compound","mwe"]) +[each_xcomp] + util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,[])
						results.append([pred_with_aux,temp])

	return results		

def getcomplexpredicates(nsubj_gov,pred_with_aux,out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges):
	results = []
	"""
	TODOs:
	3. dobj with each of its nmod dependents
	4. nmod as the second argument
	5. dobj of ccomp as second argument
	"""
	#1. All the dependents of nsubjgov
	results.append([pred_with_aux,util.get_all_out_edges_with_exception_recursively(out_edges,nsubj_gov,["cop","nsubjpass","auxpass","neg","conj:and","cc","aux","mark"])])

	#2. Only dobj and dobj's dependents
	if "dobj" in enhanced_out_edges[nsubj_gov]:
		for each_dobj in enhanced_out_edges[nsubj_gov]["dobj"]:
			index = each_dobj.rfind('-')
			if each_dobj[0:index] in w_words:
				continue
			temp = [each_dobj] + util.get_all_out_edges_with_exception_recursively(out_edges,each_dobj,[])
			results.append([pred_with_aux,temp])

			#Only dobj
			temp = [each_dobj] + util.get_specific_edges(out_edges,each_dobj,["det","neg","compound","mwe"])
			results.append([pred_with_aux,temp])

			#Since dobj would be noun mostly, we need to process the acl clause seperately as acl clause would contain
			#verb but it wont be involved in any seperate individual relation. We need to have multiple splits(xcomp of acl) etc.
			results = process_noun(each_dobj,pred_with_aux, out_edges, enhanced_all_dependencies, enhanced_out_edges, results)

	if "nmod:agent" in enhanced_out_edges[nsubj_gov]:
		for each_dobj in enhanced_out_edges[nsubj_gov]["nmod:agent"]:
			index = each_dobj.rfind('-')
			if each_dobj[0:index] in w_words:
				continue
			temp = [each_dobj] + util.get_all_out_edges_with_exception_recursively(out_edges,each_dobj,[])
			results.append([pred_with_aux,temp])

			#Only dobj
			temp = [each_dobj] + util.get_specific_edges(out_edges,each_dobj,["det","neg","compound","mwe","case"])
			print temp
			results.append([pred_with_aux,temp])

			#Since dobj would be noun mostly, we need to process the acl clause seperately as acl clause would contain
			#verb but it wont be involved in any seperate individual relation. We need to have multiple splits(xcomp of acl) etc.
			results = process_noun(each_dobj,pred_with_aux, out_edges, enhanced_all_dependencies, enhanced_out_edges, results)

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

			#xcomp without its advcl,advmod and xcomp,acl:relcl
			temp = [each_xcomp] + util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,["advmod","ccomp","xcomp","acl:relcl"])
			results.append([pred_with_aux,temp])

			#xcomp without nmod
			for each_rel in enhanced_out_edges[each_xcomp]:
				if "nmod" in each_rel:
					for each_nmod in enhanced_out_edges[each_xcomp][each_rel]:
						temp = [each_xcomp] + util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,["advmod","ccomp","xcomp",each_rel])
						results.append([pred_with_aux,temp])

			#Ignoring conjunctions
			temp = [each_xcomp] + util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,["advmod","ccomp","xcomp","conj"])
			results.append([pred_with_aux,temp])

			#Treating dobj of xcomp as the second argument
			if "dobj" in enhanced_out_edges[each_xcomp]:
				temp1 = util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,["advmod","ccomp","xcomp","dobj"])
				new_predicate = pred_with_aux + temp1 + [each_xcomp]
				results.append([new_predicate, [enhanced_out_edges[each_xcomp]["dobj"][0]] + util.get_all_out_edges_with_exception_recursively(out_edges,enhanced_out_edges[each_xcomp]["dobj"][0],["acl:relcl"])])

			#Treating xcomp of xcomp as the second argument
			if "xcomp" in enhanced_out_edges[each_xcomp]:
				temp1 = util.get_all_out_edges_with_exception_recursively(out_edges,each_xcomp,["advmod","ccomp","xcomp"])
				new_predicate = pred_with_aux + temp1 + [each_xcomp]
				for new_each_xcomp in enhanced_out_edges[each_xcomp]["xcomp"]:
					temp1 = [new_each_xcomp] + util.get_all_out_edges_with_exception_recursively(out_edges,new_each_xcomp,[])
					results.append([new_predicate,temp1])


			"""
			#Handling conjunctions
			if "conj:and" in enhanced_out_edges[each_xcomp]:
				for each_conj in enhanced_out_edges[each_xcomp]["conj:and"]:
					temp = [each_conj] + util.get_all_out_edges_with_exception_recursively(out_edges,each_conj,["advmod","ccomp","xcomp"])
					results.append([pred_with_aux,temp])
			"""					
			
			

	#5. Each ccomp
	if "ccomp" in enhanced_out_edges[nsubj_gov]:
		for each_ccomp in enhanced_out_edges[nsubj_gov]["ccomp"]:
			temp = [each_ccomp] + enhanced_all_dependencies[each_ccomp]
			temp = [each_ccomp] + util.get_all_out_edges_with_exception_recursively(out_edges,each_ccomp,["conj"])
			results.append([pred_with_aux,temp])
			"""
			if "conj:and" in enhanced_out_edges[each_ccomp]:
				for each_conj in enhanced_out_edges[each_ccomp]["conj:and"]:
					temp = [each_conj] + util.get_all_out_edges_with_exception_recursively(out_edges,each_conj,["advmod","ccomp","xcomp"])
					results.append([pred_with_aux,temp])
			"""
			#dobj of ccomp as second argument
			if "dobj" in enhanced_out_edges[each_ccomp]:
				temp1 = util.get_all_out_edges_with_exception_recursively(out_edges,each_ccomp,["advmod","ccomp","xcomp","dobj","conj:and","cc"]) #TODO: Here I am omitting the conj atm See what can be done. eg The plea was filed on Monday by advocate Ranjana Agnihotri, who alleged that the Delhi Police was not investigating the case properly and that the matter should be transferred to the NIA.
				new_predicate = pred_with_aux + temp1 + [each_ccomp]
				results.append([new_predicate, [enhanced_out_edges[each_ccomp]["dobj"][0]] + util.get_all_out_edges_with_exception_recursively(out_edges,enhanced_out_edges[each_ccomp]["dobj"][0],["acl:relcl"])])

	#6. Each nmod
	for relation in enhanced_out_edges[nsubj_gov]:
		if "nmod" in relation:
			for each_nmod in enhanced_out_edges[nsubj_gov][relation]:
				temp = [each_nmod] + enhanced_all_dependencies[each_nmod]
				results.append([pred_with_aux,temp])

				temp = [each_nmod] + util.get_all_out_edges_with_exception_recursively(out_edges,each_nmod,["conj:and","cc"])
				results.append([pred_with_aux,temp])

				temp = [each_nmod] + util.get_all_out_edges_with_exception_recursively(out_edges,each_nmod,["conj:and","cc","acl:relcl"])
				results.append([pred_with_aux,temp])
				
				"""
				if each_nmod in enhanced_out_edges:
					#Nmod conj dependent would just replace the governor in the relations with everything else same.
					if "conj:and" in enhanced_out_edges[each_nmod]:
						for each_conj in enhanced_out_edges[each_nmod]["conj:and"]:
							temp = [each_conj] + util.get_all_out_edges_with_exception_recursively(out_edges,each_conj,[]) + util.get_all_out_edges_with_exception_recursively(out_edges,each_nmod,["conj:and","cc"])
							results.append([pred_with_aux,temp])
				"""


	#7. Each advmod
	if "advmod" in enhanced_out_edges[nsubj_gov]:
		for each_advmod in enhanced_out_edges[nsubj_gov]["advmod"]:
			temp = [each_advmod] + enhanced_all_dependencies[each_advmod]
			results.append([pred_with_aux,temp])


	return results

def find_nsubjpass(out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges,root):
	out_edges_dict = convert_out_edges(out_edges)
	relations = find_nsubj_rel(edges,out_edges_dict)
	if relations == False:
		return
	results = []
	w_words = ["which", "whom","where","when","who","why","what"]
	for rel in relations:
		results = []
		sub = rel[1]
		#TODO: See if there can be differennt combination of first arguments AND ITS DEPENDENTS.
		first_argument = get_first_argument(sub,out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges)
		is_cop_present, predicate = get_predicate(rel[0], out_edges, in_edges, edges,sentence, enhanced_all_dependencies, enhanced_out_edges)				

		
		#case of presence of auxillary verbs or no cop of auxillary.
		is_ccomp = False
		is_relcl = False
		ccomp_parent = None
		relcl_parent = None
		if rel[0] in in_edges:
			for inedge in in_edges[rel[0]]:
				if inedge[0] == 'ccomp':
					is_ccomp = True
					ccomp_parent = inedge[1]
				elif inedge[0] == 'acl:relcl':
					relcl_parent = inedge[1]
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
			#Adding the context to results
			results = get_context(out_edges, root, [rel[0]], results)
			
		elif is_relcl == True:	
			#change subject to relcl governor and remove nsubj edge and the wword connected by nsubj
			temp_out_edges = out_edges
			temp_enhanced_all_dependencies = enhanced_all_dependencies
			temp_enhanced_out_edges = enhanced_out_edges
			is_w_word_as_sub = False
			is_w_word_as_obj = False
			relcl_value = None
			w_word_index = None
			w_word_value = None
			relcl_index = None
			#Finding new subject
			for inedge in in_edges[rel[0]]:
				if inedge[0] == 'acl:relcl':
					relcl_value = inedge[1]			
			#This temp_argument can be both nsubj or dobj
			temp_argument =[relcl_value] + util.get_specific_edges(out_edges,relcl_value,["det","neg","compound","mwe"])
			if rel[0] in out_edges:
				for k in range(len(out_edges[rel[0]])):
					if out_edges[rel[0]][k][0] == 'nsubj':
						index = out_edges[rel[0]][k][1].rfind('-')
						if out_edges[rel[0]][k][1][0:index] in w_words:
							is_w_word_as_sub = True
							w_word_index = k
							w_word_value = out_edges[rel[0]][k][1]
					
					if out_edges[rel[0]][k][0] == 'dobj':
						index = out_edges[rel[0]][k][1].rfind('-')
						if out_edges[rel[0]][k][1][0:index] in w_words:
							is_w_word_as_obj = True
							w_word_index = k
							w_word_value = out_edges[rel[0]][k][1]
			if relcl_value in out_edges:
				for k in range(len(out_edges[relcl_value])):
					if out_edges[relcl_value][k][0] == 'acl:relcl':
						relcl_index = k
			if is_w_word_as_sub == True:
				temp_out_edges[rel[0]].pop(w_word_index)
				temp_enhanced_all_dependencies[rel[0]].remove(w_word_value)
				first_argument = temp_argument
			elif is_w_word_as_obj == True:
				r = list(temp_out_edges[rel[0]][w_word_index]) 
				r[1] = relcl_value
				temp_out_edges[rel[0]][w_word_index] = tuple(r)
				temp_out_edges[relcl_value].pop(relcl_index)
				temp_enhanced_all_dependencies[rel[0]].remove(w_word_value)
				temp_enhanced_all_dependencies[rel[0]].append(relcl_value)
				temp_enhanced_out_edges[rel[0]]["dobj"] = [relcl_value]
				temp_enhanced_out_edges[relcl_value].pop("acl:relcl",None)
				#Dont change the first argument
			
			results = getcomplexpredicates(rel[0],predicate, temp_out_edges, in_edges, edges,sentence, temp_enhanced_all_dependencies, temp_enhanced_out_edges)
			#Adding the context to results
			results = get_context(out_edges, root, [rel[0]], results)

		grand_finale = []
		for result in results:
			if len(result) == 2:
				k = util.final_ordering(first_argument),util.final_ordering(result[0]),"|", util.final_ordering(result[1])
				if k not in grand_finale:
					print util.final_ordering(first_argument),"|",util.final_ordering(result[0]),"|", util.final_ordering(result[1])
					grand_finale.append(k)
			else:		
				k = util.final_ordering(first_argument),util.final_ordering(result[0]),"|", util.final_ordering(result[1]), "|", "Context :",util.final_ordering(result[2])
				if k not in grand_finale:
					print util.final_ordering(first_argument),"|",util.final_ordering(result[0]),"|", util.final_ordering(result[1]), "|", "Context :",util.final_ordering(result[2])
					grand_finale.append(k)


"""
The plea was filed on Monday by advocate Ranjana Agnihotri, who alleged that the Delhi Police was not investigating the case properly and that the matter should be transferred to the NIA.
"""
		
		