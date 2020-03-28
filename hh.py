#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import requests
from tqdm import tqdm
from datetime import datetime
from dateutil.parser import parse


# In[2]:


#dir(requests)


# In[9]:


get_ipython().run_line_magic('pylab', 'inline')


# In[ ]:





# In[3]:


addr = 'https://api.hh.ru/vacancies'
head = {'User-Agent': 'NoApp'}


# In[4]:


vacancies_list = [ 'Data scientist',
'Data science', 
'Ml specialist', 
'Machine learning', 
'Data Analyst',
'ML']


# In[ ]:





# 'area': {'id': '1', 'name': 'Москва'...}    
# 'salary': {'from': 300000, 'to': None, 'currency': 'RUR', 'gross': False}    
# 'description': {'......'}    
# 'key_skills': [{'name': 'Мат стат'}, {'name': 'Мат анализ'}, {'name': 'Python'}, {'name': 'Git'}]     

# 

# In[7]:


id_list     = list()
area_list   = list()
descr_list  = list()
salary_from_list = list()
salary_to_list   = list()
salary_cur_list  = list()
key_skills_list  = list()

date_list = list()

for element in vacancies_list:
    new_ones = 0
    
    #getting amount of all vacancies
    answ = requests.get(addr, params={'text':element}, headers = head)
    if answ.status_code != 200:
        print('Error get info with ' + element + ' tag')
        break
        
    print(answ.url)
    info_tag = answ.json()
    amnt_pages = info_tag['pages']
    amnt_found = info_tag['found']
    
    # amnt_pages
    for page in tqdm(range(amnt_pages)):
        # going through all pages
        answ = requests.get(addr, params={'text':element, 'page':page}, headers = head)
        if answ.status_code != 200:
            print('Error get info with ' + element + ' tag on page ' + str(page))
            break
        info_tag_page = answ.json()
        info_tag_page = info_tag_page['items']
        if len(info_tag_page) == 0:
            break
        
        #len(info_tag_page)
        for vac in range( len(info_tag_page) ):
            #going through all vacancies on pages 
            if info_tag_page[vac]['id'] in id_list:
                break
            
            #print(info_tag_page[vac]['id'])
            answ = requests.get(addr + '/' + info_tag_page[vac]['id'], headers = head)
            if answ.status_code != 200:
                print('Error get info about vacancia ' + info_tag_page[vac]['id'])
                break  
            
            vacancy = answ.json()
            
            id_list.append(    vacancy['id'])
            
            if isinstance(vacancy['area'], type(None)):
                area_list.append('')
            else:
                area_list.append(  vacancy['area']['name'].lower())  # id name
            
            if isinstance(vacancy['description'], type(None)):
                descr_list.append('')
            else:
                descr_list.append(  vacancy['description'].lower())  # id name
            
            
            if isinstance(vacancy['salary'], type(None)):
                salary_from_list.append( None )   # from to
                salary_to_list.append(   None )   # from to
                salary_cur_list.append(  None )
            else:
                salary_from_list.append( vacancy['salary']['from']) # from to
                salary_to_list.append(   vacancy['salary']['to'])   # from to
                salary_cur_list.append(  vacancy['salary']['currency'].lower())
            
                        
            if len(vacancy['key_skills']) > 0:
                for skill in range( len(vacancy['key_skills']) ):   # name name name name.....
                    key_skills_list.append(  vacancy['key_skills'][skill]['name'].lower())   
            
            date_list.append( parse(vacancy['published_at'], ignoretz = True) )
            new_ones += 1
                   
    print('Found ' + str(amnt_found) + ' vacancies with key words "' + element + '" with ' + str(new_ones) + ' not in list')
    
    
print('\nDone')


# In[ ]:





# In[ ]:


answ = requests.get(addr, params = {'text':'ML'}, headers = head)


# In[ ]:


len(answ.json())


# In[ ]:


answ.status_code


# In[ ]:


info = answ.json()
print( info['found'] )
print( info['pages'] )
print( len(info['items']) )

print( info['items'][0]['id'] )


# In[ ]:





# In[ ]:


#answ = requests.get(addr + '/' + info['items'][0]['id'], headers = head)
answ = requests.get(addr + '/' + str(35218725), headers = head)


# In[ ]:


vac = answ.json()


# In[ ]:


vac


# In[ ]:





# In[ ]:





# In[8]:


print(len(id_list))
print(id_list[:5])
print(area_list[:5])
#print(descr_list[:5])
print(salary_from_list[:5])
print(salary_to_list[:5])
print(salary_cur_list[:5])
print(key_skills_list[:5])
print(date_list[:5])


# In[ ]:


vacancy


# In[ ]:





# In[ ]:





# In[ ]:




