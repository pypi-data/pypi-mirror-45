import entobn
#a = entobn.googel_translate('do')

translet = entobn.translate_bengali('How are you?') # Translate To Bengali From Google, Bing, Yandex, Baidu.
tobangla = entobn.en_bn('How are you?') # Translate To Bengali From English.
toenglish = entobn.bn_en('তুমি কেমন আছো?') # Translate To English From Bengali.
print (translet)
