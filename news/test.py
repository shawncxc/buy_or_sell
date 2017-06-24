from gensim.models import Phrases

# def phrasize(words):
# 	print words
# 	bigram = Phrases([words], min_count=1, threshold=2)
# 	print list(bigram[[u'the', u'mayor', u'of', u'new', u'york', u'was', u'there']])
# 	return list(bigram[[u'the', u'mayor', u'of', u'new', u'york', u'was', u'there']])

# phrasize(["the mayor of new york was there", "machine learning can be useful sometimes","new york mayor was present"])

documents = ["the mayor of new york was there", "machine learning can be useful sometimes", "new york mayor was present", "machine learning will kill us all"]
sentence_stream = [doc.split(" ") for doc in documents]
print sentence_stream
bigram = Phrases(sentence_stream, min_count=1, threshold=2)
sent = [u'the', u'mayor', u'of', u'new', u'york', u'was', u'there']
print(bigram[sent])
sent = [u'machine', u'learning', u'can', u'be', u'useful', u'sometimes']
print(bigram[sent])