#!/usr/bin/env python
# coding: utf-8

# In[77]:


import re
import json


# In[78]:


dataset = open('./lv4.json','rb')
dic = json.load(dataset)


# In[79]:


def get_name( s ):
    _name = s[:s.find(',')]
    return _name


# In[80]:


def get_tel(s):
    _tel = re.findall( r'[0-9]{11}', s)
    return _tel


# In[81]:


def get_province(s, d):
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw, d[it]['c']
    return ""


# In[82]:


def get_city(s, d):
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw, d[it]['c']
    return ""


# In[83]:


def get_town(s, d):
    #print("dict=", d)
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw, d[it]['c']
    return ""


# In[84]:


def get_block(s, d):
    #print(d)
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw
    return ""


# In[85]:


def clr(s, ss):
    pos = s.find(ss)
    ans = s[:pos] + s[pos+len(ss):]
    return ans


# In[86]:


def solve(s, noise):
    while (1):
        ct = 0
        for i in noise:
            pos = s.find(i)
            if ( pos == 0 ):
                s = clr(s,i)
            else:
                ct += 1
        if ( ct == len(noise) ):
            break
    return s


# In[87]:


def analy(s, l):
    for i in l:
        pos = s.find(i)
        if ( pos >= 0 ):
            return i
    return ""


# In[88]:


def main(s, d):
    
    lv1 = ['省','市','自治区']
    lv3 = ['区','县']
    lv4 = ['镇','乡','街道']
    lv527 = ['路','街']
    directly = ['北京','天津','上海','重庆']
    autonomous = ['宁夏回族','广西','内蒙古','新疆维吾尔族','西藏']
    
    json_info = {}
    address = []
    
    dic = d
    s = s[:len(s)-1]
    
    _name = get_name(s)
    #print(_name)
    json_info['姓名'] = _name
    s = s[s.find(',')+1:]
    
    _tel = ''.join(get_tel(s))
    #print(_tel)
    json_info['手机'] = _tel
    s = clr(s,_tel)
    
    
    #print(s)
    #get lv1
    _prov, dic = get_province(s, dic)
    #print(_prov)
    if (_prov in directly) == False:
        s = clr(s,_prov)
        
    if _prov in directly:
        _prov += lv1[1]
    elif _prov in autonomous:
        _prov += lv1[2]
    else:
        _prov += lv1[0]
    address.append(_prov)
    
    #print(s)
    #get lv2
    _city, dic = get_city(s, dic)
    #print(_city)
    s = clr(s,_city)
    _city += lv1[1]
    address.append(_city)
    s = solve(s,lv1)
    
    #print(s)
    #get lv3
    sz = len(dic)
    if sz > 1:
        _town, dic = get_town(s, dic)
    else:
        _town = analy(s, lv3)
    #print(_town)
    s = clr(s,_town)
    for i in lv3:
        if s.find(i) >= 0:
            _town += i
            break
    address.append(_town)
    s = solve(s,lv3)
    
    #print(s)
    #get lv4
    sz = len(dic)
    if sz > 1:
        _block = get_block(s, dic)
    else:
        _block = analy(s, lv4)
    #print(_block)
    s = clr(s,_block)
    for i in lv4:
        if s.find(i) >= 0:
            _block += i
            break;
    address.append(_block)
    s = solve(s,lv4)
    
    
    #get lv5 to lv7, in short is lv52(to)7
    #print(s)
    address.append(s)
    
    json_info['地址'] = address
    
    print(json_info)
    json.dump( json_info, open('./json_out.json', 'w', encoding='utf-8'), ensure_ascii=False )
    #return s


# In[93]:


s = input()
main(s,dic)


# In[ ]:




