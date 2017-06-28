import spacy
import numpy

nlp = spacy.load('en')
word = u'success'
print nlp.vocab[word].vector

# example = nlp(u'This apple is so terribly good! But not this banana.')
# for token in example:
# 	print token, token.is_stop # stop words
# 	print token, token.sentiment # sentiment
# 	print token, token.vector.shape # word vector
	# print nlp.vocab[token].vector
