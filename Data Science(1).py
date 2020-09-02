#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import lxml.html as lh
import requests


# In[2]:


url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
#create a page to handle contents of the website
page=requests.get(url)
#store the contents of the page under doc
doc=lh.fromstring(page.content)
#Noe parse data stored between <tr>...<tr> of html
tr_elements=doc.xpath('//tr')


# In[3]:


[len(T) for T in tr_elements[:15]]


# In[4]:


tr_elements=doc.xpath('//tr')
col=[]
i=0
# for each row, store a header and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print('%d:"%s"'%(i,name))
    col.append((name,[]))


# In[5]:


#lets store data on the second row going onwards
for j in range(1,len(tr_elements)):
    #T is the j'th row
    T=tr_elements[j]
    #if row is not of size 3, then the //tr data is not from our table
    if len(T)!=3:
        break
    #i is our column index
    i=0
    #Now iterate though each column of the row
    for t in T.iterchildren():
        data=t.text_content()
        #Now check if row is empty
        if i>0:
            #convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #append the data to the empty list of the i'th column
        col[i][1].append(data)
        #increament i for the next column
        i+=1


# In[6]:


[len(C) for (title,C) in col]


# In[7]:


dict={title:column for (title,column) in col}
df=pd.DataFrame(dict)
cols=df.columns.tolist()
df=df[cols]
df.head()


# In[8]:


df.columns=['Postal Code','Borough','Neighbourhood']
df=df.replace('\n','',regex=True)
df.head()


# In[10]:


df.drop(df.index[df['Borough']=='Not assigned'],inplace = True)
#drop previous index and reset the index
df=df.reset_index(drop=True)
df.head(10)


# In[11]:


df=df.groupby(['Postal Code','Borough'])['Neighbourhood'].apply(','.join).reset_index()
df.columns=['Postal Code','Borough','Neighbourhood']
df.head(10)


# In[12]:


df.drop(df.index[df['Borough']=='Not assigned'], inplace=True)


# Combining neighbourhoods with similar postal codes and borough

# In[13]:


df=df.groupby(['Postal Code','Borough'])['Neighbourhood'].apply(','.join).reset_index()
df.columns=['Postal Code','Borough','Neighbourhood']
df.head(10)


# Removing any space in the start of the string

# In[14]:


df['Neighbourhood']=df['Neighbourhood'].str.strip()


# Assigning borough values to the neighbourhood with 'Not assigned'

# In[15]:


df.loc[df['Neighbourhood']=='Not assigned','Neighbourhood']=df['Borough']
df.head()


# In[16]:


df.shape


# In[ ]:




