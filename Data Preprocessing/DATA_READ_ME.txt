Last updated: 3/17/26

All JSON files taken from https://github.com/doinab/constellation-lines/

json_convert_combo_csv.py - Python script in active development, combines all 40 json files into one convenient csv file. 

output.csv - Output file from the json_convert python script. Each row is a single constealltion from the dataset.

Columns of data in output:
count -	integer assigned to the constellation 
con_id - constellation identification inside the data set
con_name - constellation name or names in one or multiple languages 
con_lines -	stars that combine to makeup lines of the constellation 
con_certainty -	constellation characteristics for how it is identified by viewers on the ground 
con_visual - constellation visual description
con_variant - if constellation is a varient of another then that other constellation name is listed 
con_category -	category of visual that the constellation depicts i.e. fish,bird, human, etc. 
IAU_abv - constellation abbreviation assigned by IAU (International Astronomical Union)
cul_id - ID of the culture that the constealltion belongs to
cul_name -	name of the culture that the constealltion belongs to
region - region of the world that culture and constealltion belongs to
subregion -	more speicifc location for the culture and constealltion
period - time frame of research into constealltion	
place -	location of research that went into constealltion
source - source of information used in research	
licence - copy right creative commons license for the distribution of the information and images 
phylogeny -	origin point of the constealltion and culture
description - description of the culture	
culture - additional speciifc information about the culture
astronomy -	additional information about the cultures knowledge about astronomy
data_summary -	short summary about the cultures constellations 
certainty -	additional information about the veracity of the data 
cons_total_by_cul -	total number of constealltion listed for the culture in the dataset
common_names - names used to describe the stars in the constealltion

node_csv_gen.py = This script takes the output csv and breaks a few columns down into Gephi NODE data as a new CSV.

edge_csv_gen.py = This file is used to generate a new CSV of edge data for Gephi, it uses the source JSON file to do so.
