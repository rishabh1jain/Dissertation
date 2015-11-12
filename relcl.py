import util

#Converting to format [word][rel] = List of all words related to word with the given relation
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

def find_relcl_rel(edges,out_edges_dict):
	if 'acl:relcl' in edges:
		return edges["acl:relcl"]
	else:
		return False

def process_nmods(out_edges_dict,nmod):
	case = ""
	nmod_dependents = [nmod]	
	for key in out_edges_dict[nmod]:
		if "case" in key:
			case = out_edges_dict[nmod][key]
		elif "nmod" in key:
			nmod_dependents = list(set(nmod_dependents)|set(process_nmods(out_edges_dict,out_edges_dict[nmod][key][0])))
		else:#NON CASE DEPENDENTS OF NMOD LIKE DETERMINERS etc
			nmod_dependents = list(set(nmod_dependents) |set(out_edges_dict[nmod][key]))
	nmod_dependents = list(set(nmod_dependents) |set(case))
	return nmod_dependents

def get_all_out_edges_recursively_except_appos_helper(out_edges_dict,whose,out_edges):
	if whose not in out_edges:
		return []
	else:
		temp = []
		for out_edge in out_edges[whose]:
			if "appos" not in out_edge[0]:
				temp.append(out_edge[1])
	return temp

def get_all_out_edges_recursively_except_appos(out_edges_dict,whose, out_edges):
	temp = get_all_out_edges_recursively_except_appos_helper(out_edges_dict,whose, out_edges)
	if len(temp) == 0:
		return []
	else:
		temp1 = temp
		for k in temp:
			temp1 = list(set(temp1)| set(get_all_out_edges_recursively_except_appos(out_edges_dict, k, out_edges,)))
		return temp1

def extract_noun_modifiers(out_edges_dict, noun,out_edges): #For getting the dedendent of argument1 and argument2
	modifiers = {}
	modifiers["non-nmods"] = []
	modifiers["nmods"] = []
	if noun not in out_edges_dict:
		return modifiers
	for rel in out_edges_dict[noun]:
		if ("appos" not in rel and "nmod" not in rel and "relcl" not in rel) or "poss" in rel: #Avoiding revist to relcl
			for j in out_edges_dict[noun][rel]:
				modifiers["non-nmods"] = list(set([j]) | set(modifiers["non-nmods"]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,j, out_edges)))
		elif "nmod" in rel:
			for each_nmod in out_edges_dict[noun][rel]:
				modifiers["nmods"] = list(set(modifiers["nmods"]) | set (process_nmods(out_edges_dict,each_nmod)))
	return modifiers

#TODO: Take care of copular cases.
def extract_relevant_predicate_relations(out_edges_dict,pred,out_edges):
#In most of the cases, the predicates are aux + verb or aux + adj.
	if "aux" in out_edges_dict[pred]:
		return out_edges_dict[pred]["aux"]
	else:
		return []

def extract_second_argument(out_edges_dict,pred,out_edges):
	pred_dobj_and_its_dependents = []
	pred_advmod = []
	pred_iobj_and_its_dependents = []
	pred_advcl_and_its_dependents = []
	pred_xcomp_and_its_dependents = []
	pred_ccomp_and_its_dependents = []
	pred_nmod_and_its_dependents = []

	if "dobj" in out_edges_dict[pred]: #Assuming there is only one word related with the relation dobj
		temp = out_edges_dict[pred]["dobj"][0]
		modifiers = extract_noun_modifiers(out_edges_dict,temp,out_edges)
		pred_dobj_and_its_dependents = list(set([temp]) | 
				set(modifiers["nmods"]) | set(modifiers["non-nmods"])) #modifiers include acl, relcl

	if "advmod" in out_edges_dict[pred]: 
		for j in out_edges_dict[pred]["advmod"]: #multiple adverbs He is eating slowly,happily.
			temp = j
			temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
			pred_advmod.append(temp)

	if "iobj" in out_edges_dict[pred]: 
		temp = out_edges_dict[pred][0] #Assuming only one iobj
		modifiers = extract_noun_modifiers(out_edges_dict,temp,out_edges)
		pred_iobj_and_its_dependents = list(set([temp]) | 
				set(modifiers["nmods"]) | set(modifiers["non-nmods"]))

	if "advcl" in out_edges_dict[pred]: 
		for j in out_edges_dict[pred]["advcl"]: #multiple adverbs He is eating slowly,happily.
			temp = j
			temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
			pred_advcl_and_its_dependents.append(temp)

	if "xcomp" in out_edges_dict[pred]: 
		for j in out_edges_dict[pred]["xcomp"]: #multiple adverbs He is eating slowly,happily.
			temp = j
			temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
			pred_xcomp_and_its_dependents.append(temp)

	if "ccomp" in out_edges_dict[pred]: 
		for j in out_edges_dict[pred]["ccomp"]: #multiple adverbs He is eating slowly,happily.
			temp = j
			temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
			pred_ccomp_and_its_dependents.append(temp)

	#Since there can be n types of nmod depdency, we need to have this loop :(
	for rel in out_edges_dict[pred]:
		if "nmod" in rel:
			for each_nmod in out_edges_dict[pred][rel]:
				pred_nmod_and_its_dependents = list(set(pred_nmod_and_its_dependents) | 
														set (process_nmods(out_edges_dict,each_nmod)))


	print "---------"
	print "DOBJ", pred_dobj_and_its_dependents
	print "ADVMOD", pred_advmod
	print "IOBJ", pred_iobj_and_its_dependents
	print "ADVCL", pred_advcl_and_its_dependents
	print "XCOMP", pred_xcomp_and_its_dependents
	print "NMODS", pred_nmod_and_its_dependents
	print "---------"


#TODO Take care of copular verb case,  He is a bright student. Here the root is student. NOUN as the governor of nsubj
def find_relcl(out_edges, in_edges, edges,sentence):
	out_edges_dict = convert_out_edges(out_edges)
	relations = find_relcl_rel(edges,out_edges_dict)
	if relations == False:
		return 0
	w_words = ["which", "whom","where","when"]
	for rel in relations:
		sub = rel[0]
		pred = rel[1]
		print "FIRST ARGUMENT", sub, extract_noun_modifiers(out_edges_dict, sub,out_edges)
		print "PREDICATE", pred, extract_relevant_predicate_relations(out_edges_dict,pred,out_edges)
		print "SECOND ARGUMENT"
		extract_second_argument(out_edges_dict,pred,out_edges)
		

		#dobj and adverbcl advmod and acl are argu2
		
		
		
#Note: Argument 2 can be XCOMP, CCOMP, ADVMOD, ADVCL, DOBJ, ACL
#ccomp subject may be w word He is eating which is good
#interesting xcomp He is eating to go there to meet him. meet -> go xcomp there -> go advmod
#He was there when I left. 