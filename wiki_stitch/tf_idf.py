import re, math, string
stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
punctuations = set(string.punctuation)
def remove_stop_words(words):
	global stopwords
	words = [word for word in words if not word in stopwords]
	return words

def split_words(doc):
	words = doc.lower().translate(None, string.punctuation).split()	
	return remove_stop_words(words)

def word_frequency(words):
	word_dict={}
	for i in words:
		try:
			word_dict[i]+=1
		except:
			word_dict[i]=1
	return word_dict

def get_doc_tf(doc):
	words = split_words(doc)
	ndoc_tf = word_frequency(words) 
	for i in ndoc_tf:
		ndoc_tf[i]=float(ndoc_tf[i])/len(words)
	return ndoc_tf

def create_query_doc_tf_idf(words, doc_tf, doc_idf):
	query_doc_tf_idf_temp={}
	for doc in doc_tf:
		query_doc_tf_idf_temp[doc]={}
		for word in set(words):
			try: 
				query_doc_tf_idf_temp[doc][word]= float(doc_tf[doc][word])*doc_idf[word]
			except:
				query_doc_tf_idf_temp[doc][word] = 0.0
	return query_doc_tf_idf_temp

def create_query_tf_idf(words, doc_idf):
	query_tf_idf_temp={}
	word_count = word_frequency(words)
	for word in set(words):
		try:
			query_tf_idf_temp[word] = float(word_count[word])/len(words)*doc_idf[word]
		except:
			query_tf_idf_temp[word] = 0.0
	return query_tf_idf_temp

def create_doc_idf(doc_df):
	for i in doc_df:
		doc_idf[i]=1+math.log(len(docs)/doc_df[i],2)
	return doc_idf

def cosine_sim(doc, query):
	cosSim = 0.0
	for term in query:
		cosSim += doc[term]*query[term]
	try:
		cosSim /= normalize(doc)
	except:
		pass
	return cosSim

def normalize(sample):
	sum = 0.0
	for term in sample:
		sum += sample[term]**2
	return math.sqrt(sum)




delimiters = [' ', ',', '.', '?', '!', ':', "'", '()', '[]']
f=open("test_data.txt","r").readlines()

t=int(f[0].strip('\n'))
docs = []
query = []
query_doc_map = {} 		# {q1:{d1:score, d2:score}, q2{...}} Here q1 is 0 and represented by query[], d1 is repr by docs[]
query_doc_tf_idf = {} 	# {0:{d1: {t1:count, t2:count}, d2:{t1:count, t2:count}}, 1:{...}, ...}
doc_tf = {} 			# {0:{t1:count, t2:count}, 1:{...}, ...}
doc_idf = {} 			# {t1:val, t2:value, ...}
query_tf_idf = {} 		# {0: {t1:val, t2:val}, 1:{t1:val, t2:val} ...}
doc_df = {} 			# {t1:val, t2:value, ...}
for i in range(t):
	docs.append(f[i+1].strip('\n'))
	doc_tf[i] = get_doc_tf(docs[i])
	for term in doc_tf[i]:
		if term in doc_df:
			doc_df[term]+=1.0
		else:
			doc_df[term]=1.0

doc_idf = create_doc_idf(doc_df)

for i in range(t):
	query.append(f[t+i+2].strip('\n'))
	words = split_words(query[i])
	query_doc_tf_idf[i] = create_query_doc_tf_idf(words, doc_tf, doc_idf)
	query_tf_idf[i] = create_query_tf_idf(words, doc_idf)

for query in query_doc_tf_idf:
	query_doc_map[query] = {}
	query_norm = normalize(query_tf_idf[query])
	for doc in query_doc_tf_idf[query]:
		try:
			query_doc_map[query][doc] = cosine_sim(query_doc_tf_idf[query][doc], query_tf_idf[query])/query_norm
		except:
			query_doc_map[query][doc] = 0.0

for i in query_doc_map:
	for j in query_doc_map[i]:
		if query_doc_map[i][j]==max(query_doc_map[i].values()):
			print j+1
