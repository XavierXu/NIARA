import csv
import re
with open('ranked_features_all.csv') as inputfile, open("lexical_top50_test_header.csv", "wb") as outfile:
    temp_list = []
    count = 1
    for line in inputfile:
        tri_gram = re.search(r'(.*),.*', line).group(1)
        print 'NO%s:%s' %(count, tri_gram)
        temp_list.append(tri_gram)
        count = count + 1
        if count > 50:
            break
    writer = csv.writer(outfile)
#    str_list = []
#    for each in temp_list:


    print temp_list
    old_list = ["class","url","3rd_level_domain","2nd_level_domain","1st_level_domain","url_length","3rd_level_domain_length","2nd_level_domain_length","1st_domain_leg\
th","dot_count","url_entropy","2nd_level_domain_entropy","3rd_level_domain_entropy"]
    print old_list
    new_list = []
    new_list = old_list + temp_list
    print new_list
    writer.writerow(new_list)
