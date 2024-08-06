import time
import requests
import os
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright
from colorama import Fore, init

init(convert=True)
red = Fore.RED
green = Fore.GREEN
cyan = Fore.CYAN
lb = Fore.LIGHTBLUE_EX
lc = Fore.LIGHTCYAN_EX
white = Fore.WHITE

class LOCALTONET:

    def __init__(self, email, password, api_key) -> None:
        self.email = email
        self.password = password
        self.api = api_key
        self.authTokUrl = 'https://localtonet.com/api/GetAuthTokens'
        self.TcpUdpCreationUrl = 'https://localtonet.com/tunnel/createtcpudp'
        self.loginUrl = 'https://localtonet.com/Identity/Account/Login'
        self.LOCALPATH = os.getcwd()
        self.headers = {
                    'accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                }
        
        self.token = self.GetAuthToken()
        self.verifyToken = self.GetVerifyToken()

    def launchAppThread(self, auth):
        appPath = os.path.join(self.LOCALPATH, 'localClient')
        os.chdir(appPath)
        start_command = f'start localclient.exe authtoken {auth}'
        subprocess.check_output(start_command, shell=True)
        return True
    
    def killProcess(self):
        res = subprocess.check_call('taskkill /IM "localclient.exe" /F')
        return res
        
    def CreateTcpUdpTunnel(self, port: str):
        current_path = os.getcwd()
        browserPath = Path(os.path.join(current_path, 'chromewin', 'chrome.exe'))
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=browserPath.absolute(), headless=True, slow_mo=50)
            context = browser.new_context()
            page = context.new_page()
            print('🔃 Please Wait...')
            while True:
                time.sleep(1)
                try:
                    page.goto(self.loginUrl, wait_until='load')
                    break
                except:
                    continue
            time.sleep(1)
            os.system('cls')
            print(f'\n{green}🔃 {cyan}Trying Logging in')
            page.fill('#Input_Email', self.email)
            page.fill('#Input_Password', self.password)
            time.sleep(1)
            page.click('#kt_sign_up_submit')
            time.sleep(2)
            os.system('cls')
            print(f'\n{green}[🗸] {cyan}Logged in')
            while True:
                time.sleep(1)
                os.system('cls')
                print('🔃 Please Wait...')
                try:
                    page.goto('https://localtonet.com/tunnel/tcpudp')
                    break
                except Exception as e:
                    print(e)
                    continue
            time.sleep(1)
            os.system('cls')
            try:
                page.get_by_role('button', name='Delete').click()
                time.sleep(1)
                page.get_by_role('button', name='Yes').click()
                print(f'\n{green}[🗸] {cyan}Old Tunnel Has Been Deleted To Create A New One.')
            except:
                pass
            time.sleep(2)
            os.system('cls')
            print(f'\n{green}🔃 Creating {cyan}TCP/UDP {green}Tunnel')
            page.click('#createTcpUdpForm > div.row.col-lg-9 > div:nth-child(1) > div > span > span.selection > span')
            time.sleep(1)
            page.fill('#kt_body > span.select2-container.select2-container--bootstrap5.select2-container--open > span > span.select2-search.select2-search--dropdown > input', 'tcp')
            time.sleep(1)
            page.keyboard.press('Enter')
            time.sleep(1)
            page.click('#createTcpUdpForm > div.row.col-lg-9 > div:nth-child(3) > div > span > span.selection > span')
            time.sleep(1)
            page.fill('#kt_body > span.select2-container.select2-container--bootstrap5.select2-container--open > span > span.select2-search.select2-search--dropdown > input', 'de')
            time.sleep(1)
            page.keyboard.press('Enter')
            time.sleep(1)
            page.fill('#createTcpUdpForm > div:nth-child(2) > div:nth-child(2) > div > input', port)
            time.sleep(1)
            page.click('#createTcpUdpForm > div:nth-child(2) > div:nth-child(5) > button')
            time.sleep(5)
            identity = None
            html = page.content()
            soup = bs(html, 'lxml')
            tr = soup.find('tr', class_='odd')
            tunnel_id = tr.attrs['id']
            tds = soup.find_all('td', class_='dt-center')
            for td in tds:
                try:
                    server_id = str(td.span.getText()).strip()
                    break
                except Exception as e:
                    continue
            for cookie in context.cookies():
                if cookie['name'] == '.AspNetCore.Identity.Application':
                    identity = cookie['value']
        return {'ID': tunnel_id, 'Server': server_id, 'Identity': identity }

    def startTunnel(self, id: str, identity: str):
        os.system('cls')
        print(f'\n{green}🔃 Starting {cyan}TCP/UDP {green}Tunnel')
        headers = {
            'cookie': f'.AspNetCore.Identity.Application={identity}'
        }

        res = requests.post('https://localtonet.com/tunnel/relayprocess', data={'id': f'{id}'}, headers=headers)
        json_res = res.json()
        os.system('cls')
        if json_res['data']['isSuccess'] == True:
            tunnel_req = requests.get('https://localtonet.com/tunnel/getusertcpudp?maxResultCount=10&skipCount=1&type=&token=&search=', headers=headers)
            json_response = tunnel_req.json()
            print(f'{cyan}[🗸] {green}Tunneling Has Been Started')
            return json_response['result'][0]['serverPort']
        else:
            print(f'{red}[x] Failed To Start The Tunnel.')
            time.sleep(3)
            return False

    def GetAuthToken(self):
        """
        
        Returns The Auth Token Of Localtonet Account Using API Key

        """
        s = requests.Session()

        response = s.get(self.authTokUrl, headers=self.headers)

        return response.json().get('result')[0].get('token')
    

    def GetVerifyToken(self):

        with requests.Session() as s:

            html = s.get('https://localtonet.com/tunnel/tcpudp')

            soup = bs(html.text, "lxml")

            verifyTok = soup.find(name='input', attrs=({'name': '__RequestVerificationToken'}))
            if verifyTok:
                return verifyTok.attrs['value']
            else:
                return 'Unable To Locate Verify Request Token'
