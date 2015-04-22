import re,sys
final_res = ""
words={}
for word in file("words.txt"):
	words[word[:-1].lower()]=True
#print sys.getsizeof(words)
n=int(raw_input())
def segment(word, res):
	global final_res
	for i in range(1,len(word)+1):
		substr = word[0:i]
		try:
			if words[substr]:
				if i == len(word): 
					res+=substr
					final_res = res
					res=""
				segment(word[i:], res+substr+" ")
		except:
			s=0
while(n>0):
	w=raw_input()
	if '#' in w:
		w=w.split('#')[1]
	else:
		w=w.split('.')[0]
	w=re.split("([0-9]+[.]*[0-9]*|-)",w)
	#print w
	sent=""
	for word in w:
		if word != '-' and not word.isdigit() and len(word)>0 and not re.match("[0-9]+[.][0-9]+",word):
			segment(word,"")
			sent+=final_res
			final_res=""
		else:
			sent+=" "+word+" "
	n-=1
	print sent.strip()







