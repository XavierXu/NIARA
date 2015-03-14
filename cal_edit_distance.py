import re
from pyngram import calc_ngram
import json
import simplejson
import logging
import time
import editdistance
import random

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


def generator_random_list_good(number):
#    try:
        counter = 0
        with open('Alexa_top_1M_country') as f:
            while True:
                counter = counter + 1

                if counter < number +1:
                    
                    line = next(f)
                    line = random.choice(open('Alexa_top_1M_country').readlines())
                    pattern = re.search(r'(.*)[ |\t](.*)', line)#re.search(r'(\w+).(.*)', line)
                    url = pattern.group(1)
                    yield url


                else:
#                    print 'counter reached the limit...exiting loop'
                    break

def generator_list_good(number):
#    try:
        counter = 0
        line_number = 0
        tmp_list = []
        with open('Alexa_top_1M_country') as f:
            while True:
                line_number = line_number + 1
#                print "working on line number of Alexa1M: LINE NUMBER %s..." %line_number
                counter = counter + 1

                if counter < number +1:
                    
                    line = next(f)
                    pattern = re.search(r'(.*)[ |\t](.*)', line)#re.search(r'(\w+).(.*)', line)
                    url = pattern.group(1)
                    yield url


#                    if len(string)>10:
#                        tmp_list = folding_url(string)

#                        for each in tmp_list:
#                            yield ngram(each), string, family
#                    else:
#                        yield ngram(string), string, family
                else:
#                    print 'counter reached the limit...exiting loop'
                    break

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line


def generator_random_list_bad(number):
#    try:
        counter = 0
        with open('dga_based_on_dictionary_1.txt') as f:
            while True:
                counter = counter + 1
                if counter < number +1:
                    line = next(f)
                    line = random.choice(open('dga_based_on_dictionary_1.txt').readlines())
                    url = line.strip()
                    yield url

                else:
#                    print 'counter reached the limit...exiting loop'
                    break

def generator_list_bad(number):
#    try:
        counter = 0
        line_number = 0
        with open('dga_based_on_dictionary_1.txt') as f:
            while True:
                line_number = line_number + 1
#                print "working on line number of DGA: LINE NUMBER %s..." %line_number
                counter = counter + 1
#                if counter < 20:
                if counter < number +1:
                    
                    line = next(f)
#                    print 'line is %s'%line
                    url = line.strip()
                    yield url

#                    print 'url is %s'%string
#                    if len(string)>10:
#                        tmp_list = folding_url(string)

#                        for each in tmp_list:
#                            yield ngram(each), string, family
#else:
#    yield ngram(string), string, family
                else:
#                    print 'counter reached the limit...exiting loop'
                    break

def calculate_ave_edit_distance(input):

    input_list = input
#    print 'input_list is now %s'%input_list
    count = 0 
    i = 0
    for each in input_list:
        tmp_list = list(input_list)
#        print 'tmp_list is now %s'%tmp_list
        tmp_list.remove(each)
        j = 0
#        print 'tmp_list is now %s'%tmp_list
        for each_1 in tmp_list:
            j = j + int(editdistance.eval(each, each_1))
        i = i + j
        count = count + 1
#    print 'Has interated for %s times'%count
#    print 'total edit distance is %s'%i
    ave_i = float(i) / float((len(input_list)*(len(input_list)-1)))
#    print 'Average edit distance is %s'%ave_i
    return ave_i

def cross_calculate_ave_edit_distance(input1, input2):

    input_list1 = input1
    input_list2 = input2

#    print 'input_list is now %s'%input_list
    count = 0 
    i = 0
    for each in input_list1:
        j = 0
#        print 'tmp_list is now %s'%tmp_list
        for each_1 in input_list2:
            j = j + int(editdistance.eval(each, each_1))
        i = i + j
        count = count + 1
#    print 'Has interated for %s times'%count
#    print 'total edit distance is %s'%i
    ave_i = float(i) / float( (len(input_list1) * (len(input_list2)) ))
#    print 'Average edit distance is %s'%ave_i
    return ave_i



@timeit
def get_top_down_result(number):
    logging.basicConfig(filename='edit_distance.log', level=logging.INFO)
    logging.info('Goal: to calculate edit distance of every element to other elements in a list...')
    logging.info('Started!')
    ave_alexa_edit_distance = 0
    ave_dicdga_edit_distance = 0

    alexa_list = []
    for each in generator_list_good(number):
#        print each
        alexa_list.append(each)
#    print alexa_list
    ave_alexa_edit_distance = calculate_ave_edit_distance(alexa_list)
#creating bad
    bad_list = []
    for each in generator_list_bad(number):
#        print each
        bad_list.append(each)
#    print bad_list
    ave_dicdga_edit_distance = calculate_ave_edit_distance(bad_list)

    print 'alexa list has %s'%len(alexa_list)
    print 'bad list has %s'%len(bad_list)
    print 'the average edit distance of alexa list of %s is %s'%(len(alexa_list),ave_alexa_edit_distance)
    print 'the average edit distance of dic-based dga list of %s is %s'%(len(bad_list), ave_dicdga_edit_distance)
    logging.info('***get_top_down_result***')
    logging.info('alexa list has %s'%len(alexa_list))
    logging.info('bad list has %s'%len(bad_list))
    logging.info('the average edit distance of alexa list of %s is %s'%(len(alexa_list),ave_alexa_edit_distance))
    logging.info('the average edit distance of dic-based dga list of %s is %s'%(len(bad_list), ave_dicdga_edit_distance))
    logging.info('********************************')


def get_all_random_result(number):
    logging.basicConfig(filename='edit_distance.log', level=logging.INFO)
    logging.info('Goal: to calculate edit distance of every element to other elements in a list...')
    logging.info('Started!')
    ave_alexa_edit_distance = 0
    ave_dicdga_edit_distance = 0

    alexa_list = []
    for each in generator_random_list_good(number):
#        print each
        alexa_list.append(each)
#    print alexa_list
    ave_alexa_edit_distance = calculate_ave_edit_distance(alexa_list)
#creating bad
    bad_list = []
    for each in generator_random_list_bad(number):
#        print each
        bad_list.append(each)
#    print bad_list
    ave_dicdga_edit_distance = calculate_ave_edit_distance(bad_list)

    print 'alexa list has %s'%len(alexa_list)
    print 'bad list has %s'%len(bad_list)
    print 'the average edit distance of alexa list of %s is %s'%(len(alexa_list),ave_alexa_edit_distance)
    print 'the average edit distance of dic-based dga list of %s is %s'%(len(bad_list), ave_dicdga_edit_distance)
    logging.info('***get_all_random_result***')
    logging.info('alexa list has %s'%len(alexa_list))
    logging.info('bad list has %s'%len(bad_list))
    logging.info('the average edit distance of alexa list of %s is %s'%(len(alexa_list),ave_alexa_edit_distance))
    logging.info('the average edit distance of dic-based dga list of %s is %s'%(len(bad_list), ave_dicdga_edit_distance))
    logging.info('********************************')


def get_fixed_alexa_but_random_dga_result(number):
    logging.basicConfig(filename='edit_distance.log', level=logging.INFO)
    logging.info('Goal: to calculate edit distance of every element to other elements in a list...')
    logging.info('Started!')
    ave_alexa_edit_distance = 0
    ave_dicdga_edit_distance = 0

    alexa_list = []
    for each in generator_list_good(number):
#        print each
        alexa_list.append(each)
#    print alexa_list
    ave_alexa_edit_distance = calculate_ave_edit_distance(alexa_list)
#creating bad
    bad_list = []
    for each in generator_random_list_bad(number):
#        print each
        bad_list.append(each)
#    print bad_list
    ave_dicdga_edit_distance = calculate_ave_edit_distance(bad_list)
    print '***get_fixed_alexa_but_random_dga_result***'
    print 'alexa list has %s'%len(alexa_list)
    print 'bad list has %s'%len(bad_list)
    print 'the average edit distance of alexa list of %s is %s'%(len(alexa_list),ave_alexa_edit_distance)
    print 'the average edit distance of dic-based dga list of %s is %s'%(len(bad_list), ave_dicdga_edit_distance)
    logging.info('***get_fixed_alexa_but_random_dga_result***')
    logging.info('alexa list has %s'%len(alexa_list))
    logging.info('bad list has %s'%len(bad_list))
    logging.info('the average edit distance of alexa list of %s is %s'%(len(alexa_list),ave_alexa_edit_distance))
    logging.info('the average edit distance of dic-based dga list of %s is %s'%(len(bad_list), ave_dicdga_edit_distance))
    logging.info('********************************')

#get_top_down_result(10)
#get_fixed_alexa_but_random_dga_result(10)
#get_all_random_result(10)

def get_cross_fixed_alexa_but_random_dga_result(number):
    logging.basicConfig(filename='edit_distance.log', level=logging.INFO)
    logging.info('Goal: to calculate edit distance of every element to other elements in a list...')
    logging.info('Started!')
    ave_distance_between_alexa_and_dga = 0
    ave_dicdga_edit_distance = 0

    alexa_list = []
    for each in generator_list_good(number):
#        print each
        alexa_list.append(each)
#    print alexa_list
#    ave_alexa_edit_distance = calculate_ave_edit_distance(alexa_list)
#creating bad
    bad_list = []
    for each in generator_random_list_bad(number):
#        print each
        bad_list.append(each)
#    print bad_list
    ave_distance_between_alexa_and_dga = cross_calculate_ave_edit_distance(alexa_list, bad_list)
#    ave_dicdga_edit_distance = calculate_ave_edit_distance(bad_list)
    print '***get_fixed_alexa_but_random_dga_result***'
    print 'alexa list has %s'%len(alexa_list)
    print 'bad list has %s'%len(bad_list)
    print 'the average edit distance between alexa and dic_dga of size %s is %s'%(len(alexa_list),ave_distance_between_alexa_and_dga)
    logging.info('***get_fixed_alexa_but_random_dga_result***')
    logging.info('alexa list has %s'%len(alexa_list))
    logging.info('bad list has %s'%len(bad_list))
    logging.info('the average edit distance of alexa and dic_dga of size %s is %s'%(len(alexa_list),ave_distance_between_alexa_and_dga))
    logging.info('********************************')

#get_cross_fixed_alexa_but_random_dga_result(10)

sample_number_list = [10, 50, 300, 500, 700, 1000, 1500, 2000, 3000, 4000]
for each in sample_number_list:
#    get_top_down_result(each)
#    get_fixed_alexa_but_random_dga_result(each)
#    get_all_random_result(each)
    get_cross_fixed_alexa_but_random_dga_result(each)
