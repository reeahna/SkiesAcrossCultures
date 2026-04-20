"""
ENGR-583 Spring '26
Team C
Skies Across Cultures
Version: 1.0
Date: 3/17/26

This script takes all 40 json files and uses them to generate a csv file of EDGE data for Gephi
Source: https://github.com/doinab/constellation-lines/

Note: Current path variable expects this script to be in the same folder as the JSON files directory.

This file is used to generate a new CSV of edge data for Gephi, it uses the source JSON file to do so.
"""
#----IMPORTS----#
import glob  #glob is used to search file system
import json  #used for opening json files
import csv  #used for writing out to csv


#----GLOBAL VAR----#
output_file = "EDGE.csv"  #output csv file name

#assumes python script is run from same directory as json folder
path_patt = r"JSON\*.json"  #path to directory of json files


#----SET UP COLUMN NAMES AS LISTS----#
#header being used for culture(many constellations) data
edge_header = ["Source","Target"]


#----CSV HEADER WRITE----#
#open csv and write out header as first row
header = open(output_file,  "w", encoding="utf-8", newline='', errors="replace")  #opens in write mode,file is overwritten if it exists already, UTF-8 must be used
writer = csv.writer(header)  #create the csv writer
writer.writerow(edge_header)  #write a row to the csv file, combo of culture and constellation headers
header.close()  #close connection, file will be opened again later in a diff mode

#----JSON FILE NAMES----#
path_dir = []#list to store jason file names
for filepath in glob.glob(path_patt, recursive=True):  #access files in directory - appends name to list
    path_dir.append(filepath)  #add directory to JSON files to the file path list

#open CSV file for new row to be appended, UTF-8 encoding must be used
#pass newline to stop blank spaces being auto added
data_out = open(output_file, "a", encoding="utf-8", newline='')  #append mode to add to file not overwrite
writer = csv.writer(data_out)  #create the csv writer

#----JSON FILE PROCESSING----#
#process each JSON file, i is a file name
for i in path_dir:  #Open and load JSON data,
    with (open(i, "r", encoding="utf-8", newline='', errors="replace") as json_file):
        data = json.load(json_file)  #data is a dictionary of JSON pairs

        # ----PROCESS JSON CONSTELLATIONS DATA----#
        #look at each line that makes up a constellation to get all star connections
        for j in data["constellations"]:  #look at data in sub-dictionary
            if "lines" in j:  #in lines is a key in dictionary
                for k in j["lines"]:  #loop through it
                    if len(k) == 1:  #ignore is its only a single star
                        pass
                    else:
                        for index in range(len(k)-1): #go through each line of stars and find the pairs
                            part_1 = k[index].replace("*","")  #clean up data
                            part_2 = k[index+1].replace("*","")  #clean up data
                            ready_line = [part_1.lstrip(), part_2.lstrip()]  #clean up data
                            writer.writerow(ready_line)  #write row to output CSV
            elif "group" in j:  #if constellation uses group key instead of lines
                k = j["group"]
                for index in range(len(k)-1):  #all group are written as a single list not a list of lists
                    part_1 = k[index].replace("*", "")  #clean up data
                    part_2 = k[index + 1].replace("*", "")  #clean up data
                    ready_line = [part_1.lstrip(), part_2.lstrip()]  #clean up data
                    writer.writerow(ready_line)  #write row to output CSV
            else:  #if no key lines or group then skip
                pass

 #----WRAP UP----#
#have exited JSON file loop
data_out.close()  #once all JSON files have had their data written to CSV,close the connection
print("done")  #print when operation is finished

