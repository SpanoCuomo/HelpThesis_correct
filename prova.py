import json

def TXT_2_list(nomefile):
    with open(nomefile, "r", encoding="utf-8") as file:
            urls = json.load(file)

    ListaDaUsare = list(dict.fromkeys(urls))
    print(ListaDaUsare[0])
    return ListaDaUsare
    
        
TXT_2_list("UDA_da_pagina.txt")