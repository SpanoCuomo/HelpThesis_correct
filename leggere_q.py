<<<<<<< HEAD
import json

with open("UDA_da_pagina.txt", "r", encoding="utf-8") as file:
    target_page_url_list_FB_UDA_da_pagina = json.load(file)



=======
import json

with open("UDA_da_pagina.txt", "r", encoding="utf-8") as file:
    target_page_url_list_FB_UDA_da_pagina = json.load(file)



>>>>>>> 18bd82e (adesso codice più robusto. Devo ancora fare storie e reels dalla nuova pagina fcebook)
print(target_page_url_list_FB_UDA_da_pagina[0])