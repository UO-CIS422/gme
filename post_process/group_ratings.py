"""
group_ratings:  Gather mutual ratings of students by group. 

Usage: 
   python3 group_ratings.py gme.csv 

   We assume names have already been normalized by clean_names.py
   (possibly in multiple rounds)

   We assume that if x rates y OR y rates x, then x and y are 
   in the same group

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
    parser = argparse.ArgumentParser(description="Combine groups in GME file")
    parser.add_argument('gme', type=str,
                        help="GME file in csv format")
    args = parser.parse_args()
    return args


# Structure of GME file -- relevant columns are the first two
#
#
# rater_name_col = 1
# rated_name_col = 2

rater_label = "member"
rated_label = "teammate"
# Numbered attributes in spreadsheet
attributes = [ "dependable", "constructive", "engaged",
                   "productive", "asset" ]
# Each comment entry is one of those attributes + _comments
#
# Structure of a group record is
# [ names, rating, rating, rating, ... ]
#
# Note now we are using a DictReader, so each rating
# is an ordered dict.  This makes it easier to access
# rating[name, attribute].
#

def group_ratings(gme_file_path):
    """
    Returns list of group ratings, where each group is 
    a list of individual ratings with at least one cross-rating
    """
    groups = [ ] 
    person_group = { }
    with open(gme_file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile) 
        for row in reader:
            rater = row[rater_label]
            rated = row[rated_label]
            # print("Processing {}->{}".format(rater,rated))
            if rater in person_group:
                group = person_group[rater]
            elif rated in person_group:
                group = person_group[rated]
            else:
                group = [ [ ],  ]
                groups.append(group)
            person_group[rater] = group
            person_group[rated] = group
            group.append(row)
            names = group[0]
            if rater not in names:
                names.append(rater)
            if rated not in names:
                names.append(rated)
            # print("Group now is {}".format(group[0]))
    return groups

def list_groups(groups):
    for group in groups:
        print("Group: ", end="")
        print(group[0])
        #for row in group:            
    return

def rating_of(member, teammate, attribute, group):
    """
    The group record is [[members], rating, rating, ... ]
    where each rating is a dict in which 'member' is the 
    rater and 'teammate' is the rated person.  Some members 
    may not have submitted ratings, so for those we return 
    '-'
    """
    for gme in group[1:]:
        if gme["member"] == member and gme["teammate"] == teammate:
            return gme[attribute]
    return "-"

def summarize_group(group):
    """Print a matrix summary of group"""
    members = group[0]
    # Header row
    print(" ,", end="")  # Start in second column
    for member in members:
        print(member, end=",")
    print()
    # One row per member
    for member in members:
        print(member, end=",")
        for mate in members:
            collected = ""
            sep=""
            for attribute in attributes:
                collected = (collected + sep +
                   rating_of(mate,member,attribute,group))
                sep = "/"
            print(collected, end=",")
        print()
    
        
    
def main():
    args = get_args()
    groups = group_ratings(args.gme)
    # list_groups(groups)

    for group in groups:
        summarize_group(group)
        print()  # Separate

if __name__ == "__main__":
    main()


