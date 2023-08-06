from bs4 import BeautifulSoup
import requests
from .HtmlParser import SearchOptionParser, ProductListParser, ProductParser
import threading
import time
import pandas as pd
class StructuredProductCrawler:
    headers = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
            }
    def __init__(self, verbose = False):
        self.verbose = verbose
        self.df_headers = [
            'URL',
            'UID',
            'NAME',
            'CURRENCY',
            'MATURITY',
            'UNDERLYING',
            'PRINCIPAL_PROTECTION',
            'PI',
            'ISSUE_DATE',
            'ISSUER',
            'MASTER_AGENT',
            'DISTRIBUTOR']
        self.index_url = "https://structurednotes-announce.tdcc.com.tw/Snoteanc/apps/bas/BAS210.jsp"
        self.product_url = "https://structurednotes-announce.tdcc.com.tw{product_partial_url}"
        self.max_pages = {}
        self.products = []
        self.products_df = None
        self.queries = [
            "AGENT_CODE={agent}",
            "ISSUE_ORG_UUID=",
            "SALE_ORG_UUID=",
            "FUND_LINK_TYPE=",
            "FUND_CURR=",
            "FUND_TYPE=",
            "FUND_STOP_DATE=",
            "agentDateStart=",
            "agentDateEnd=",
            "action=Q",
            "LAST_ORDER_BY=FUND_NAME",
            "ORDER_BY=",
            "IS_ASC=",
            "currentPage={page_number}"
        ]
        self.base_query_url = self.index_url + "?" + "&".join(self.queries)

    def _get_master_agents(self):
        response = requests.get(self.index_url, headers=self.headers)
        parser = SearchOptionParser(response)
        return parser.get_master_agents()

    def _get_max_page(self, url, agent):
        response = requests.get(url,headers=self.headers)
        max_page_number = ProductListParser(response).get_max_list_page()
        self.max_pages[agent]=max_page_number

    def _get_max_pages_for_all_master_agents(self):
        master_agents = self._get_master_agents()
        agents = list(master_agents.keys())
        threads = []
        for agent in agents:
            print("getting max page of {}".format(master_agents[agent]))
            first_page_url = self.base_query_url.format(agent=agent, page_number =1)
            thread = threading.Thread(target = self._get_max_page, args=(first_page_url, agent,))
            thread.start()
            time.sleep(0.5)
            threads.append(thread)
        for thread in threads:
            thread.join()
        return self.max_pages

    def _get_all_page_urls(self):
        max_pages = self._get_max_pages_for_all_master_agents()
        urls = []
        for agent, max_page in max_pages.items():
            agent_urls = [self.base_query_url.format(agent=agent, page_number =x) for x in range(1,max_page+1)]
            urls += agent_urls
        return urls

    def _get_product_list(self, url):
        response = requests.get(url, headers=self.headers)
        parser = ProductListParser(response)
        product_list = parser.get_product_list()
        self.products += product_list

    def _fill_in_distributor_info(self, product_partial_url):
        url = self.product_url.format(product_partial_url = product_partial_url)
        response = requests.get(url, headers=self.headers)
        parser = ProductParser(response)
        distributors = parser.get_product_distributors()
        self.products.loc[self.products["URL"]==product_partial_url,["DISTRIBUTOR"]] = ",".join(distributors)

    def _crawl_missing_distributor(self):
        threads = []
        products_missing_distributor = self.products[self.products["DISTRIBUTOR"].isin(["Y","N"])]
        for index, product_partial_url in enumerate(products_missing_distributor["URL"].tolist()):
            thread = threading.Thread(target = self._fill_in_distributor_info, args=(product_partial_url,))
            thread.start()
            threads.append(thread)
            time.sleep(0.5)
        for thread in threads:
            thread.join()

    def crawl(self):
        threads =[]
        page_urls = self._get_all_page_urls()

        for index, url in enumerate(page_urls):
            print("crawling {} of {} pages".format(index+1,len(page_urls)))
            thread = threading.Thread(target = self._get_product_list, args=(url,))
            thread.start()
            time.sleep(0.5)
            threads.append(thread)
            if index%20==0:
                time.sleep(1)
        for thread in threads:
            thread.join()
        self.products = pd.DataFrame(self.products, columns=self.df_headers)
        self._crawl_missing_distributor()
        return self.products
