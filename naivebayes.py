import re
from sensitive_data import dataset,feature_set,no_of_items

#Hitung probabilitas kategori sebuah kata
def calc_prob(word,category):
	if word not in feature_set or word not in dataset[category]:
		return 0

	return float(dataset[category][word])/no_of_items[category]

def weighted_prob(word,category):
	basic_prob=calc_prob(word,category)

	#Jumlah kemunculan di semua kategori
	if word in feature_set:
		tot=sum(feature_set[word].values())
	else:
		tot=0

	weight_prob=((1.0*0.5)+(tot*basic_prob))/(1.0+tot)
	return weight_prob

def test_prob(test,category):
	split_data=re.split('[^a-zA-Z][\'][ ]',test)
	
	data=[]
	for i in split_data:
		if ' ' in i:
			i=i.split(' ')
			for j in i:
				if j not in data:
					data.append(j.lower())
		elif len(i) > 2 and i not in data:
			data.append(i.lower())

	p=1
	for i in data:
		p*=weighted_prob(i,category)
	return p

# Naive Bayes
def naive_bayes(test):
	'''
		p(A|B) = p(B|A) * p(A) / p(B)

		Assume A - Category
			   B - Test data
			   p(A|B) - Category given the Test data

		Here ignoring p(B) in the denominator (Since it remains same for every category)
	'''
	results={}
	for i in dataset.keys():
		cat_prob=float(no_of_items[i])/sum(no_of_items.values())

		test_prob1=test_prob(test,i)

		results[i]=test_prob1*cat_prob

	return results

print ('Enter the sentence')
text=input()
result=naive_bayes(text)

if result['1'] > result['-1']:
	print ('positive')
else:
	print ('negative')