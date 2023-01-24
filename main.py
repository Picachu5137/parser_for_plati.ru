import requests
from bs4 import BeautifulSoup as bs
import lxml


def plati_req(request, gpp=10, n_page=1, is_available=True, response='xml', check_status=0, ):  # goods_per_page
    if not request:
        return "req is empty"
    else:
        URL_TEMPLATE = f"https://plati.io/api/search.ashx?query={request}\
                        &pagesize={gpp}&pagenum={n_page}\
                        &visibleOnly={is_available}&response={response}"  # req for plati.ru
        response = requests.get(URL_TEMPLATE)
        out = {}
        if check_status:
            #  print(response.text)
            print(response.url)
            print(response.status_code)

        soup = bs(response.text, "lxml")
        for item in soup.find_all("item"):
            item_id = item.get("id")
            name = item.find("name").get_text(), item.find("name_eng").get_text() # 0 = name_rus, 1 = name_eng
            price = tuple(map(float, (item.find("price_usd").get_text(), item.find("price_rur").get_text(),
                                      item.find("price_eur").get_text(), item.find("price_uah").get_text())))
            url = item.find("url").get_text()
            print(item_id)
            out[item_id] = {"name": name, "price": price, "url": url}
        return out


# TODO: read https://habr.com/ru/post/568334/
# TODO: make err return


if __name__ == "__main__":
    # req = input()
    req = "skyrim"
    p_req = plati_req(req, gpp=10, check_status=1)
    print(f"{p_req} \n {len(p_req)}")

"""
documentation https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html#id27 
pydocs https://docs-python.ru/packages/paket-beautifulsoup4-python/#example
"""
