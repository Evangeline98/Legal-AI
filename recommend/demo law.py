#!/usr/bin/env python
# coding: utf-8
import pymysql
import numpy as np
import pandas as pd 

def recommendlaw(intention,dbcon,number):
    """
    intention: np.array 意图 
    dbcon: database connection
    number: number of recommended laws
    """
    
    lawset = pd.DataFrame(columns= ('article','num'))
    for i in range(intention.shape[0]):

        sql1 = """SELECT article,1 as num FROM cn_company WHERE article like '%""" + intention[i] + """%'""" 
        #append dataframe
        lawset = lawset.append(pd.read_sql_query(sql1,db),ignore_index=True)
    query = pd.DataFrame(lawset)
    #rank according to matching objectives
    recommend = query.groupby('article').sum().sort_values('num',ascending = False)
    return(recommend[:number])

if __name__ == 'main':
    intention = np.array(["合同","生产","劳动","仲裁"])
    db = pymysql.connect(
         host="cdb-74dx1ytr.gz.tencentcdb.com",
         user="root",
         passwd="sufelaw2019",
         port=10008,
         db = 'cn_law')
    
   recommendlaw(intention,db,3)




