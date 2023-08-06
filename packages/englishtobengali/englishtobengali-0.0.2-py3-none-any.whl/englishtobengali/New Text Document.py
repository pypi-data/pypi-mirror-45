import entobn
#a = entobn.googel_translate('do')

translet = entobn.translate_bengali('What are you doing now?') # Translate To Bengali From Google, Bing, Yandex, Baidu.
tobangla = entobn.en_bn('What are you doing now?') # Translate To Bengali From English.
toenglish = entobn.bn_en('তুমি এখন কি করছো?') # Translate To English From Bengali.
print (tobangla)
