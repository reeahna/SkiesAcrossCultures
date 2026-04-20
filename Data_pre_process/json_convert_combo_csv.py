"""
ENGR-583 Spring '26
Team C
Skies Across Cultures
Version: 2.1
Date: 3/16/26

This script takes all 40 json files and converts them into a large CSV for further analysis.
Source: https://github.com/doinab/constellation-lines/

Note: Current path variable expects this script to be in the same folder as the JSON files directory.

future additions:
fix bug, some JSON files under the CONSTELLATIONS key uses a sub-key called group not lines, some data is getting missed
remove data not needed for data analysis or visualizations?
"""
#----IMPORTS----#
import glob  #glob is used to search file system
import json  #used for opening json files
import csv  #used for writing out to csv
import time  #used for calculating run time in final console output

#----GLOBAL VAR----#
output_file = "output.csv"  #output csv file name
pre_time = time.time()  #prime the timer that is used to calculate delta time
#assumes python script is run from same directory as json folder
path_patt = r"JSON\*.json"  #path to directory of json files
count = 0  # counter var, constellation count


#----SET UP COLUMN NAMES AS LISTS----#
#header being used for culture(many constellations) data
cul_header = ["id","name","region","subregion","period","place","source","licence","phylogeny","description", "culture","astronomy","data summary","certainty","constellations", "common_names"]
#header being used for individual constellations data
cons_header = ["id", "names", "lines", "certainty", "description", "variant_of", "semantics", "IAU"]
#combination of other two headers with some renamed column names for clarity,will be used in csv
renamed_header = ["con_id","con_name","con_lines","con_certainty","con_visual","con_variant","con_category","IAU_abv","cul_id","cul_name","region","subregion","period","place","source","licence","phylogeny","description","culture","astronomy","data_summary","certainty","cons_total_by_cul","common_names"]

#----CSV HEADER WRITE----#
#open csv and write out header as first row
head_out = open(output_file,  "w", encoding="utf-8", newline='', errors="replace")  #opens in write mode,file is overwritten if it exists already, UTF-8 must be used
writer = csv.writer(head_out)  #create the csv writer
renamed_header.insert(0,"count")  #insert a column at the start to assign a count to each row
writer.writerow(renamed_header)  #write a row to the csv file, combo of culture and constellation headers
head_out.close()  #close connection, file will be opened again later in a diff mode

#----JSON FILE NAMES----#
path_dir = []#list to store jason file names
for filepath in glob.glob(path_patt, recursive=True):  #access files in directory - appends name to list
    path_dir.append(filepath)  #add directory to JSON files to the file path list

#open CSV file for new row to be appended, UTF-8 encoding must be used
#pass newline to stop blank spaces being auto added
data_out = open(output_file, "a", encoding="utf-8", newline='')  #append mode to add to file not overwrite
writer = csv.writer(data_out)  #create the csv writer


def culture_process(json_dict_cul):
    """
    This function processes high level JSON data realted to cultures. It
    creates one of the two lists needed for row write to the csv.

    It takes in a the JSON data as a dictionary. Returns a list of data. 
    """
    keys = json_dict_cul.keys()  #keys is a view object of JSON file keys
    key_l = list(keys)  #key list is a list object of the key names
    new_culture_row = []  #row to be appended to csv as a new data for each culture (each JSON file)
    for j in cul_header:  #for each key(column) in the header
        if j == "constellations":#if the key(column) is constellations then count # of constellations for that culture(JSON)
             new_culture_row.append(len(json_dict_cul[j]))
        elif j in key_l:  #if that key is represented in current open JSON file
             new_culture_row.append(json_dict_cul[j])#append that keys value to the new row to get output later
        else:  #if the current key is not in current JSON file
            new_culture_row.append("none") #then add none as a place-holder to new row
    return new_culture_row  #return final row data as a list back to main

def constellation_process(json_dict_cons):
    """
    This function processes low level JSON data related to constellations. It
    creates one of the two lists needed for row write to the csv.

    It takes in the JSON data as a dictionary. Returns a list of data.
    """
    new_cons_row = []  #row to be appended to csv as a new data
    con_key_l = list(json_dict_cons.keys())  #list of keys from the current constellation
    #for each key in the control header for constellations
    for k in cons_header:
        #if current constellation key is in control header
        if k in con_key_l:
            #append value to new built list (header)
            new_cons_row.append(json_dict_cons[k])
        #if key is not in control list
        else:
            #append placeholder value to new built list (header)
            new_cons_row.append("none")
    return new_cons_row  #return final row data as a list back to main

def main():
    """
    This function takes no inputs. It opens all JSON files and then calls supportign functions
    to process the data int oa final output which is written out to a CSV file. 
    """
    global count  #sets permission for main to make changes to count varibale
    
    #----JSON FILE PROCESSING----#
    #process each JSON file, i is a file name
    for i in path_dir:  #Open and load JSON data,
        with (open(i, "r", encoding="utf-8", newline='', errors="replace") as json_file):
            data = json.load(json_file)  #data is a dictionary of JSON pairs
            
            cul_list = culture_process(data)  #call function to process culture data inside JSON file
            
            # ----PROCESS JSON CONSTELLATIONS DATA----#
            #this block creates one of the two lists needed for final CSV write
            #look at each constellation in the constellations nested list from the JSON file
            for con in data["constellations"]:
                count+=1  #count assigned to each constellation so they are numbered
                                       
                cons_list = constellation_process(con)  #call function to process constellation data from JSON
                                       
                #----BUILD FINAL ROW TO BE WRITTEN TO CSV----#
                com_row = cons_list + cul_list  #complete row is a concatenation of both culture and constellation data
                com_row.insert(0,count)  #insert the current count at start of row
                writer.writerow(com_row)  #write a row to the csv file

#if the main function exists run lines 130-138
if __name__=="__main__":
    main() #call main
    
    #----WRAP UP----#
    #have exited JSON file loop
    data_out.close()  #once all JSON files have had their data written to CSV,close the connection
    #check elapsed time since last time stamp and set delta time
    cur_time = time.time()  #stop the timer, get current time
    delta = cur_time - pre_time  #time elapsed from one calc to the next
    print(f"Operation complete in {delta:.2f} seconds.")  #success message
