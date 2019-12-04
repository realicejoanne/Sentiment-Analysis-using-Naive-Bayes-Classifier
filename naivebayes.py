import re # regular expression library
from sensitive_data import dataset,feature_set,no_of_items # sensitive_data.py

# Hitung probabilitas kata untuk suatu kategori
def calc_prob(word,category):
	if word not in feature_set or word not in dataset[category]:
		return 0

	return float(dataset[category][word])/no_of_items[category]

# Hitung probabilitas bobot kata untuk suatu kategori
def weighted_prob(word,category):
	# Probabilitas kata
	basic_prob=calc_prob(word,category)

	# Jumlah kemunculan di semua kategori
	if word in feature_set:
		tot=sum(feature_set[word].values())
	else:
		tot=0

	# Rumus probabilitas bobot kata:
	# (bobot * asumsi_probabilitas + jumlah_kemunculan * probabilitas dasar) / (jumlah_kemunculan + bobot)
	# Bobot secara default diambil sebagai 1.0 dan asumsi probabilitasnya adalah 0.5
	weight_prob=((1.0*0.5)+(tot*basic_prob))/(1.0+tot)
	return weight_prob #probabilitas bobot kata

# Untuk mendapatkan probabilitas data uji untuk kategori yang diberikan
def test_prob(test,category):
	# Split kalimat test data ke nonkarakter dan tidak dipisah apabila ada tanda kutip dan *, dan ?
	split_data=re.split('[^a-zA-Z][\'][ ]',test)
	
	data=[]
	for i in split_data:
		# Split spasi
		if ' ' in i:
			i=i.split(' ')
			
			for j in i:
				# Tambah data baru ke list data uji
				if j not in data:
					data.append(j.lower())
		
		# Edge case kalau ditemukan ada kata lebih dari 3 huruf dan ternyata belum ada
		elif len(i) > 2 and i not in data:
			data.append(i.lower())

	# Mencari bobot yang real bukan coba-coba lagi
	p=1
	for i in data:
		p*=weighted_prob(i,category)
	return p

# Naive Bayes
def naive_bayes(test):
	'''
		Rumus Naive Bayes: p(A|B) = p(B|A) * p(A) / p(B)

		Anggap A - Kategori
			   B - Test data
			   p(A|B) - Kategori dari test data

		Abaikan p(B) dalam penyebut karena akan jadi tetap sama untuk setiap kategori
	'''
	results={}
	
	for i in dataset.keys():
		cat_prob=float(no_of_items[i])/sum(no_of_items.values())
		test_prob1=test_prob(test,i)
		results[i]=test_prob1*cat_prob
		
	return results # hasil (1 atau -1) berdasarkan Naive Bayes

# Output program
print ('Masukkan kalimat:')
text=input()
result=naive_bayes(text)

if result['1'] > result['-1']:
	print ('Review Positif')
else:
	print ('Review Negatif')