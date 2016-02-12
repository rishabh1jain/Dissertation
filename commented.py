"""
case = ""
	nmod_dependents = [nmod]	
	for key in out_edges_dict[nmod]:
		if "case" in key:
			case = out_edges_dict[nmod][key]
			print "CASE", case
		elif "nmod" in key:
			nmod_dependents = list(set(nmod_dependents)|set(process_nmods(out_edges_dict,out_edges_dict[nmod][key][0])))
		else:#NON CASE DEPENDENTS OF NMOD LIKE DETERMINERS etc
			nmod_dependents = list(set(nmod_dependents) |set(out_edges_dict[nmod][key]))
	nmod_dependents = list(set(nmod_dependents) |set(case))
	return nmod_dependents

def extract_noun_modifiers(out_edges_dict, noun,out_edges): #For getting the dedendent of argument1 and argument2
	modifiers = {}
	modifiers["non-nmods"] = []
	modifiers["nmods"] = []
	if noun not in out_edges_dict: #The 
		return modifiers
	for rel in out_edges_dict[noun]:
		if ("appos" not in rel and "nmod" not in rel) or "poss" in rel:
			for j in out_edges_dict[noun][rel]:
				modifiers["non-nmods"] = list(set([j]) | set(modifiers["non-nmods"]) | set(get_all_out_edges_recursively_except_appos(out_edges_dict,j, out_edges)))
		elif "nmod" in rel:
			for each_nmod in out_edges_dict[noun][rel]:
				print each_nmod
				modifiers["nmods"] = list(set(modifiers["nmods"]) | set (process_nmods(out_edges_dict,each_nmod)))
	return modifiers

"""