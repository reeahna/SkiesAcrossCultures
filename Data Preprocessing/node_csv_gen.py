"""
ENGR-583 Spring '26
Team C
Skies Across Cultures
Version: 1.0
Date: 3/17/26

Note: this script expects to be in the same folder as the output.csv generated from json_convert_combo_csv.py

This script takes the output csv and breaks a few columns down into Gephi NODE data

"""
#----IMPORTS----#
import csv  #used for writing out to csv

#----GLOBALS----#
node_header = ["ID","Label","Num_Con","IAU_bool"]  #list used for csv header
#count = 0  #count is used for unique ID value

#----CSV HEADER WRITE----#
#open node csv and write out header as first row
with open('NODE_3.csv', 'w', encoding="utf-8", newline='' ) as node_file:
    writer = csv.writer(node_file)  #create the csv writer
    writer.writerow(node_header)  #write a row to the csv file

#open older csv in read mode so data can be taken out
with open('output.csv', 'r', encoding="utf-8", newline='' ) as csvfile:
    csv_reader = csv.reader(csvfile)
    header = next(csv_reader)  # Read the first row as column names so its not included in processing

    constellation_count = {} #dictionary for how many times constellations a star appears in
    iau_bool = {} #dictionary for if stars appear in constellations recognized by the IAU or not

    #----clean star names----#
    for row in csv_reader:  #for each row in the csv
        data_1 = row[3]  #look at the lines data
        mod_1_1 = data_1.replace("[", "")
        mod_2_1 = mod_1_1.replace("]", "")
        mod_3_1 = mod_2_1.replace("*", "")
        mod_4_1 = mod_3_1.replace("'", "")
        mod_5_1 = mod_4_1.split(",")  # split the star names into a list

        #----proces for dictionaries----#
        #for loop determines if star is in a IAU recognized constellation or not
        for i in mod_5_1:
            clean = i.lstrip()
            if row[8] == "none":
                iau_bool[clean] = False
            else:
                iau_bool[clean] = True
            # for loop added to a dictionary to determine how many constellations a star appears in
            if clean == "none":
                break
            elif clean not in constellation_count:
                constellation_count[clean] = 1
                break
            else:
                constellation_count[clean] += 1
                break
#open node csv back up in append mode
with open('NODE_3.csv', 'a', encoding="utf-8", newline='') as node_file:
    writer = csv.writer(node_file)  # create the csv writer
    #writes out to a new CSV that can be imported into gephi
    for i in constellation_count:
        write_row = [i, i, constellation_count[i], iau_bool[i]]  # set up new row data
        writer.writerow(write_row)  # write a row to the csv file
        print(write_row)
print("done")  #print when operation is finished

    



    
    
    
