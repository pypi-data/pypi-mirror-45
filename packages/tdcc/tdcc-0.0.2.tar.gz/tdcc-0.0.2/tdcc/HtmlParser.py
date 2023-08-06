from bs4 import BeautifulSoup

class HtmlParser:
    def __init__(self, response):
        self._response = response
        assert response.status_code == 200
        html = self._response.text
        self._parser = BeautifulSoup(html, 'html5lib')

class SearchOptionParser(HtmlParser):
    def __init__(self, response):
        super().__init__(response)
    def _get_options(self, id):
        options = self._parser.select("#{} option".format(id))
        return {option.get("value"):option.text for option in options if option.get('value')!=''}
    def get_master_agents(self):
        id = "agent"
        return self._get_options(id)
    def get_distributors(self):
        id = "saleOrg"
        return self._get_options(id)


class ProductListParser(HtmlParser):
    def __init__(self, response):
        super().__init__(response)
    def get_max_list_page(self):
        """
        The max page number is hidden in the attribute of the img:
        <img src="/Snoteanc/images/lp.gif" style="border:none" onclick="setPage('30')">
        """
        last_page_button = self._parser.find("img", {"src" : "/Snoteanc/images/lp.gif"})
        if last_page_button:
            max_page = last_page_button.get("onclick").split("'")[1]
        else:
            max_page = 1
        return int(max_page)

    def get_product_list(self):
        """
        Returns:
        list: a list of lists of product information[n=11].
        """
        last_table = self._parser.select("table")[2]
        table_rows = last_table.select("tr")
        df_rows = []
        for row in table_rows:
            df_row = []
            tds = row.select("td")
            if len(tds)!=11:
                continue
            df_row.append(tds[0].get("onclick").split("'")[1])
            for td in tds:
                df_row.append(td.text.replace("\n","").replace("\t","").replace("\r","").replace("\xa0","").replace("&nbsp;","").strip())
            df_rows.append(df_row)
        return df_rows

class ProductParser(HtmlParser):
    def __init__(self, response):
        super().__init__(response)
    def get_product_distributors(self):
        distributors = []
        distributor_rows = self._parser.find("span",{"id":"div2"}).select("tr td table")[-1].findAll("tr")[2:]
        for row in distributor_rows:
            distributor = row.findAll("td")[1].text.replace("\n","").replace("\t","").replace("\r","").replace("\xa0","").replace("&nbsp;","").strip()
            distributors.append(distributor)
        return distributors
