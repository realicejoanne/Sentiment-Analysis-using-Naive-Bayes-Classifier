import re # regular expression library
import csv # csv library

fh=open("dataset.csv","r") # buka file dataset yg diinginkan

# Delimiter pada kalimat csv adalah + yang akan digunakan agar titik dan koma tidak dianggap akhir kalimat
reader = csv.reader(fh, delimiter='+')

# Kumpulan dari data yang sudah memiliki label (+ dan -)
dataset={}

# Kumpulan dari data yang menyimpan label  1
# { label l : data yang memiliki label l }
no_of_items={}

# Kumpulan dari jumlah kata yang memiliki label
# { kata : { label l : jumlah kata dengan label 1 } }
feature_set={}

# Untuk setiap kalimat pada dataset
for row in reader:
	# Inisialisasi label yang belum ada di kamus
	no_of_items.setdefault(row[1],0)
	# Menambahkan perhitungan untuk setiap kata yang berlabel 1
	no_of_items[row[1]]+=1
	# Inisialisasi kamus untuk label yang belom ada
	dataset.setdefault(row[1],{})
	# Split kalimat ke nonkarakter dan tidak dipisah apabila ada tanda kutip dan *, dan ?
	split_data=re.split('[^a-zA-Z\']',row[0])
	
	# Split kata untuk setiap kalimat
	for i in split_data:
		# Menghilangkan stop words dengan mengabaikan kata yang kurang dari 3 huruf
		if len(i) > 2:
			# Inisialisasi perhitungan kata di dataset
			dataset[row[1]].setdefault(i.lower(),0)
			# Increment perhitungan kata dengan label row[1]
			dataset[row[1]][i.lower()]+=1
			# Inisialisasi kamus untuk kata yang baru ditemukan ke feature set
			feature_set.setdefault(i.lower(),{})
			# Jika label ditemukan untuk kata pertama kali, insialisasi nilai yang serupa untuk kata sebagai kunci
			feature_set[i.lower()].setdefault(row[1],0)
			# Increment  untuk kata di label tersebut
			feature_set[i.lower()][row[1]]+=1