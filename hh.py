#!/usr/bin/env python
# coding: utf-8

# TODO:
#    - [ ] перевести формирование счетчика навыков в функцию
#    - [ ] добавить обьединенную сортировку по заработной плате
#    - [ ] на основе вышеприведенных пунктовЖ добавить просмотр навыков по 0.XX самым высокооплачиваемым вакансиям
#    - [x] try - except блок при загрузке данных с сайта
#    - [ ] сделать приложением?

# In[108]:


import requests
from tqdm.notebook import tqdm
from datetime import datetime
from dateutil.parser import parse

import re
import time
from collections import Counter

import pandas as pd


# In[2]:


#dir(requests)


# In[3]:


get_ipython().run_line_magic('pylab', 'inline')


# In[ ]:





# In[4]:


addr = 'https://api.hh.ru/vacancies'
head = {'User-Agent': 'NoApp'}


# In[21]:


vacancies_list = [ 'Data scientist',
'Data science', 
'Ml specialist', 
'Machine learning', 
#'Data Analyst',
#'master data',
'ML']


# In[ ]:





# 'area': {'id': '1', 'name': 'Москва'...}    
# 'salary': {'from': 300000, 'to': None, 'currency': 'RUR', 'gross': False}    
# 'description': {'......'}    
# 'key_skills': [{'name': 'Мат стат'}, {'name': 'Мат анализ'}, {'name': 'Python'}, {'name': 'Git'}]     
# 'published_at': YYYY-MM-DDThh:mm:ss±hhmm

# ### Забираем данные по вакансиям с hh

# In[22]:


clr = lambda x: (re.sub(r'<.*?>', '', str(x)))
BREAK_STOP_LEVEL = 3


# In[187]:


get_ipython().run_cell_magic('time', '', '\nid_list     = list()\narea_list   = list()\ndescr_list  = list()\nsalary_from_list = list()\nsalary_to_list   = list()\nsalary_cur_list  = list()\nkey_skills_list  = list()\n\ndate_list = list()\n\nbreaks_count = 0\n\nfor element in vacancies_list:\n    new_ones = 0\n    \n    #getting amount of all vacancies\n    try:\n        answ = requests.get(addr, params={\'text\':element}, headers = head)\n        if answ.status_code != 200:\n            print(\'Error get info with \' + element + \' tag\')\n            break\n    except:\n        print(\'exception try to get list of vacansies for profession\')\n        breaks_count += 1\n        print(\'end\')\n        break\n        \n    print(answ.url)\n    time.sleep(1)\n    \n    info_tag = answ.json()\n    amnt_pages = info_tag[\'pages\']\n    amnt_found = info_tag[\'found\']\n    \n    # amnt_pages\n    for page in tqdm(range(amnt_pages)):\n        # going through all pages\n        try:\n            answ = requests.get(addr, params={\'text\':element, \'page\':page}, headers = head)\n            if answ.status_code != 200:\n                print(\'Error get info with \' + element + \' tag on page \' + str(page))\n                break\n        except:\n            print(f\'exception try to get next list of vacansies for {element}\')\n            breaks_count += 1\n            if breaks_count > BREAK_STOP_LEVEL:\n                break\n            continue\n            \n        info_tag_page = answ.json()\n        info_tag_page = info_tag_page[\'items\']\n        if len(info_tag_page) == 0:\n            break\n        \n        #len(info_tag_page)\n        for vac in range( len(info_tag_page) ):\n            #going through all vacancies on pages \n            if info_tag_page[vac][\'id\'] in id_list:\n                break\n            \n            try:\n                #print(info_tag_page[vac][\'id\'])\n                answ = requests.get(addr + \'/\' + info_tag_page[vac][\'id\'], headers = head)\n                if answ.status_code != 200:\n                    print(\'Error get info about vacancia \' + info_tag_page[vac][\'id\'])\n                    break  \n            except:\n                print(\'exception try to get vacancy description\')\n                breaks_count += 1\n                if breaks_count > BREAK_STOP_LEVEL:\n                    break\n                continue\n            vacancy = answ.json()\n            \n            id_list.append(vacancy[\'id\'])\n            \n            if isinstance(vacancy[\'area\'], type(None)):\n                area_list.append(\'\')\n            else:\n                area_list.append(  vacancy[\'area\'][\'name\'].lower())  # id name\n            \n            if isinstance(vacancy[\'description\'], type(None)):\n                descr_list.append(\'\')\n            else:\n                descr_list.append(  clr(vacancy[\'description\']).lower())  # id name\n            \n            \n            if isinstance(vacancy[\'salary\'], type(None)):\n                salary_from_list.append( None )   # from to\n                salary_to_list.append(   None )   # from to\n                salary_cur_list.append(  None )\n            else:\n                salary_from_list.append( vacancy[\'salary\'][\'from\']) # from to\n                salary_to_list.append(   vacancy[\'salary\'][\'to\'])   # from to\n                salary_cur_list.append(  vacancy[\'salary\'][\'currency\'].lower())\n            \n                        \n            #if len(vacancy[\'key_skills\']) > 0:\n            #    for skill in range( len(vacancy[\'key_skills\']) ):   # name name name name.....\n            #        key_skills_list.append(  vacancy[\'key_skills\'][skill][\'name\'].lower())\n            key_skills_list.append(  vacancy[\'key_skills\'] )   \n            \n            date_list.append( parse(vacancy[\'published_at\'], ignoretz = True) )\n            new_ones += 1\n                   \n    print(\'Found \' + str(amnt_found) + \' vacancies with key words "\' + element + \'" with \' + str(new_ones) + \' not in list\')\n    \n    \nprint(\'\\nDone\')')


# In[ ]:





# ### Зачищаем вакансии так, что бы при наличии в одной вакансии нескольких библиотек js, оставался бы только один js. и т.п.

# In[188]:


key_skills_list[:5]


# In[189]:


# для обьединения
javascript_list = ['javascript', 'node.js', 'js', 'react', 'react.js', 'reactjs', 'jquery', 'angularjs', 'jquery', 'vue.js', 'vuejs', 'vue', 'backbone', 'redux']

skill_dict = {'анализ данных':'data analysis', 'машинное обучение':'machine learning',
              'ml':'machine learning', 'разработка по':'software development',
              'data scientist': 'data science',
              'opencv': 'computoe vision', 'cv': 'computoe vision', 'компьютерное зрение': 'computoe vision',
              'анализ данных':'data analysis', 'бизнес-анализ':'business analysis',
              'базы данных':'работа с базами данных', 'html5':'html', 
              'проведение презентаций':'presentation skills',
              #?'тестирование': 'a/b', 'qa'
              'kubernetes': 'kubernates',
              'k8s': 'kubernates',
              'marketing analysis': 'маркетинговый анализ',
              'analytical skills': 'аналитическое мышление',
              'cистемы управления базами данных': 'cубд',
              'ms access': 'office', 'ms powerpoint': 'office', 'ms excel': 'office',
              'ms office': 'office', 'ms visio': 'office', 'ms outlook': 'office',#'ms project': 'office', 
              'ms sharepoint': 'office', 
              'powerbi': 'ms power bi',
              'power bi': 'ms power bi',
              'rest api': 'rest',
              'ruby on rails': 'ruby',
              'natural language processing': 'nlp',
              'go': 'golang',
              'negotiation skills': 'ведение переговоров',
              'bigquery': 'google bigquery',
             }
for_change = skill_dict.keys()


# In[190]:


key_skills = Counter()
for el in tqdm(key_skills_list):
    if len(el) > 1:
        skills = []
        for ind in range(len(el)):
            element = el[ind]['name'].lower()
            
            if 'sql' in element and 'nosql' not in element:
                skills.append('sql')
            elif 'english' in element:
                skills.append('английский язык')
            elif 'c++' in element or 'c' == element:
                skills.append('c/c++')
            elif element in javascript_list:   # should be earlie then 'java'
                skills.append('javascript')
            elif element.startswith('java'):
                skills.append('java')
            elif element.startswith('hadoop'):
                skills.append('hadoop')
                
            elif element.startswith('css'):
                skills.append('css')
                
            elif 'nosql' in element:
                skills.append('nosql')
            elif element.startswith('qa'):
                skills.append('qa')
            elif element.startswith('a/b'):
                skills.append('a/b')
            elif 'тест' in element:
                skills.append('qa')
            elif 'nlp' in element:
                skills.append('nlp')
            elif 'продаж' in element or 'холод' in element:
                skills.append('ignored skills')
            else:
                skills.append(element)
            
            if skills[-1] in for_change:
                skills[-1] = skill_dict[skills[-1]]

        key_skills += Counter(set(skills))


# Посмотрим на требуемые скилы в вакансиях

# In[191]:


show_butch = 0 # какую группу по 50 скилов отображать

for_print = key_skills.most_common()[show_butch*50 : show_butch*50 + 50]
#for_print = key_skills.most_common()[-1*show_butch*50 - 50 : -1*show_butch*50 ]
for el in for_print:
    print(f'{el[1]:3}  {el[0]}')


# In[ ]:





# ### Посмотрим на оплату

# In[192]:


df_slr = pd.DataFrame({'slr_from':salary_from_list, 'slr_to':salary_to_list, 'slr_cur':salary_cur_list})
df_slr.shape


# In[193]:


df_slr.head()


# In[194]:


df_slr[df_slr.slr_cur == 'rur'].slr_from.dropna().shape, df_slr[['slr_from', 'slr_to']].slr_from.dropna().shape


# In[195]:


plt.boxplot( df_slr[df_slr.slr_cur == 'rur'].slr_from.drop(df_slr[df_slr.slr_cur == 'rur'].slr_from.idxmax()).dropna() )


# In[196]:


#plt.boxplot( df_slr[df_slr.slr_cur == 'rur'].slr_to.dropna() )
plt.boxplot( df_slr[df_slr.slr_cur == 'rur'].slr_to.drop(df_slr[df_slr.slr_cur == 'rur'].slr_to.idxmax()).dropna() )


# если предположить, что все вакансии с оплатой больше 30000 в рублях

# In[222]:


plt.boxplot( df_slr.query('slr_from <= 800000 and slr_from > 30000').slr_from.dropna())


# In[223]:


plt.boxplot( df_slr.query('slr_to <= 800000 and slr_to > 30000').slr_to.dropna())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# #### test

# In[6]:


answ = requests.get(addr, params = {'text':'ML'}, headers = head)
print(len(answ.json(), answ.status_code)


# In[8]:


answ.status_code


# In[9]:


info = answ.json()
print( info['found'] )
print( info['pages'] )
print( len(info['items']) )

print( info['items'][0]['id'] )


# In[ ]:





# In[15]:


answ = requests.get(addr + '/' + str(35218725), headers = head)
vac = answ.json()
#vac


# In[25]:


vac


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


#data_ks[0].value_counts()[60:120]


# In[ ]:





# In[ ]:




