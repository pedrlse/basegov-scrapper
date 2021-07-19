# imports
import time
import math
import requests


def checkServer(baseurl, load):  # verificar se o servidor esta a funcionar corretamente
    r = requests.get(baseurl)
    status = r.status_code
    if status == 200:
        return r
    else:
        while status != 200:
            print("Erro no servidor, o processo continuará após a resolução do erro - " +
                  str(math.trunc(load)) + "%")
            time.sleep(5)
            r = requests.get(baseurl)
            status = r.status_code
        else:
            print("O processo continuará...")
            return r
