"""
He said that he was eating an Apple on Monday.
OUT_EDGES
{u'Apple-8': [(u'det', u'an-7'), (u'nmod:on', u'Monday-10')], u'Monday-10': [(u'case', u'on-9')], u'said-2': [(u'nsubj', u'He-1'), (u'ccomp', u'eating-6')], u'eating-6': [(u'mark', u'that-3'), (u'nsubj', u'he-4'), (u'aux', u'was-5'), (u'dobj', u'Apple-8')]}
enhanced_out_edges
{u'Apple-8': {u'nmod:on': [u'Monday-10'], u'det': [u'an-7']}, u'Monday-10': {u'case': [u'on-9']}, u'said-2': {u'ccomp': [u'eating-6'], u'nsubj': [u'He-1']}, u'eating-6': {u'aux': [u'was-5'], u'nsubj': [u'he-4'], u'dobj': [u'Apple-8'], u'mark': [u'that-3']}}
enhanced_all_dependencies
{u'was-5': [], u'Monday-10': [u'on-9'], u'an-7': [], u'on-9': [], u'Apple-8': [u'an-7', u'Monday-10', u'on-9'], u'that-3': [], u'He-1': [], u'said-2': [u'He-1', u'eating-6', u'that-3', u'he-4', u'was-5', u'Apple-8'], u'he-4': [], u'eating-6': [u'that-3', u'he-4', u'was-5', u'Apple-8', u'an-7', u'Monday-10']}
"""


"""
Seperating out adverbial clause as a fourth argument.
"He is faster than me in writing."
"""