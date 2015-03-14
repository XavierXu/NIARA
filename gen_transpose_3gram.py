#!/usr/bin/env python

#extract transposed feature vectors (rows are features, columns are domains)
from pyngram import calc_ngram
import csv,sys,resource
import codecs
#hand to god I have no idea why I added this...
def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#the "n" in n-grams
grams = 3

#------Getting possible tri-grams-----#

all_grams = []
all_doms = []

print "Gathering possible grams fordictionary-based DGA URLs"

#path to dga url file (tab delimited, column 1 is domain, column 2 is class)
with open("dga_based_on_dictionary_1.txt", "rU") as infile1:

    for line in infile1:
        domain = line.strip()
        tri_gram_results_in_list = []
        tri_gram_results_in_list = calc_ngram(domain, 3) #[('ceb', 1), ('ace', 1), ('ebo', 1), ('ook', 1), ('boo', 1), ('fac', 1)] as example
        for each in tri_gram_results_in_list:
            all_grams.append(each[0])

        all_doms.append(domain)

with codecs.open("Alexa_top_1M_country", "rU", encoding='utf-8') as infile2:
    line_count = 0
    for line in infile2:
        line_count+=1
        if line_count >= 238035:
            print 'Alexa Sampling End at line %s'%line_count
            break
        domain = line.split(" ")[0].strip()
        label = "Non-DGA"

        print 'Working on line %s'%domain
        tri_gram_results_in_list = []
        tri_gram_results_in_list = calc_ngram(domain, 3) #[('ceb', 1), ('ace', 1), ('ebo', 1), ('ook', 1), ('boo', 1), ('fac', 1)] as example
        for each in tri_gram_results_in_list:
            all_grams.append(each[0])

        all_doms.append(domain)



all_grams = list(set(all_grams))

header = []
header.append("url")
header.append("class")
header.extend(all_grams)



print len(all_grams)

#-----Make feature vectors-----#
print "Making feature vectors for DGA"

gram_dict={}
class_dict={}
classes = []
domains = []

#path to dga url file (tab delimited, column 1 is domain, column 2 is class)
#row = []
with open("dga_based_on_dictionary_1.txt", "rU") as infile1:

#    writer = csv.writer(outfile)
    #writer.writerow(header)
#    head = [next(infile1) for x in xrange(4)]
    for line in infile1:
        domain = line.strip()
#        print line
        print domain
        label = 'dic_bas_DGA'

        these_grams = []
        tri_gram_results_in_list = []
        #for g in range(1,grams+1):
        #    these_grams.extend([domain[i:i+g] for i in range(len(domain)-g+1)])
        tri_gram_results_in_list = calc_ngram(domain, 3) #[('ceb', 1), ('ace', 1), ('ebo', 1), ('ook', 1), ('boo', 1), ('fac', 1)] as example      
        for each in tri_gram_results_in_list:
            these_grams.append(each[0])

        gram_dict[domain] = these_grams
        class_dict[domain] = label
        classes.append(label)
        domains.append(domain)

with codecs.open("Alexa_top_1M_country", "rU", encoding='utf-8') as infile2:
    line_count = 0
    for line in infile2:
        line_count+=1
        if line_count >= 238035:
            print 'Alexa Sampling End at line %s'%line_count
            break
        domain = line.split(" ")[0].strip()
        label = 'Non_DGA'
        these_grams = []
        tri_gram_results_in_list = []
        #for g in range(1,grams+1):
        #    these_grams.extend([domain[i:i+g] for i in range(len(domain)-g+1)])
        tri_gram_results_in_list = calc_ngram(domain, 3) #[('ceb', 1), ('ace', 1), ('ebo', 1), ('ook', 1), ('boo', 1), ('fac', 1)] as example      
        for each in tri_gram_results_in_list:
            these_grams.append(each[0])

        gram_dict[domain] = these_grams
        class_dict[domain] = label
        classes.append(label)
        domains.append(domain)

        #row = []
        #row.extend([0] * len(all_grams))

        #for gram in these_grams:
        #    if row[all_grams.index(gram)]==0:
        #        row[all_grams.index(gram)]=1

        #row.insert(0, line.split("\t")[0])
        #row.insert(0, label)

#row.extend([line.split("\t")[0],label])

#        writer.writerow(row)

print all_doms
print class_dict

#path to transposed data
with open("DGA_data_transpose", "wb") as outfile:
    clas_str = ["class"]

    for dom in all_doms:
        clas_str.append(class_dict[dom])


    outfile.write(",".join(clas_str)+"\n")

    count = 0

    for gram in all_grams:
        count +=1
        pos = 0
        row = [gram]
        for dom in all_doms:
            if gram in gram_dict[dom]:
                row.append("1")
                pos+=1
            else:
                row.append("0")

        print "Feature " + str(count) + ": " + row[0] + ", " + str(pos) + " positives"
        
        outfile.write(",".join(row)+"\n")
