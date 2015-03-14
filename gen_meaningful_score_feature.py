import itertools, enchant
import csv
from pyngram import calc_ngram

#df = pd.read_csv('test_out.csv')
#saved_column = df.column_name #you can also use df['column_name']

#print saved_column

dictionary = enchant.Dict("en_US")

#split the string in all possible places
def break_down(text):
    words = text.split()
    ns = range(1, len(words))
    for n in ns:
        for idxs in itertools.combinations(ns, n):
            yield [' '.join(words[i:j]) for i, j in zip((0,) + idxs, idxs + (None,))]

#compute the maximum meaningful characters ratio
def meaningful_characters(domain):
    if domain == '' or domain == ' '  or len(domain) == 0:
        return 0
#    domain_length = float(len(domain))
#    domain = ''.join([i for i in domain if not i.isdigit()])
    char_count = 0
    ratio = 0.0
#    breakdowns = break_down(" ".join(domain))
    breakdowns = []
    tri_gram_results = calc_ngram(domain, 3)
    four_gram_results = calc_ngram(domain, 4)
    five_gram_results = calc_ngram(domain, 5)
    six_gram_results = calc_ngram(domain, 6)
    for item in tri_gram_results:
        breakdowns.append(item[0])
    for item in four_gram_results:
        breakdowns.append(item[0])
    for item in five_gram_results:
        breakdowns.append(item[0])
    for item in six_gram_results:
        breakdowns.append(item[0])
    for word in breakdowns:
        if dictionary.check(word):
                char_count = char_count + 1
    ratio = char_count/len(domain)
    return ratio


#domain_list = []
file_out = open('meaningful_score_with_hidden_data.csv','w')
with open('Hidden_Alexa_DGA_PaperFeatures_no_mcr.csv','rb') as csvfile:
    with open('./meaningful_score_with_hidden_data.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvfile)
        all = []
        for row in reader:

            col=row[4] #domain
            col1 = row[3] #subdomain
            print 'working on domain %s'%col                
            score = 0
            score1 = 0
            if col == 'domain':
                score = '2nd_domain_meaningful_score'

            else:
                score = meaningful_characters(col)

            if col1 == 'subdomain':
                score1 = '3rd_domain_meaningful_score'
                
            else:
                score1 = meaningful_characters(col1)

            print col
#            domain_list.append(col)
#            characters = ''
#            for each in new_col:
#                characters = characters + ' ' + each
            row.append(score)
            row.append(score1)
            all.append(row)
#            all.append(col)
#        str="<a href=/" + col.strip().lower()
#        str+= "/>" + col + "</a> "
#        file_out.write(col)
        writer.writerows(all)
