"""ExtractPaperFeatures.py: extract various features detailed according to literature review"""

__author__      = "James Marquardt and Weihan Jiang"
__copyright__   = "Copyright 2015, UW"

import tldextract, csv, sys, codecs, timeit
#from MeaningfulCharacters import meaningful_characters
from EntropyExtractor import domain_entropy
import re

print "********Gentting Top 50 3-gram Features from ranking list **************"
def return_top50():
    with open('ranked_features_all.csv') as inputfile:
        temp_list = []
        count = 1
        for line in inputfile:
            tri_gram = re.search(r'(.*),.*', line).group(1)
            print 'NO%s:%s' %(count, tri_gram)
            temp_list.append(tri_gram)
            count = count + 1
            if count > 50:
                break
#            writer = csv.writer(outfile)
#    str_list = []
#    for each in temp_list:


    print temp_list
    old_list = ["class","url","3rd_level_domain","2nd_level_domain","1st_level_domain","url_length","3rd_level_domain_length","2nd_level_domain_length","1st_domain_length","dot_count","url_entropy","2nd_level_domain_entropy","3rd_level_domain_entropy"]
    print old_list
    new_list = []
    new_list = old_list + temp_list
    print new_list
    return new_list, temp_list

top50 = []
top50 = return_top50()[1]
csv_header = []
csv_header = return_top50()[0]
#for each in return_top50()[0]:
#    new_each = '\"' + each + '\"'
#    csv_header.append(new_each)


print "Extracting DGA Features"
start_time = timeit.default_timer()
with open("dga_based_on_dictionary_1.txt", "rU") as infile1, codecs.open("Alexa_top_1M_country", "rU", encoding='utf-8') as infile2, open("lexical_top50_200kdic_200kAlexa.csv", "wb") as outfile:

    writer = csv.writer(outfile)
    #writer.writerow(["class","url","subdomain","domain","suffix","url_length","subdomain_length","domain_length","suffix_length","dot_count","domain_mcr","subdomain_mcr","url_entropy","domain_entropy","subdomain_entropy"])
    writer.writerow(csv_header)


    line_count = 0

    for line in infile1:
        line_count += 1
        domain = line.strip()#.split("\t")[0].strip()
        #        label = line.split("\t")[1].strip()
        print 'Working on line %s'%domain

        tld = tldextract.extract(domain)

        row = []

        #class and url
        row.append('Dictionary_based_DGA')
        row.append(domain)

        #TLD info
        row.append(tld.subdomain)
        row.append(tld.domain)
        row.append(tld.suffix)

        #length
        row.append(len(domain))
        row.append(len(tld.subdomain))
        row.append(len(tld.domain))
        row.append(len(tld.suffix))

        #dots
        row.append(domain.count("."))

        #meaningful characters ratio
        '''
        row.append(meaningful_characters(tld.domain))
        row.append(meaningful_characters(tld.subdomain))
        '''

        #shannon entropy
        row.append(domain_entropy(domain))
        row.append(domain_entropy(tld.domain))
        row.append(domain_entropy(tld.subdomain))

        #generating 3-gram feature
        for each in top50:
            match = re.search(r'%s'%each, domain)
            if match:
                row.append('1')
            else:
                row.append('0')

        writer.writerow(row)
        
        if line_count % 10000 == 0:
            print line_count

    line_count = 0

    tld_errors = 0
    write_errors = 0

    writer = csv.writer(outfile)
    #writer.writerow(["class","url","subdomain","domain","suffix","url_length","subdomain_length","domain_length","suffix_length","dot_count","domain_mcr","subdomain_mcr","url_entropy","domain_entropy","subdomain_entropy"])
#    writer.writerow(["class","url","subdomain","domain","suffix","url_length","subdomain_length","domain_length","suffix_length","dot_count","url_entropy","domain_entropy","subdomain_entropy"])


    for line in infile2:
        line_count+=1
        if line_count >= 238035:
            print 'Alexa Sampling End at line %s'%line_count
            break
        domain = line.split(" ")[0].strip()
        label = "Non-DGA"

        try:
            tld = tldextract.extract(domain)
        except:
            tld_errors += 1
            continue

        row = []


        #class and url
        row.append(label)
        row.append(domain)

        #TLD info
        row.append(tld.subdomain)
        row.append(tld.domain)
        row.append(tld.suffix)

        #length
        row.append(len(domain))
        row.append(len(tld.subdomain))
        row.append(len(tld.domain))
        row.append(len(tld.suffix))

        #dots
        row.append(domain.count("."))

        #meaningful characters ratio
        '''
        row.append(meaningful_characters(tld.domain))
        row.append(meaningful_characters(tld.subdomain))
        '''

        #shannon entropy
        row.append(domain_entropy(domain))
        row.append(domain_entropy(tld.domain))
        row.append(domain_entropy(tld.subdomain))

        #generating 3-gram feature
        for each in top50:
            match = re.search(r'%s'%each, domain)
            if match:
                row.append('1')
            else:
                row.append('0')



        try:
            writer.writerow(row)
        except UnicodeEncodeError, UnicodeError:
            #print row
            write_errors += 1

        if line_count % 10000 == 0:
            print line_count

    print "There were " + str(write_errors) + " write errors in Alexa"
    print "There were " + str(tld_errors) + " tld errors in Alexa"

elapsed = timeit.default_timer() - start_time
print "Features extracted in " + str(elapsed) + " seconds"
