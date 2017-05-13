"""
Clean names: Iteratively normalize a 'names' column of a CSV file. 

Usage: 
   python3 clean_names.py gme.csv names.csv >names_new.csv

    We need to normalize (uniquify) student names so that
    we can match them.  We iteratively build a "names" sheet
    that maps names as entered to normalized names.

    On each pass (each execution of this script):
       If a name appears in the "as entered" column, with a
       substitution on the "substitute" column, we make the
       substitution.

       If the substitution is "delete", we delete the row.

       Otherwise, we create a new entry in names sheet
       mapping the name to itself.   The user can then alter
       that entry and run again.
"""

import argparse
import csv

def get_args():
    """
    Get command line args: 
      - The GME spreadsheet file
      - The names table file
    both of which should be text files in csv format. 
    
    Returned as a namespace. 
    """
    parser = argparse.ArgumentParser(description="Normalize names in GME file")
    parser.add_argument('gme', type=str,
                        help="GME file in csv format")
    parser.add_argument('names',  type=str,
                        help="Names file in csv format")
    args = parser.parse_args()
    return args

# CSV file structure (columns, headers)
#  
# 
key_col = 0  # Key is in column 1
val_col = 1  # Value is in column 2
key_header = "As entered"  # to make it easy to skip

def read_name_map( name_map_path) :
    """
    Returns a dict mapping as-written names to 
    normalized names
    """
    with open( name_map_path, newline="") as csvfile:
        table = { }
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) < 2:
                continue
            if row[key_col] == key_header:
                continue
            key = row[key_col]
            val = row[val_col]
            table[key] = val
    return table

# Structure of GME file -- relevant columns are the first two
#
#
rater_name_col = 1
rated_name_col = 2

def fix_name(row, index, name_map):
    """
    Make substitution to element at index, augmenting 
    name map if the element is not already in the map. 
    """
    # print("Input row: {}".format(row))
    name = row[index].strip()
    # print("Name entry is {}".format(name))
    if name.endswith(" (yourself)"):
        name = name[:-len(" (yourself)")]
    # print("Shortening to |{}|".format(name))
    if name not in name_map:
        name_map[name] = name     # Initially the identity transform
    row[index] = name_map[name]

    

def clean_names(gme_file_path, name_map):
    """
    Returns modified GME file as a list of rows; 
    also updates name_map 
    """
    gmes = [ ] 
    with open(gme_file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == "date":
                # Header row, skip
                pass
            else:
                fix_name(row, rater_name_col, name_map)
                fix_name(row, rated_name_col, name_map)
            gmes.append(row)
    return gmes

def rewrite_gmes(gme_file_path, gmes):
    """
    Write the modified gmes to a CSV file
    """
    with open(gme_file_path, 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        for row in gmes:
            writer.writerow(row)
    return


def rewrite_names_map(names_path, name_map):
    """
    Write the augmented name map
    """
    with open(names_path, 'w', newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["As entered", "Normalized"])
        names = sorted(name_map.keys())
        for name in names:
            writer.writerow([ name, name_map[name] ])
    return

def main():
    args = get_args()
    name_map = read_name_map(args.names)
    # print(name_map)
    gmes = clean_names(args.gme, name_map)
    rewrite_names_map(args.names, name_map)
    rewrite_gmes(args.gme, gmes)
    

if __name__ == "__main__":
    main()


