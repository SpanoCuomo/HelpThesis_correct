import json

with open("UDA_da_pagina.txt", "r", encoding="utf-8") as file:
    target_page_url_list_FB_UDA_da_pagina = json.load(file)



print(target_page_url_list_FB_UDA_da_pagina[0])