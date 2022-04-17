from datetime import date, datetime, timedelta

month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

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

def fonurl(html):
    with sync_playwright() as p:
        news = News()
        news.url = html 
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        html = html + "print.html"
        page.goto(html, timeout = 0)
        page_title = page.locator("xpath=//h1").text_content(timeout = 0)
        news.title = page_title

        page_text = page.locator("xpath=//div/p")
        text_count = page_text.count()
        for i in range(1, text_count):
            news.text += page_text.nth(i).text_content(timeout = 0) + " "

        news.autor.append("Нет автора")

        page_img = page.locator("xpath=//img")
        img_count = page_img.count()
        for i in range(1, img_count - 1):
            scr = page_img.nth(i).get_attribute("src", timeout = 0)
            news.img.append(scr)

        page_url = page.locator("xpath=//p/a")
        url_count = page_url.count()
        for i in range(url_count):
            check_url = page_url.nth(i).get_attribute("href", timeout = 0)
            if len(check_url) > 1 and check_url[0] == '/':
                check_url = "https://www.fontanka.ru" + check_url
                news.urls.append(check_url)
        
        page_data = page.locator("xpath=//article/div/div[1]/div[2]/span").text_content()
        page_data = page_data.split(",")[0].split(" ")
        data = date(int(page_data[2]), month_list.index(page_data[1]) + 1, int(page_data[0]))
        news.dateday = data.strftime('%Y-%m-%d')

        page_tag = page.locator("xpath=//a/h4")
        tag_count = page_tag.count()
        for i in range(tag_count):
            tag = page_tag.nth(i).text_content()
            news.tags.append(tag)

        browser.close()
        return news

def foncrow(data_begin, data_end):
    with sync_playwright() as p:
        begin = date.fromisoformat(data_begin)
        end = date.fromisoformat(data_end) 
        end += timedelta(days=1)
        urlv = list()

        browser = p.firefox.launch(headless=False)

        while(begin != end):
            page = browser.new_page()
            url = "https://www.fontanka.ru/" + begin.strftime("%Y/%m/%d") + "/news.html"
            page.goto(url, wait_until = "domcontentloaded")

            urls = page.locator("xpath=//li/div[2]/div/a[1]")
            count_urls = urls.count()
            for i in range(count_urls):
                href = urls.nth(i).get_attribute("href")
                if href[0] == '/':
                    urlv.append("https://www.fontanka.ru" + href)

            begin += timedelta(days=1)
            page.close()
        browser.close()
        return urlv