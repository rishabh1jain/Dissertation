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

def find_nsubj_rel(edges,out_edges_dict):
	if 'nsubj' in edges:
		return edges["nsubj"]
	else:
		return False

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
	temp = get_all_out_edges_recursively_except_appos_helper(out_edges_dict,whose, out_edges) #This will return all immediate outedges
	if len(temp) == 0:
		return []
	else:
		temp1 = temp
		for k in temp:
			temp1 = list(set(temp1)| set(get_all_out_edges_recursively_except_appos(out_edges_dict, k, out_edges,)))
		return temp1

#TODO: Take care of copular cases.
def extract_relevant_predicate_relations(out_edges_dict,pred,out_edges): #TODO: PRedicates can have outgoing nmod modifiers
#In most of the cases, the predicates are aux + verb or aux + adj.
	if "aux" in out_edges_dict[pred]:
		return out_edges_dict[pred]["aux"]
	else:
		return []

def process_nmods(out_edges_dict, word,out_edges): 
	temp = []
	for edge in out_edges_dict[word]:				
		if "nmod" in edge:							
			for each_nmod_word in out_edges_dict[word][edge]:
				#recursively get all outgoing edges of each nmod_word
				temp.append((get_all_out_edges_recursively_except_appos(out_edges_dict,each_nmod_word, out_edges)).append(each_nmod_word))
	return temp

def process_acl(out_edges_dict, word,out_edges): 
	temp = []
	for edge in out_edges_dict[word]:				
		if "acl" in edge:							
			for each_acl_word in out_edges_dict[word][edge]:
				#recursively get all outgoing edges of each nmod_word
				k = get_all_out_edges_recursively_except_appos(out_edges_dict,each_acl_word, out_edges)
				k.append(each_acl_word)
				temp.append(k)
	return temp
"""
Notes
#nominal modifiers are nouns. So they could themselves be modified by adjectives.But we wont separate them atm, we would send adj + nmod
#nmods can themselves be modified by another nmod
"""

def process_dobj(out_edges_dict, word, out_edges,second_arg): #TODO: Similar processing for subj
	second_arg["pred_dobj"] = []
	second_arg["pred_dobj"].append(word)

	if "amod" in out_edges_dict[word]:
		for j in out_edges_dict[word]["amod"]:
			second_arg["pred_dobj"].append([word,j]) 
			for out_edge in out_edges_dict[j]:
				if "conj" in out_edge:
					for word1 in out_edges_dict[j][out_edge]:
						second_arg["pred_dobj"].append([word1,word]) 

	nmods = process_nmods(out_edges_dict, word, out_edges)
	for i in nmods:
		second_arg["pred_dobj"].append(i.append(word))


	acl = process_acl(out_edges_dict, word, out_edges)
	for i in acl:
		i.append(word)
		second_arg["pred_dobj"].append(i)

	print second_arg


def extract_second_argument(out_edges_dict,pred,out_edges):
	second_arg = {}
	second_arg["pred_advmod"] = []
	second_arg["pred_iobj"] = []
	second_arg["pred_advcl"] = []
	second_arg["pred_xcomp"] = []
	second_arg["pred_ccomp"] = []
	second_arg["pred_nmod"] = []
	

	if "dobj" in out_edges_dict[pred]: 
		for j in out_edges_dict[pred]["dobj"]:
			process_dobj(out_edges_dict, j, out_edges,second_arg)

	#if "advmod" in out_edges_dict[pred]: 
	#	for j in out_edges_dict[pred]["advmod"]: #multiple adverbs He is eating slowly,happily.
	#		temp = j
	#		temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
	#		second_arg["pred_advmod"].append(temp)
#
	#if "iobj" in out_edges_dict[pred]: 
	#	temp = out_edges_dict[pred][0] #Assuming only one iobj
	#	modifiers = extract_noun_modifiers(out_edges_dict,temp,out_edges)
	#	second_arg["pred_iobj"] = list(set([temp]) | 
	#			set(modifiers["nmods"]) | set(modifiers["non-nmods"]))
#
	#if "advcl" in out_edges_dict[pred]: 
	#	for j in out_edges_dict[pred]["advcl"]: #multiple adverbs He is eating slowly,happily.
	#		temp = j
	#		temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
	#		second_arg["pred_advcl"].append(temp)
#
	#if "xcomp" in out_edges_dict[pred]: 
	#	for j in out_edges_dict[pred]["xcomp"]: #multiple adverbs He is eating slowly,happily.
	#		temp = j
	#		temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
	#		second_arg["pred_xcomp"].append(temp)
#
	#if "ccomp" in out_edges_dict[pred]: 
	#	for j in out_edges_dict[pred]["ccomp"]: #multiple adverbs He is eating slowly,happily.
	#		temp = j
	#		temp = list(set([temp]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,temp,out_edges)))
	#		second_arg["pred_ccomp"].append(temp)

	#Since there can be n types of nmod depdency, we need to have this loop :(
	#for rel in out_edges_dict[pred]:
	#	if "nmod" in rel:
	#		for each_nmod in out_edges_dict[pred][rel]:
	#			second_arg["pred_nmod"] = list(set(pred_nmod_and_its_dependents) | 
	#													set (process_nmods(out_edges_dict,each_nmod)))

	return second_arg

#TODO Take care of copular verb case,  He is a bright student. Here the root is student. NOUN as the governor of nsubj
def find_nsubj(out_edges, in_edges, edges,sentence):
	out_edges_dict = convert_out_edges(out_edges)
	relations = find_nsubj_rel(edges,out_edges_dict)
	w_words = ["which", "whom","where","when"]
	for rel in relations:
		sub = rel[1]
		index = sub.rfind('-')
		lead = sub[0:index]
		if lead in w_words:
			continue

		pred = rel[0]
		#print "FIRST ARGUMENT", sub, extract_noun_modifiers(out_edges_dict, sub,out_edges)
		#print "PREDICATE", pred, extract_relevant_predicate_relations(out_edges_dict,pred,out_edges)
		print "SECOND ARGUMENT" #There can be multiple second arguments
		extract_second_argument(out_edges_dict,pred,out_edges)
		
#ccomp subject may be w word He is eating which is good
#interesting xcomp He is eating to go there to meet him. meet -> go xcomp there -> go advmod
#He was there when I left. 
#recursive ccomps

#TODO
#Check for determiners


"""
if a verb has outgoing nmod then its non core dependency. There can be one relation with only verb and one with verb and nmod
if a noun has outgoing nmod then its a core dependency.
"""