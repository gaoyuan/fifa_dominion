# -*- coding:utf-8 -*-

# fifa country&league ratings
import csv
import itertools

def ratings_to_star(rating):
    if rating > 82:
        return 5
    elif rating > 78:
        return 4.5
    elif rating > 74:
        return 4
    elif rating > 70:
        return 3.5
    elif rating > 68:
        return 3
    elif rating > 66:
        return 2.5
    elif rating > 64:
        return 2
    elif rating > 62:
        return 1.5
    elif rating > 59:
        return 1
    else:
        return 0.5

rating_dict = {}
with open('sofifa_country.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            country = row[0]
            year = int(row[1].split('-')[0]) + 1  # fifa18 uses year 2017's data
            rating = float(row[2])
            if (country, year) not in rating_dict:
                rating_dict[(country, year)] = rating

YEAR = 2019

rating_list = [(k, v) for k, v in rating_dict.items() if k[1] == YEAR]
star_list = [(k[0], float(ratings_to_star(v))) for k,v in rating_list]
star_dict = {}
for country, star in star_list:
    if star not in star_dict:
        star_dict[star] = [country]
    else:
        star_dict[star].append(country)
print(star_dict)

            
