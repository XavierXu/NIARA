import re
from pyngram import calc_ngram
import json
import simplejson
import logging
import time

from itertools import chain, combinations

def timeit(f):

    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print 'func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts)
        return result

    return timed


def generator_table_123gram_good(file_input):
#    try:
        counter = 0
        line_number = 0
        tmp_list = []
        with open(file_input) as f:
            while True:
                line_number = line_number + 1
                print "working on line number of Alexa1M: LINE NUMBER %s..." %line_number
                counter = counter + 1
#                if counter < 20:
                if counter < 1000000:
                    
                    line = next(f)
                    pattern = re.search(r'(.*)[\.](.*)[ |\t](.*)', line)#re.search(r'(\w+).(.*)', line)
                    string = pattern.group(1)
                    family = 'good'
                    tri_gram_results = calc_ngram(string, 3)
                    bi_gram_results = calc_ngram(string, 2)
                    uni_gram_results = calc_ngram(string, 1)
                    n_gram_results = uni_gram_results + bi_gram_results + tri_gram_results
                    yield n_gram_results, string, family, uni_gram_results, bi_gram_results, tri_gram_results


#                    if len(string)>10:
#                        tmp_list = folding_url(string)

#                        for each in tmp_list:
#                            yield ngram(each), string, family
#                    else:
#                        yield ngram(string), string, family
                else:
                    print 'counter reached the limit...exiting loop'
                    break

def generator_table_123gram_bad(file_input):
#    try:
        counter = 0
        line_number = 0
        tmp_list = []
        bi_gram_results = []
        uni_gram_results = []
        tri_gram_results = []
        n_gram_results = []
        with open(file_input) as f:
            while True:
                line_number = line_number + 1
                print "working on line number of DGA: LINE NUMBER %s..." %line_number
                counter = counter + 1
#                if counter < 20:
                if counter < 263370:
                    
                    line = next(f)
#                    print 'line is %s'%line
                    pattern = re.search(r'(.*)[\.](.*)[ |\t](\w+)', line)#re.search(r'(\w+)(.*)[ |\t](\w+)', line)
                    string = pattern.group(1)
                    family = pattern.group(3)

                    tri_gram_results = calc_ngram(string, 3)
                    bi_gram_results = calc_ngram(string, 2)
                    uni_gram_results = calc_ngram(string, 1)
                    n_gram_results = uni_gram_results + bi_gram_results + tri_gram_results
                    yield n_gram_results, string, 'DGA', uni_gram_results, bi_gram_results, tri_gram_results

#                    print 'url is %s'%string
#                    if len(string)>10:
#                        tmp_list = folding_url(string)

#                        for each in tmp_list:
#                            yield ngram(each), string, family
#else:
#    yield ngram(string), string, family
                else:
                    print 'counter reached the limit...exiting loop'
                    break


def calculate_3gram_normality():

    dic_3gram = {}
    with open('count_3l.txt') as f:
        for line in f:
            pattern = re.search(r'(\w+).(.*)', line)
            gram = pattern.group(1)
            count = pattern.group(2)
            dic_3gram[gram] = count

    return dic_3gram

def calculate_2gram_normality():
    dic_2gram = {}
    with open('count_2l.txt') as f:
        for line in f:
            pattern = re.search(r'(\w+).(.*)', line)
            gram = pattern.group(1)
            count = pattern.group(2)
            dic_2gram[gram] = count
    return dic_2gram


@timeit
def get_result():
    logging.basicConfig(filename='tmp.log', level=logging.INFO)
    logging.info('Goal: to find entries in both list...')
    logging.info('Started!')
    dic_2gram = {}
    dic_3gram = {}
    dic_2gram = calculate_2gram_normality()
    dic_3gram = calculate_3gram_normality()
    
#    dic_Pb = {}
    dic = {}
    dic_good = {}
    for each in generator_table_123gram_good('Alexa_top_1M_country'):
        print each

        dic[each[1]] = []  #each[1]is the URL string
        dic_good[each[1]] = []  #
        tmp_sum = 0
        for item in each[4]:    # each[4] is bi-gram list
            if item[0] in dic_2gram:    #item[0] is bi-gram letters
                tmp_2gram_count = dic_2gram[item[0]] 
            else:
                tmp_2gram_count = 0
            tmp_sum = float(tmp_sum) + float(tmp_2gram_count)
        if len(each[4]) == 0:
            tmp_2gram_nor_score = 'N/A'
        else:
            tmp_2gram_nor_score = float(tmp_sum)/float(len(each[4]))

        tmp_sum = 0
        for item in each[5]:    # each[5] is tri-gram list
            if item[0] in dic_3gram:    #item[0] is tri-gram letters
                tmp_3gram_count = dic_3gram[item[0]] 
            else:
                tmp_3gram_count = 0
            tmp_sum = float(tmp_sum) + float(tmp_3gram_count)
        if len(each[5]) == 0:
            tmp_3gram_nor_score = 'N/A'
        else:
            tmp_3gram_nor_score = float(tmp_sum)/float(len(each[5]))

        dic[each[1]].append(tmp_2gram_nor_score)
        dic_good[each[1]].append(tmp_2gram_nor_score)
        dic[each[1]].append(tmp_3gram_nor_score)
        dic_good[each[1]].append(tmp_3gram_nor_score)
        dic[each[1]].append(each[2])  #each[2] is good/bad
        dic_good[each[1]].append(each[2])

#creating bad
    dic_bad = {}
    for each in generator_table_123gram_bad('DGA_Data'):
        print each

        dic[each[1]] = []  #each[1]is the URL string
        dic_bad[each[1]] = []  #
        tmp_sum = 0
        for item in each[4]:    # each[4] is bi-gram list
            if item[0] in dic_2gram:    #item[0] is bi-gram letters
                tmp_2gram_count = dic_2gram[item[0]] 
            else:
                tmp_2gram_count = 0
            tmp_sum = float(tmp_sum) + float(tmp_2gram_count)
        if len(each[4]) == 0:
            tmp_2gram_nor_score = 'N/A'
        else:
            tmp_2gram_nor_score = float(tmp_sum)/float(len(each[4]))

        tmp_sum = 0
        for item in each[5]:    # each[5] is tri-gram list
            if item[0] in dic_3gram:    #item[0] is tri-gram letters
                tmp_3gram_count = dic_3gram[item[0]] 
            else:
                tmp_3gram_count = 0
            tmp_sum = float(tmp_sum) + float(tmp_3gram_count)
        if len(each[5]) == 0:
            tmp_3gram_nor_score = 'N/A'
        else:
            tmp_3gram_nor_score = float(tmp_sum)/float(len(each[5]))

        dic[each[1]].append(tmp_2gram_nor_score)
        dic_bad[each[1]].append(tmp_2gram_nor_score)
        dic[each[1]].append(tmp_3gram_nor_score)
        dic_bad[each[1]].append(tmp_3gram_nor_score)
        dic[each[1]].append(each[2])  #each[2] is good/bad
        dic_bad[each[1]].append(each[2])


#########
        
#######
    print dic
    print dic_good
    print dic_bad
    with open('23gram_normality_score.json', 'w') as outfile:
            json.dump(dic, outfile)

    with open('23gram_normality_score_Alexa.json', 'w') as outfile:
            json.dump(dic_good, outfile)

    with open('23gram_normality_score_DGA.json', 'w') as outfile:
            json.dump(dic_bad, outfile)





#        with open('DGA_Data') as f:
#            for line in f:
#                each_new = "^" + each
#                each_new = each_new.replace('.','[.]')
#                if re.search(each_new, line, re.IGNORECASE):
#                    print 'The following site has been found in both list: \"%s\" at LINE: %s ' %(each, line)
#                    logging.info('The following site has been found in both list: \"%s\" at LINE: %s  ' %(each, line))

    logging.info('Finished')

get_result()
                
