from datetime import date, timedelta
from time import sleep
from playwright.sync_api import sync_playwright
class News:
    def __init__(self):
        self.url = ""
        self.title = ""
        self.text = ""
        self.autor = []
        self.img = []
        self.urls = []
        self.dateday = ""
        self.tags = []

def aifurl(html):
    with sync_playwright() as p:
        news = News()
        news.url = html
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(html, timeout = 0)

        page_title = page.locator("xpath=//h1").text_content(timeout = 0)
        news.title = page_title

        page_text = page.locator("div.article_text > p")
        text_count = page_text.count()
        for i in range(text_count):
            news.text += page_text.nth(i).inner_text() + " "
    
        page_autor = page.locator("div.autor")
        autor_count = page_autor.count()
        for i in range(autor_count):
            news.autor.append(page_autor.nth(i).text_content().replace(',', ""))
        if autor_count == 0:
            news.autor.append("Нет автора")

        main_img = page.locator("div.img_box > a > img")
        page_img = page.locator("xpath=//figure/div/img")
        main_img_count = main_img.count()
        img_count = page_img.count()
        for i in range(main_img_count):
            news.img.append(main_img.nth(i).get_attribute("src"))
        for i in range(img_count):
            scr = page_img.nth(i).get_attribute("src")
            news.img.append(scr)

        main_url = page.locator("xpath=//figure/div/div/a")
        page_url = page.locator("xpath=//p/a")
        main_url_count = main_url.count()
        url_count = page_url.count()
        for i in range(main_url_count):
            check_url = main_url.nth(i).get_attribute("href")
            if check_url.find("nn.aif.ru") != -1:
                news.urls.append(check_url)
        for i in range(url_count):
            check_url = page_url.nth(i).get_attribute("href")
            if check_url.find("nn.aif.ru") != -1:
                news.urls.append(check_url)

        page_data = page.locator("div.date > time").nth(0).text_content()
        page_data = page_data.split(" ")[0].split(".")
        data = date(int(page_data[2]), int(page_data[1]), int(page_data[0]))
        news.dateday = data.strftime('%Y-%m-%d')
        
        page_tag = page.locator("div.tags > a")
        tag_count = page_tag.count()
        for i in range(tag_count):
            news.tags.append(page_tag.nth(i).text_content())
        browser.close()
        return news

def aifcrow(data_begin, data_end):
    with sync_playwright() as p:
        begin = date.fromisoformat(data_begin)
        end = date.fromisoformat(data_end) 
        end += timedelta(days=1)
        urlv = list()
        browser = p.firefox.launch(headless=False)

        while(begin != end):
            page = browser.new_page()
            data_now = begin.strftime("%Y-%m-%d")
            url = ("https://nn.aif.ru/search?text=&content_type=2&rubric_id=0&from=" + data_now
            + "&to=" + data_now)
            page.goto(url, wait_until = "domcontentloaded", timeout = 0)

            more = page.locator("a.load_more") 
            if more.count():
                while more.get_attribute("style") != "display: none;":
                    more.click()
                    while page.locator("div.spinner").get_attribute("style") == "display: block;":
                        sleep(1)

            urls = page.locator("div.text_box a")
            count_urls = urls.count()
            for i in range(count_urls):
                href = urls.nth(i).get_attribute("href")
                urlv.append(href)

            begin += timedelta(days=1)
            page.close()
        browser.close()
        return urlv
aifurl("https://nn.aif.ru/sport/nizhegorodcy_privezli_na_rodinu_dva_chempionskih_poyasa")