#!/usr/bin/env python
# coding: utf-8

# In[1]:


def recommendcase(location,quality,compensate,dbcon,number):
    """
    location: np.array
    quality: np.array
    compensate: np.array
    dbcon: database connection
    number: number of recommended cases
    """
    import pandas as pd 
    

    caseset = pd.DataFrame(columns= ('caseid','num'))
    
    if location.shape[0]:
        for i in range(location.shape[0]):
            #match keywords
            sql1 = """SELECT caseid ,summary , 1 as num FROM product_dispute.summary_case WHERE summary like '%""" + location[i] + """%'""" 
            #append dataframe
            caseset = caseset.append(pd.read_sql_query(sql1,db),ignore_index=True)
            #print(caseset)
    if quality.shape[0]:
        for i in range(quality.shape[0]):
            sql1 = """SELECT caseid ,summary,1 as num FROM product_dispute.summary_case WHERE summary like '%""" + quality[i] + """%'""" 
            #append dataframe
            caseset = caseset.append(pd.read_sql_query(sql1,db),ignore_index=True)
    if compensate.shape[0]:
        for i in range(compensate.shape[0]):
            sql1 = """SELECT caseid ,summary,1 as num FROM product_dispute.summary_case WHERE ask like '%""" + quality[i] + """%'""" 
            #append dataframe
            caseset = caseset.append(pd.read_sql_query(sql1,db),ignore_index=True)

            sql2 = """SELECT caseid ,summary,1 as num FROM product_dispute.summary_case WHERE results like '%""" + quality[i] + """%'""" 
            #append dataframe
            caseset = caseset.append(pd.read_sql_query(sql2,db),ignore_index=True)
        
    query = pd.DataFrame(caseset)

    recommend = query.groupby('caseid').sum().sort_values('num',ascending = False)
    recommend['caseid'] = recommend.index
    
    return(recommend.iloc[:number,[1,2]])

    
    


# In[2]:


if __name__ == 'main':
    import pymysql
    import numpy as np
    db = pymysql.connect(
         host="cdb-74dx1ytr.gz.tencentcdb.com",
         user="root",
         passwd="sufelaw2019",
         port=10008,
         db = 'product_dispute')

    location = np.array(['市场'])
    quality = np.array(['过期', '超过保质期'])
    compensate = np.array(['医药费'])
    recommendcase(location,quality,compensate,db,2)##return a dataframe of summary and index


# In[ ]:




