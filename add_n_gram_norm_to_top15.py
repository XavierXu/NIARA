import logging
import csv

#df = pd.read_csv('test_out.csv')
#saved_column = df.column_name #you can also use df['column_name']

#print saved_column
logging.basicConfig(filename='tmp.log', level=logging.INFO)
logging.info('Goal: to add 23gram normality score to lexical full data set...')
logging.info('Started to load json file, which is big!')


f = open('23gram_normality_score.json','r')
dic_big = {}
dic_big = eval(f.read())

logging.info('Finished loading the big json file!')

domain_list = []
file_out = open('23gram_norm_score_with_top15_alexa_and_dga.csv','w')
with open('binary_class_train.csv','rb') as csvfile:
    with open('./23gram_norm_score_with_top15_alexa_and_dga.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvfile)
        all = []
        for row in reader:
            col=row[4] #domain
            col1 = row[3] #subdomain
            if col1 == '' or col1 == ' ':
                col2 = col
            else:
                col2 = col1 + '.' + col
    
            bi_gram_norm = 0
            tri_gram_norm = 0
            if col == 'domain':
                bi_gram_norm = 'bi_gram_normality_score'
                tri_gram_norm = 'tri_gram_normality_score'
                logging.info('Writing csv file header!')
            else:
                
                if col2 in dic_big:
                    print 'domain: %s, bi-gram set to, tri-gram set'%col 
                    bi_gram_norm = dic_big[col2][0]
                    tri_gram_norm = dic_big[col2][1]
                else:
                    pass
                   
            print col2
#            domain_list.append(col)
#            characters = ''
#            for each in new_col:
#                characters = characters + ' ' + each
            row.append(bi_gram_norm)
            row.append(tri_gram_norm)
            all.append(row)
#            all.append(col)
#        str="<a href=/" + col.strip().lower()
#        str+= "/>" + col + "</a> "
#        file_out.write(col)
        writer.writerows(all)
logging.info('task done')
