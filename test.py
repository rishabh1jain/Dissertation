import test_util
from nltk.tokenize.punkt import PunktSentenceTokenizer
import parser

sentence_splitter = PunktSentenceTokenizer()
def test_appo():
	body = test_util.get_body(["bsnew"],30)
	body = test_util.convert_to_list(body)
	for article in body:
		print article
		article = sentence_splitter.tokenize(article)
		for sentence in article:
			print sentence
			#parser.find_appositions(sentence)

test_appo()