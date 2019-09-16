#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import json


# In[3]:


def get_name( s ):
    _name = s[:s.find(',')]
    return _name


# In[4]:


def get_tel(s):
    _tel = re.findall( r'[0-9]{11}', s)
    return _tel


# In[5]:


def get_province(s, d):
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw, d[it]['c']
    return ""


# In[6]:


def get_city(s, d):
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw, d[it]['c']
    return ""


# In[7]:


def get_town(s, d):
    #print("dict=", d)
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw, d[it]['c']
    return ""


# In[8]:


def get_block(s, d):
    #print(d)
    for it in d:
        nw = d[it]['n']
        pos = s.find(nw)
        if ( pos >= 0 ):
            return nw
    return ""


# In[9]:


def clr(s, ss):
    pos = s.find(ss)
    ans = s[:pos] + s[pos+len(ss):]
    return ans


# In[10]:


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


# In[19]:


def analy(s, l):
    for i in l:
        pos = s.find(i)
        if ( pos >= 0 ):
            return s[:pos+len(i)]
    return ""


# In[33]:


def _analysis_lv5(s, d):
    
    lv1 = ['省','市','自治区']
    lv3 = ['区','县']
    lv4 = ['镇','乡','街道']
    lv527 = ['路','街']
    directly = ['北京','天津','上海','重庆']
    autonomous = ['宁夏回族','广西','内蒙古','新疆维吾尔族','西藏']
    
    json_info = {}
    address = []
    
    dic = d
    
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
    #print("block=",_block)
    s = clr(s,_block)
    for i in lv4:
        if s.find(i) >= 0:
            _block += i
            break;
    address.append(_block)
    s = solve(s,lv4)
    
    #get lv5 to lv7, in short is lv52(to)7
    #print(s)
    
    #print(json_info)
    return json_info, address, s


# In[27]:


def get_op(s, ss):
    pos = s.find(ss)
    ret1 = s[:pos]
    ret2 = s[pos+len(ss):]
    return ret1, ret2


# In[56]:


def _analysis_lv7(s):
    mks = ['路','街','巷','号']
    ret = []
    for i in mks:
        nw = ''.join(re.findall('.*'+i,s))
        if (nw!=''):
            ret.append(nw)
        s = s[s.find(nw)+len(nw):]
    if (s!=''):
        ret.append(s)
    return ret


# In[49]:


def address_analysis():
    dataset = open('./_lv4_canticle.json','rb')
    dic = json.load(dataset)
    
    s = input()
    s = s[:len(s)-1]
    _op, s = get_op(s, '!')
    _op = int(_op)
    if (_op!=3):
        _json_info, _addr, _res = _analysis_lv5(s, dic)
        if (_op==1):
            _addr.append(_res)
            _json_info['地址'] = _addr
        elif (_op==2):
            _more_detail = _analysis_lv7(_res)
            _addr = _addr + _more_detail
            _json_info['地址'] = _addr
    print(_json_info)


# In[70]:


address_analysis()


# In[ ]:




