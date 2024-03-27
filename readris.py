import rispy
import pandas as pd
import numpy as np

# https://github.com/MrTango/rispy

#I rather use this instead of python's None
none = "### Empty field ###"


def readris(file):
        bibFile = open(file, 'r', encoding="utf-8")

        entries = rispy.load(bibFile, encoding='utf-8')   

        # 'entries' is a list of dictionaries. Each dict is a different paper

        rawData = []

        # we want to extract only the usefull information
        for entry in entries:
                try: title = entry['title']
                except: title = none

                try:
                        firstAuthor = entry['authors'][0]
                        authors = entry['authors']                
                except:
                        firstAuthor = none
                        authors = none                

                try: abstract = entry['abstract']
                except: abstract = none

                try: keywords = entry['keywords']
                except: keywords = none

                try: year = (entry['year'])
                except: year = none
                
                try: doi = entry['doi']
                except: doi = none

                try: doi = entry['doi']
                except: doi = none

                try: ty = entry['type_of_reference']
                except: ty = none

                
                reg = [title, firstAuthor, authors, abstract, keywords, year, doi, ty]
                rawData.append(reg)
        return rawData



def ris(fileList):

        dfIndex = ['title', 'FirstAuthor', 'Authors', 'abstract', 'keywords', 'year', 'doi', "type"]
        dfIndex2 = ['responseId', 'logprobs', 'created', 'model', 'fingerprint', 'completionTokens', 'promptTokens', 'totalTokens', 'setting', 'focus', 'application', 'context', 'objectives', 'methods', 'results', 'rateofSuccess']


        bibData =[]

        for file in fileList:
                #here we concatenate the files
                bibData = bibData + readris(file)


        #generates the dataframe:
        try:
                pdDB = pd.DataFrame(bibData,columns=dfIndex)
        except:
                pdDB = pd.DataFrame(bibData,index=dfIndex)


        pdDB = pdDB.transpose()
        emptyDF = pd.DataFrame(index=dfIndex2)

        pdDB = pd.concat([pdDB, emptyDF]).transpose()

        #removes duplicated based on title
        pdDB = pdDB.drop_duplicates(subset='title', ignore_index=True)

        return(pdDB)
