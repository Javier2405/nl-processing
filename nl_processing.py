from distutils.file_util import write_file
from multiprocessing import managers
import re
import csv
import nltk
from nltk.corpus import stopwords
import time
from ast import literal_eval
from datascience import *
import math

class text_filter():
    def __init__(self,language):
        self.language=language
        self.manager=csv_manager()
        self.utilities=utilities()
        self.wnl = nltk.WordNetLemmatizer()
        self.porter = nltk.PorterStemmer()
        self.lancaster = nltk.LancasterStemmer()
        pass

    def cleaning_data(self,path):
        reviews_raw,summarys_raw=self.manager.read_file(path,8,6)
        summarys=self.filter(summarys_raw,"lem")
        reviews=self.filter(reviews_raw,"lem")
        self.manager.write_file("lem.csv",[summarys,reviews])
        summarys=self.filter(summarys_raw,"stem")
        reviews=self.filter(reviews_raw,"stem")
        self.manager.write_file("stem.csv",[summarys,reviews])
        summarys=self.filter(summarys_raw,"stem_lancaster")
        reviews=self.filter(reviews_raw,"stem_lancaster")
        self.manager.write_file("lancaster.csv",[summarys,reviews])
        summarys=self.filter(summarys_raw,"stem_porter")
        reviews=self.filter(reviews_raw,"stem_porter")
        self.manager.write_file("porter.csv",[summarys,reviews])

    def remove_stopwords(self,sentence):
        #self.utilities.sayhi(self.remove_stopwords.__name__)
        return [token for token in sentence if token.lower() not in stopwords.words(self.language)]

    def remove_punctuation(self,sentence):
        punc = r'''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        return [token for token in sentence if token.lower() not in punc]

    def stem_word(self,word):
        regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
        stem, suffix = re.findall(regexp, word)[0]
        return stem

    def stem_sentence(self,sentence):
        #self.utilities.sayhi(self.stem_sentence.__name__)
        return [self.stem_word(token) for token in sentence]

    def lemmatization(self,sentence):
        return [self.wnl.lemmatize(token) for token in sentence]

    def stem_porter(self,sentence):
        return [self.porter.stem(token) for token in sentence]

    def stem_lancaster(self,sentence):
        return [self.lancaster.stem(token) for token in sentence]

    def filter(self, array,method):
        self.utilities.sayhi(self.filter.__name__ +" "+method)
        if method=="lem":
            return [self.lemmatization(self.remove_punctuation(self.remove_stopwords(nltk.word_tokenize(sentence)))) for sentence in array]
        elif method=="stem":
            return [self.stem_sentence(self.remove_punctuation(self.remove_stopwords(nltk.word_tokenize(sentence)))) for sentence in array]
        elif method=="stem_lancaster":
            return [self.stem_porter(self.remove_punctuation(self.remove_stopwords(nltk.word_tokenize(sentence)))) for sentence in array]
        elif method=="stem_porter":
            return [self.stem_lancaster(self.remove_punctuation(self.remove_stopwords(nltk.word_tokenize(sentence)))) for sentence in array]

class text_analysis():
    def __init__(self):
        self.manager=csv_manager()
        self.tdm_summarys={}
        self.tdm_reviews={}
        self.dtm_summarys={}
        self.dtm_reviews={}

    def generate_tdm(self,path):
        reviews,summarys=self.manager.read_file(path,0,1)
        reviewsDict={}
        summarysDict={}
        dtm_reviews={}
        dtm_summarys={}
        for doc in range(len(reviews)):
            '''for word in literal_eval(reviews[doc]):
                if word.lower() not in reviewsDict.keys():
                    reviewsDict[word.lower()]={"total":1,doc:1}
                elif doc not in reviewsDict[word.lower()].keys():
                    reviewsDict[word.lower()][doc]=1
                    reviewsDict[word.lower()]["total"]+=1
                else:
                    reviewsDict[word.lower()][doc]+=1
                    reviewsDict[word.lower()]["total"]+=1'''
            for word in literal_eval(reviews[doc]):
                #TDM
                if word.lower() not in reviewsDict.keys():
                    reviewsDict[word.lower()]={"total":1,doc:1}
                elif doc not in reviewsDict[word.lower()].keys():
                    reviewsDict[word.lower()][doc]=1
                    reviewsDict[word.lower()]["total"]+=1
                else:
                    reviewsDict[word.lower()][doc]+=1
                    reviewsDict[word.lower()]["total"]+=1
                #DTM
                if doc not in dtm_reviews.keys():
                    dtm_reviews[doc]={"terms":{word.lower():{"times":1}}}
                elif word.lower() not in dtm_reviews[doc].keys():
                    dtm_reviews[doc]["terms"][word.lower()]={"times":1}
                else:
                    dtm_reviews[doc]["terms"][word.lower()]["times"]+=1
            for word in literal_eval(summarys[doc]):
                #TDM
                if word.lower() not in summarysDict.keys():
                    summarysDict[word.lower()]={"total":1,doc:1}
                elif doc not in summarysDict[word.lower()].keys():
                    summarysDict[word.lower()][doc]=1
                    summarysDict[word.lower()]["total"]+=1
                else:
                    summarysDict[word.lower()][doc]+=1
                    summarysDict[word.lower()]["total"]+=1
                #DTM
                if doc not in dtm_summarys.keys():
                    dtm_summarys[doc]={"terms":{word.lower():{"times":1}}}
                elif word.lower() not in dtm_summarys[doc].keys():
                    dtm_summarys[doc]["terms"][word.lower()]={"times":1}
                else:
                    dtm_summarys[doc]["terms"][word.lower()]["times"]+=1
        
        '''docs=[]
        for index in range(len(summarys)):
            print(index)
            doc={'doc':index}
            for word in summarysDict:
                #print(summarysDict[word].keys())
                if index in summarysDict[word].keys():
                    doc[word]=summarysDict[word][index]
                else:
                    doc[word]=0
            docs.append(doc)'''
        
        #t = Table().from_records(docs)
        '''t = Table().from_records([
            {'column1':'data1','column2':1}, 
            {'column1':'data2','column2':2}, 
            {'column1':'data3','column2':3}
        ])'''
        #summarysTable=Table().from_records([summarysDict])
        '''for word in summarysDict:
            summarysTable.append_column(word)'''

        #print(t.rows)
        self.tdm_summarys=summarysDict
        self.tdm_reviews=reviewsDict
        self.dtm_summarys=dtm_summarys
        self.dtm_reviews=dtm_reviews
        print(self.tdm_summarys)
        print("Total terminos en summarys: "+str(len(self.tdm_summarys.keys())))
        print("Total terminos en reviews: "+str(len(self.tdm_reviews.keys())))

    def obtain_tf_idf(self):
        total_docs=len(self.dtm_summarys.keys())
        for doc in self.dtm_summarys:
            total_terms_in_doc=len(self.dtm_summarys[doc]["terms"].keys())
            for term in self.dtm_summarys[doc]["terms"]:
                tf=self.dtm_summarys[doc]["terms"][term]["times"]/total_terms_in_doc
                idf=math.log(total_docs/self.tdm_summarys[term]["total"])
                tf_idf=tf*idf
                self.dtm_summarys[doc]["terms"][term]["tf-idf"]=tf_idf
                self.dtm_summarys[doc]["terms"][term]["tf"]=tf
                self.dtm_summarys[doc]["terms"][term]["idf"]=idf
        self.manager.write_file_tf_idf("dtm_summarys.csv",self.dtm_summarys)
        for doc in self.dtm_reviews:
            total_terms_in_doc=len(self.dtm_reviews[doc]["terms"].keys())
            for term in self.dtm_reviews[doc]["terms"]:
                tf=self.dtm_reviews[doc]["terms"][term]["times"]/total_terms_in_doc
                idf=math.log(total_docs/self.tdm_reviews[term]["total"])
                tf_idf=tf*idf
                self.dtm_reviews[doc]["terms"][term]["tf-idf"]=tf_idf
                self.dtm_reviews[doc]["terms"][term]["tf"]=tf
                self.dtm_reviews[doc]["terms"][term]["idf"]=idf
        self.manager.write_file_tf_idf("dtm_reviews.csv",self.dtm_reviews)




class csv_manager():
    def __init__(self):
        self.utilities=utilities()

    def read_file(self,file,column_s,column_r):
        self.utilities.sayhi(self.read_file.__name__)
        reviews=[]
        summarys=[]
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    review=row[column_r]
                    summary=row[column_s]
                    reviews.append(review)
                    summarys.append(summary)
                else:
                    line_count= 1
        return reviews,summarys

    def write_file(self,file,data):
        self.utilities.sayhi(self.write_file.__name__)
        with open(file, mode='w',newline="") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for entry in range(len(data[0])):
                writer.writerow([data[0][entry],data[1][entry]])
    
    def write_file_tf_idf(self,file,data):
        with open(file, mode='w',newline="") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Document","Term","tf","idf","tf-idf"])
            for doc in data:
                for term in data[doc]["terms"]:
                    writer.writerow([doc,term,data[doc]["terms"][term]["tf"],data[doc]["terms"][term]["idf"],data[doc]["terms"][term]["tf-idf"]])
                
    def write_file_words(self,file,data_docs,data_words):
        with open(file, mode='w',newline="") as write_file:
            writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            my_columns=["Word"]+data_docs.keys()
            writer.writerow(my_columns)
            for term in data_words:
                index_control=1
                aux_arr=[]
                for doc in data_words[term]:
                    if doc=="total":
                        continue
                    index_control+=doc
                    writer.writerow([term]+[])

class utilities():
    def __init__(self):
        self.time=0
        pass

    def sayhi(self,function):
        print(self.get_timer()+" : [ "+function+":executing ]")
        #print("Executing "+function+" function")

    def get_timer(self):
        return str(time.perf_counter())

def main():
    tf=text_filter("english")
    #tf.cleaning_data("reviews_Baby_5_final_dataset.csv")
    analyzer=text_analysis()
    analyzer.generate_tdm("resources/stem.csv")
    analyzer.obtain_tf_idf()

main()