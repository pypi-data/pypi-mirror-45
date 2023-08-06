#!/usr/bin/python
#!/usr/bin/python3
#!/usr/bin/env python
#!/usr/bin/env python3
# -*- coding: utf8 -*-

# Python Web Based English To Bangla Translator (Google, Bing, Yandex, Baidu).
# Author               :- Md Jabed Ali(jabed)
# Facebook             :- https://www.facebook.com/paradox.jabed
# Github               :- https://github.com/jabedparadox

import random
from json import loads
import requests
from bs4 import BeautifulSoup
import argparse
import re
#import aiohttp
#import asyncio
#import async_timeout
#from aiohttp import web
from json import loads
import json
import argparse
import os
import sys
import time
#from google.cloud import translate

#print("******************************** Md Jabed Ali(jabed) **********************************\n************************************ Translator ***************************************\n******** Example:- Translate to: Enter 1 for Afrikaans / Enter 2 for Albanian  ********\n\n1-Afrikaans~af   2-Albanian~sq       3-Amharic~am         4-Arabic~ar     5-Armenian~hy\n6-Azerbaijani~az 7-Basque~eu         8-Belarusian~be      9-Bengali~bn    10-Bosnian~bs\n11-Bulgarian~bg  12-Catalan~ca       13-Cebuano~ceb       14-Chichewa~ny  15-Chinese~zh-CN\n16-Corsican~co   17-Croatian~hr      18-Czech~cs          19-Danish~da    20-Dutch~nl\n21-English~en    22-Esperanto~eo     23-Estonian~et       24-Filipino~tl  25-Finnish~fi\n26-French~fr     27-Frisian~fy       28-Galician~gl       29-Georgian~ka  30-German~de\n31-Greek~el      32-Gujarati~gu      33-Haitian Creole~ht 34-Hausa~ha     35-Hawaiian~haw\n36-Hebrew~iw     37-Hindi~hi         38-Hmong~hmn         39-Hungarian~hu 40-Icelandic~is\n41-Igbo~ig       42-Indonesian~id    43-Irish~ga          44-Italian~it   45-Japanese~ja\n46-Javanese~jw   47-Kannada~kn       48-Kazakh~kk         49-Khmer~km     50-Korean~ko\n51-Kurdish~ku    52-Kyrgyz~ky        53-Lao~lo            54-Latin~la     55-Latvian~lv\n56-Lithuanian~lt 57-Luxembourgish~lb 58-Macedonian~mk     59-Malagasy~mg  60-Malay~ms\n61-Malayalam~ml  62-Maltese~mt       63-Maori~mi          64-Marathi~mr   65-Mongolian~mn\n66-Myanmar~my    67-Nepali~ne        68-Norwegian~no      69-Pashto~ps    70-Persian~fa\n71-Polish~pl     72-Portuguese~pt    73-Punjabi~pa        74-Romanian~ro  75-Russian~ru\n76-Samoan~sm     77-Scots Gaelic~gd  78-Serbian~sr        79-Sesotho~st   80-Shona~sn\n81-Sindhi~sd     82-Sinhala~si       83-Slovak~sk         84-Slovenian~sl 85-Somali~so\n86-Spanish~es    87-Sundanese~su     88-Swahili~sw        89-Swedish~sv   90-Tajik~tg\n91-Tamil~ta      92-Telugu~te        93-Thai~th           94-Turkish~tr   95-Ukrainian~uk\n96-Urdu~ur       97-Uzbek~uz         98-Vietnamese~vi     99-Welsh~cy     100-Xhosa~xh\n101-Yiddish~yi   102-Yoruba~yo       103-Zulu~zu\n\n*********************************** Translator **************************************\n")
#print("******************************** Md Jabed Ali(jabed) **********************************\n*************************** English To Bengali Translator *****************************\n") # Example:- Translate to: Enter 1 for Afrikaans / Enter 2 for Albanian  ********\n\n1-Afrikaans~af   2-Albanian~sq       3-Amharic~am         4-Arabic~ar     5-Armenian~hy\n6-Azerbaijani~az 7-Basque~eu         8-Belarusian~be      9-Bengali~bn    10-Bosnian~bs\n11-Bulgarian~bg  12-Catalan~ca       13-Cebuano~ceb       14-Chichewa~ny  15-Chinese~zh-CN\n16-Corsican~co   17-Croatian~hr      18-Czech~cs          19-Danish~da    20-Dutch~nl\n21-English~en    22-Esperanto~eo     23-Estonian~et       24-Filipino~tl  25-Finnish~fi\n26-French~fr     27-Frisian~fy       28-Galician~gl       29-Georgian~ka  30-German~de\n31-Greek~el      32-Gujarati~gu      33-Haitian Creole~ht 34-Hausa~ha     35-Hawaiian~haw\n36-Hebrew~iw     37-Hindi~hi         38-Hmong~hmn         39-Hungarian~hu 40-Icelandic~is\n41-Igbo~ig       42-Indonesian~id    43-Irish~ga          44-Italian~it   45-Japanese~ja\n46-Javanese~jw   47-Kannada~kn       48-Kazakh~kk         49-Khmer~km     50-Korean~ko\n51-Kurdish~ku    52-Kyrgyz~ky        53-Lao~lo            54-Latin~la     55-Latvian~lv\n56-Lithuanian~lt 57-Luxembourgish~lb 58-Macedonian~mk     59-Malagasy~mg  60-Malay~ms\n61-Malayalam~ml  62-Maltese~mt       63-Maori~mi          64-Marathi~mr   65-Mongolian~mn\n66-Myanmar~my    67-Nepali~ne        68-Norwegian~no      69-Pashto~ps    70-Persian~fa\n71-Polish~pl     72-Portuguese~pt    73-Punjabi~pa        74-Romanian~ro  75-Russian~ru\n76-Samoan~sm     77-Scots Gaelic~gd  78-Serbian~sr        79-Sesotho~st   80-Shona~sn\n81-Sindhi~sd     82-Sinhala~si       83-Slovak~sk         84-Slovenian~sl 85-Somali~so\n86-Spanish~es    87-Sundanese~su     88-Swahili~sw        89-Swedish~sv   90-Tajik~tg\n91-Tamil~ta      92-Telugu~te        93-Thai~th           94-Turkish~tr   95-Ukrainian~uk\n96-Urdu~ur       97-Uzbek~uz         98-Vietnamese~vi     99-Welsh~cy     100-Xhosa~xh\n101-Yiddish~yi   102-Yoruba~yo       103-Zulu~zu\n\n*********************************** Translator **************************************\n")

# Different headers.
def random_useragent():
    #http://useragentstring.com/pages/useragentstring.php
    url = "https://fake-useragent.herokuapp.com/browsers/0.1.8"
    r = requests.get(url)
    randomuseragent = loads(r.text)['browsers']
    #print(random.choice(randomuseragent[random.choice(list(randomuseragent))]))
    return random.choice(randomuseragent[random.choice(list(randomuseragent))])

u_a = random_useragent()
headers = {'User-Agent': u_a,
           #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
           #':authority': 'translate.google.com',
           #':scheme': 'https',
           'X-Requested-With': 'XMLHttpRequest',
           'Upgrade-Insecure-Requests': '1',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,application/json,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, br',
           #'Origin': ' ',
           #'Host': ' ',
}

# Possible spell error.
def pssible_error():
    url_pssible_error = 'https://api.languagetool.org/v2/check?instanceId=19644:1556175692778?disabledRules=WHITESPACE_RULE,FRENCH_WHITESPACE&allowIncompleteResults=true&enableHiddenRules=true&useragent=ltorg&text=Thre is so sorce&language=auto&altLanguages=en-US&textSessionId=19644:1556175692778'
    res_pssible_error = requests.get(url_pssible_error, headers=headers).text
    rslt_pssible_error = json.loads(res_pssible_error)
    rslt0_pssible_error = rslt_pssible_error['matches']
    rslt1_pssible_error = [str(re.findall('{\'value\': \'(.*?)\'', str(i['replacements']), re.DOTALL)).replace('\'', '') for i in rslt0_pssible_error]
    return rslt1_pssible_error

# With aiohttp.
async def get_session(session, url):
    with async_timeout.timeout(5):
        async with session.get(url) as response:
            return await response.text()

# With aiohttp.
'''async def init_get():
    app = web.Application()
    app.router.add_route('GET', '/{name}', handle)
    return await loop.create_server(
        app._make_handler(), '127.0.0.1', 8080)'''

# With aiohttp.
#url =['', '']
async def get_main():
    async with aiohttp.ClientSession() as session:
        resp = await get_session(session, 'https://www.-.com')
        return web.Response(text=resp)
        #session.close()

# Which lang.
def translateto():
     while True:
          trnslt_to = input("Translate to: ")
          if trnslt_to.isdigit():
               return trnslt_to
               break
          else:
               print ("Enter a digit.")

# Translating frm baidu.
#def baidu_translate():
     #trnslt_to = input("Translate to: ")

# Multiple item extend.
def mltipl(lst, *elmnt):
    lst.extend(elmnt)

# Translating frm bing.
def bing_translate(frm_bing, to_bing):
    trnslt_to = translateto()
    bing_param = {'text': '',
              'from': 'en',
              'to': 'bn'
    }
    bing_param_detect = {'text': ''}
    url_bing = 'https://www.bing.com/ttranslate?&category=&IG=D458B762C9184506AF3108AE1F0CDA26&IID=translator.5036.3'
    url_bing_detect = requests.post('https://www.bing.com/tdetect?&IG=103CA78C8D314209BCF33D5EC2D6FC56&IID=translator.5036.1', data=bing_param_detect, headers=headers).text
    res_bing = requests.post(url_bing, data=bing_param, headers=headers).text
    return res_bing

# English to Bengali.
def en_bn(word_en=None):
        url0_en_bn = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=bn&dt=t&q=' + word_en.title()
        res0_en_bn = requests.get(url0_en_bn, headers=headers).text
        yandex_param = {'text': word_en.title(),
                        'from': '4'
                        }
        url_yandex = 'https://translate.yandex.net/api/v1/tr.json/translate?id=6d3ae0b0.5cbf4919.6cddeec8-4-0&srv=tr-text&lang=en-bn&reason=auto'
        res_yandex = requests.post(url_yandex, data=yandex_param, headers=headers).text
        try:
            #bing_param_detect = {'text': word_en}
            #url_bing_detect = requests.post('https://www.bing.com/tdetect?&IG=103CA78C8D314209BCF33D5EC2D6FC56&IID=translator.5036.1', data=bing_param_detect, headers=headers, timeout=3).text
            bing_param = {'text': word_en.title(),
                          'from': 'en',
                          #'to': tl.split('~')[-1]
                          'to': 'bn'
                          }
            url_bing = 'https://www.bing.com/ttranslate?&category=&IG=D458B762C9184506AF3108AE1F0CDA26&IID=translator.5036.3'
            res_bing = requests.post(url_bing, data=bing_param, headers=headers, timeout=3).text
        except (IndexError, ValueError):
            res_bing = "na"
        try:
            rslt_bing = re.findall('"(.*?)"', str(res_bing), re.DOTALL)[-1]
        except (IndexError, ValueError):
            rslt_bing = 'Null'
        try:
            rslt_yandex = re.findall('"(.*?)"', str(res_yandex), re.DOTALL)[-1]
        except (IndexError, ValueError):
            rslt_yandex = 'Null'     
        try:
            rslt_en_bn = re.findall('"(.*?)"', str(res0_en_bn), re.DOTALL)[0]
        except (IndexError, ValueError):
            rslt_en_bn = 'Null'
        rslt_final = []
        #rslt_final.append(str(rslt_en_bn+rslt_yandex+rslt_bing))
        #mltipl(rslt_en_bn, rslt_yandex, rslt_bing)
        rslt_final = rslt_en_bn + ', ' + rslt_yandex + ', ' + rslt_bing
        return rslt_final
            
# Bengali to English.
def bn_en(word_bn=None):
    while True:
        url0_bn_en = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q=' + word_bn.title()
        res0_bn_en = requests.get(url0_bn_en, headers=headers).text
        yandex_param = {'text': word_bn.title(),
                        'from': '4'
                        }
        url_yandex = 'https://translate.yandex.net/api/v1/tr.json/translate?id=6d3ae0b0.5cbf4919.6cddeec8-4-0&srv=tr-text&lang=bn-en&reason=auto'
        res_yandex = requests.post(url_yandex, data=yandex_param, headers=headers).text
        try:
            #bing_param_detect = {'text': word_en}
            #url_bing_detect = requests.post('https://www.bing.com/tdetect?&IG=103CA78C8D314209BCF33D5EC2D6FC56&IID=translator.5036.1', data=bing_param_detect, headers=headers, timeout=3).text
            bing_param = {'text': word_bn.title(),
                          'from': 'bn',
                          #'to': tl.split('~')[-1]
                          'to': 'en'
                          }
            url_bing = 'https://www.bing.com/ttranslate?&category=&IG=D458B762C9184506AF3108AE1F0CDA26&IID=translator.5036.3'
            res_bing = requests.post(url_bing, data=bing_param, headers=headers, timeout=3).text
        except (IndexError, ValueError):
            res_bing = "na"
        try:
            rslt_bing = re.findall('"(.*?)"', str(res_bing), re.DOTALL)[-1]
        except (IndexError, ValueError):
            rslt_bing = 'Null'
        try:
            rslt_yandex = re.findall('"(.*?)"', str(res_yandex), re.DOTALL)[-1]
        except (IndexError, ValueError):
            rslt_yandex = 'Null'     
        try:
            rslt_en_bn = re.findall('"(.*?)"', str(res0_bn_en), re.DOTALL)[0]
        except (IndexError, ValueError):
            rslt_en_bn = 'Null'
        rslt_final = []
        #rslt_final.append(str(rslt_en_bn+rslt_yandex+rslt_bing))
        #mltipl(rslt_en_bn, rslt_yandex, rslt_bing)
        rslt_final = rslt_en_bn + ', ' + rslt_yandex + ', ' + rslt_bing
        return rslt_final        

# Translating frm googel.
def translate_bengali(inputtext=None):
     while True:
          #trnslt_to = translateto()
          #trnslt_to = input("Translate to: ")
          '''if trnslt_to == '1':
               tl = 'Afrikaans~af'
          elif trnslt_to == '2':
               tl = 'Albanian~sq'
          elif trnslt_to == '3':
               tl = 'Amharic~am'
          elif trnslt_to == '4':
               tl = 'Arabic~ar'
          elif trnslt_to == '5':
               tl = 'Armenian~hy'
          elif trnslt_to == '6':
               tl = 'Azerbaijani~az'
          elif trnslt_to == '7':
               tl = 'Basque~eu'
          elif trnslt_to == '8':
               tl = 'Belarusian~be'
          elif trnslt_to == '9':
               tl = 'Bengali~bn'
          elif trnslt_to == '10':
               tl = 'Bosnian~bs'         
          elif trnslt_to == '21':
               tl = 'en'
               '''
          while True:
              if inputtext==None:
                  inputtext = input("Enter Text: ").title()
              url = 'https://api.languagetool.org/v2/check?instanceId=19644:1556175692778?disabledRules=WHITESPACE_RULE,FRENCH_WHITESPACE&allowIncompleteResults=true&enableHiddenRules=true&useragent=ltorg&text=' + inputtext + '&language=auto&altLanguages=en-US&textSessionId=19644:1556175692778'
              res_pssible_error = requests.get(url, headers=headers).text
              rslt_pssible_error = json.loads(res_pssible_error)
              if 'misspelling' in str(rslt_pssible_error):
                  #print(json.dumps(rslt_pssible_error, indent = 4, sort_keys=True))
                  rslt0_pssible_error = rslt_pssible_error['matches']
                  rslt1_pssible_error = [str(re.findall('{\'value\': \'(.*?)\'', str(i['replacements']), re.DOTALL)).replace('\'', '') for i in rslt0_pssible_error]
                  print ('Possible spelling mistake. Correction :' + str(rslt1_pssible_error))
              else:
                  break

          # Bing.
          try:
              bing_param_detect = {'text': inputtext}
              url_bing_detect = requests.post('https://www.bing.com/tdetect?&IG=103CA78C8D314209BCF33D5EC2D6FC56&IID=translator.5036.1', data=bing_param_detect, headers=headers, timeout=3).text
              bing_param = {'text': inputtext,
                            'from': url_bing_detect,
                            #'to': tl.split('~')[-1]
                            'to': 'bn'
                            }
              url_bing = 'https://www.bing.com/ttranslate?&category=&IG=D458B762C9184506AF3108AE1F0CDA26&IID=translator.5036.3'
              res_bing = requests.post(url_bing, data=bing_param, headers=headers, timeout=3).text
          except:
              res_bing = "na"
          try:
              rslt_bing = '\n' +  "From Bing    : " +  inputtext + ' <-> ' + re.findall('"(.*?)"', str(res_bing), re.DOTALL)[-1]
          except (IndexError, ValueError):
              rslt_bing = "From Bing    : " + 'Null'
              
          # Yandex. 
          yandex_param = {'text': inputtext,
                          'from': '4'
                          }
          url_yandex = 'https://translate.yandex.net/api/v1/tr.json/translate?id=6d3ae0b0.5cbf4919.6cddeec8-4-0&srv=tr-text&lang=en-bn&reason=auto'
          res_yandex = requests.post(url_yandex, data=yandex_param, headers=headers).text
          try:
              rslt_yandex = "From Yandex  : " +  inputtext + ' <-> ' + re.findall('"(.*?)"', str(res_yandex), re.DOTALL)[-1]
          except (IndexError, ValueError):
              rslt_yandex = "From Yandex  : " + 'Null'          
          
          # Google.
          url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=bn&dt=t&q=' + inputtext
          res = requests.get(url, headers=headers).text
          #print ("Translating to " + tl.split('~')[0] + " .....")
          #print ("Translating To Bengali .....")
          try:
              rslt_google = "From Google  : " +  inputtext + ' <-> ' + re.findall('"(.*?)"', str(res), re.DOTALL)[0]
          except (IndexError, ValueError):
              rslt_google = "From Google  : " + 'Null'
              
          # Baidu.
          #url_baidu  = 'https://api.fanyi.baidu.com'
          rslt_baidu = "From Baidu   : " + 'Null'
          
          #print ('\n' + "From Googel: " +  inputtext + ' <-> ' + re.findall('"(.*?)"', str(res), re.DOTALL)[0] + '\n' + "From Bing  : " +  inputtext + ' <-> ' + re.findall('"(.*?)"', str(res_bing), re.DOTALL)[-1] + '\n'  + "From Yandex: " +  inputtext + ' <-> ' + re.findall('"(.*?)"', str(res_yandex), re.DOTALL)[-1] + '\n')
          #print (rslt_bing +  '\n' + rslt_yandex + '\n' + rslt_google + '\n' + rslt_baidu + '\n')
          rslt_final = rslt_bing +  '\n' + rslt_yandex + '\n' + rslt_google + '\n' + rslt_baidu + '\n'
          return rslt_final
          #if inputtext!==None:
              
          agn = input("Want to translate again? (Y/N): ")
          if agn == 'Y':
              pass
          else:
              sys.exit()

#if __name__ == '__main__':
     #googel_translate()


'''print("1-Afrikaans~af   2-Albanian~sq       3-Amharic~am         4-Arabic~ar     5-Armenian~hy
         6-Azerbaijani~az 7-Basque~eu         8-Belarusian~be      9-Bengali~bn    10-Bosnian~bs
         11-Bulgarian~bg  12-Catalan~ca       13-Cebuano~ceb       14-Chichewa~ny  15-Chinese~zh-CN
         16-Corsican~co   17-Croatian~hr      18-Czech~cs          19-Danish~da    20-Dutch~nl
         21-English~en    22-Esperanto~eo     23-Estonian~et       24-Filipino~tl  25-Finnish~fi
         26-French~fr     27-Frisian~fy       28-Galician~gl       29-Georgian~ka  30-German~de
         31-Greek~el      32-Gujarati~gu      33-Haitian Creole~ht 34-Hausa~ha     35-Hawaiian~haw
         36-Hebrew~iw     37-Hindi~hi         38-Hmong~hmn         39-Hungarian~hu 40-Icelandic~is
         41-Igbo~ig       42-Indonesian~id    43-Irish~ga          44-Italian~it   45-Japanese~ja
         46-Javanese~jw   47-Kannada~kn       48-Kazakh~kk         49-Khmer~km     50-Korean~ko
         51-Kurdish~ku    52-Kyrgyz~ky        53-Lao~lo            54-Latin~la     55-Latvian~lv
         56-Lithuanian~lt 57-Luxembourgish~lb 58-Macedonian~mk     59-Malagasy~mg  60-Malay~ms
         61-Malayalam~ml  62-Maltese~mt       63-Maori~mi          64-Marathi~mr   65-Mongolian~mn
         66-Myanmar~my    67-Nepali~ne        68-Norwegian~no      69-Pashto~ps    70-Persian~fa
         71-Polish~pl     72-Portuguese~pt    73-Punjabi~pa        74-Romanian~ro  75-Russian~ru
         76-Samoan~sm     77-Scots Gaelic~gd  78-Serbian~sr        79-Sesotho~st   80-Shona~sn
         81-Sindhi~sd     82-Sinhala~si       83-Slovak~sk         84-Slovenian~sl 85-Somali~so
         86-Spanish~es    87-Sundanese~su     88-Swahili~sw        89-Swedish~sv   90-Tajik~tg
         91-Tamil~ta      92-Telugu~te        93-Thai~th           94-Turkish~tr   95-Ukrainian~uk
         96-Urdu~ur       97-Uzbek~uz         98-Vietnamese~vi     99-Welsh~cy     100-Xhosa~xh
         101-Yiddish~yi   102-Yoruba~yo       103-Zulu~zu")'''
