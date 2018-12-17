#------------------------------------------------------------------------------
#The four parts of this program are explained more thoroughly in the narrative.
#------------------------------------------------------------------------------

import gzip
import csv
import sys

csv.field_size_limit(sys.maxsize)

temp_row = []

#1) Extracting information from ‘title.ratings.tsv.gz’
ratings_rows = []
with gzip.open('title.ratings.tsv.gz', 'rt', encoding="utf8") as r:
    reader = csv.DictReader(r, delimiter='\t')
    for row in reader:
        if int(row["numVotes"]) > 10000:
            temp_row.append(row["tconst"])
            temp_row.append(row["averageRating"])
            temp_row.append(row["numVotes"])
            ratings_rows.append(temp_row)
            temp_row = []

#2) Extracting information from ‘title.akas.tsv.gz’
akas_rows = []
with gzip.open('title.akas.tsv.gz', 'rt', encoding="utf8") as t:
    reader = csv.DictReader(t, delimiter='\t')
    for row in reader:
        if row["isOriginalTitle"] == '1':
            temp_row.append(row["titleId"])
            temp_row.append(row["title"])
            akas_rows.append(temp_row)
            temp_row = []

#3) Creating ‘best_10_releases_IMDB.txt’
found_accumulator = 0
fileopen = open("best_10_releases_IMDB.txt", 'w')
fileopen.write("The 10 highest rated releases on IMDB with at least 10,000 ratings.\n\n")
for r_row in sorted(ratings_rows, key=lambda x: x[1], reverse=True):
    for a_row in akas_rows:
        if r_row[0] == a_row[0]:
                found_accumulator+=1
                file_string = (str(found_accumulator)+": "+a_row[1]+", average rating: "+r_row[1]+" with "+r_row[2]+" ratings.\n")
                fileopen.write(file_string)
    if found_accumulator == 10:
        break
fileopen.close()

#4) Creating ‘worst_10_releases_IMDB.txt’
found_accumulator = 0
fileopen = open("worst_10_releases_IMDB.txt", 'w')
fileopen.write("The top 10 lowest rated releases on IMDB with at least 10,000 ratings.\n\n")
for r_row in sorted(ratings_rows, key=lambda x: x[1]):
    for a_row in akas_rows:
        if r_row[0] == a_row[0]:
                found_accumulator+=1
                file_string = (str(found_accumulator)+": "+a_row[1]+", average rating: "+r_row[1]+" with "+r_row[2]+" ratings.\n")
                fileopen.write(file_string)
    if found_accumulator == 10:
        break
fileopen.close()
