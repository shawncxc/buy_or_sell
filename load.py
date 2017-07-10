from sklearn.externals import joblib
import spacy
import seekingalpha.processor as processor
import seekingalpha.word_embedding as embedding

# load model
loaded_model = joblib.load('linear_model.sav')

# tokenize and clean
def load_news(title, content):
	words = []
	nlp = spacy.load('en')
	
	title_nlp = nlp(title)
	for token in title_nlp:
		lemma = processor.remove_linebreaker_tabs(token.lemma_)
		if processor.is_useless(token): continue
		words.append(lemma)

	content_nlp = nlp(content)
	for token in content_nlp:
		lemma = processor.remove_linebreaker_tabs(token.lemma_)
		if processor.is_useless(token): continue
		words.append(lemma)

	return words

# convert to vectors
def vectorize(words):
	word_vecs = []
	nlp = spacy.load('en')

	for word in words:
		word_vec = nlp.vocab[word].vector
		word_vecs.append(word_vec)
	
	return embedding.avg_vec(word_vecs)

def get_result(title, content):
	if type(title).__name__ == 'str': title = unicode(title)
	if type(content).__name__ == 'str': content = unicode(content)
	words = load_news(title, content)
	X_test = [vectorize(words)]
	result = loaded_model.predict(X_test)
	print(result)
	return result

# title = 'AMD: The ship is sinking, Bloomerburg say SELL'
# content = 'The product of AMD is not as expected, and we say we should sell all of it'
# get_result(title, content)