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

month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 
'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

def belurl(html):
    with sync_playwright() as p:
        news = News()
        news.url = html
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto(html, timeout = 0)

        page_title = page.locator("xpath=//h1").text_content(timeout = 0)
        news.title = page_title

        page_text = page.locator("xpath=//p")
        text_count = page_text.count()
        for i in range(text_count - 3):
            news.text += page_text.nth(i).inner_text() + " "
    

        autor = page_text.nth(text_count - 3).inner_text()
        if autor.find('.') != -1:
            news.text += autor
            autor = "Нет автора"
        news.autor.append(autor)

        page_img = page.locator("xpath=//img")
        img_count = page_img.count()
        for i in range(2, img_count - 5):
            scr = page_img.nth(i).get_attribute("src")
            if scr.find("2_upscale") != -1:
                scr = "https://www.belpressa.ru" + scr
                news.img.append(scr)
    
        page_url = page.locator("xpath=//p/a")
        url_count = page_url.count()
        maxt = 0
        for i in range(url_count):
            check_url = page_url.nth(i).get_attribute("href")
            if check_url.find("belpressa") != -1:
                news.urls.append(check_url)
        
        page_data = page.locator("span.date_time:nth-child(1)").text_content()
        page_data = page_data.split(",")[0].split()
        data = date(int(page_data[2]), month_list.index(page_data[1]) + 1, int(page_data[0]))
        news.dateday = data.strftime('%Y-%m-%d')

        page_tag = page.locator(".breadcrumbs > ul:nth-child(1) > li:nth-child(2) > a:nth-child(1)")
        news.tags.append(page_tag.text_content())

        browser.close()
        return news

def belcrow(data_begin, data_end):
    with sync_playwright() as p:
        begin = date.fromisoformat(data_begin)
        end = date.fromisoformat(data_end) + timedelta(days=1)
        urlv = list()

        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.belpressa.ru/type/news/", wait_until = "domcontentloaded")
        page.locator("li.ex-and:nth-child(6) > span:nth-child(1)").click()
        page.locator("li.ex-and:nth-child(7) > span:nth-child(1)").click()
        page.locator("li.ex-and:nth-child(8) > span:nth-child(1)").click()

        while(begin != end):
            page.locator("li.ex-xor:nth-child(" + str(2022 - begin.year + 2) + ") > span").click()
            string = "li.ex-and:nth-child(7) > ul:nth-child(2) > li:nth-child(" + str(begin.month) + ") > span"
            page.locator(string).click()

            if (begin.day > 0 and begin.day < 11):
                page.locator("li.ex-and:nth-child(8) > ul:nth-child(2) > li:nth-child(1) > span").click()
                string = ("li.ex-and:nth-child(8) > ul:nth-child(3) > li:nth-child(1)> ul:nth-child(2) > li:nth-child("
                + str(begin.day) +") > span")
                page.locator(string).click()

            if (begin.day > 10 and begin.day < 21):
                page.locator("li.ex-and:nth-child(8) > ul:nth-child(2) > li:nth-child(2) > span").click()
                string = ("li.ex-and:nth-child(8) > ul:nth-child(3) > li:nth-child(2)> ul:nth-child(2) > li:nth-child("
                + str(begin.day - 10) +") > span")
                page.locator(string).click()

            if (begin.day > 20):
                page.locator("li.ex-and:nth-child(8) > ul:nth-child(2) > li:nth-child(3) > span").click()
                string = ("li.ex-and:nth-child(8) > ul:nth-child(3) > li:nth-child(3)> ul:nth-child(2) > li:nth-child("
                + str(begin.day - 20) +") > span")
                page.locator(string).click()

            sleep(2)
            check = page.locator(".ex-pagination > li")
            count_check = check.count()
            while(count_check > 7):
                sleep(2)
                check = page.locator(".ex-pagination > li")
                count_check = check.count()
            if count_check == 0:
                count_check = 3

            for i in range(0, count_check - 2):
                sleep(2)
                crow = page.locator("div.ex-wrap-thumbnail a")
                crow_count = crow.count()
                for i in range(crow_count):
                    url = crow.nth(i).get_attribute("href")
                    urlv.append("https://www.belpressa.ru" + url)
                if count_check > 3:
                    page.locator(".ex-icon-chevron-right").click()

            begin += timedelta(days=1)
            page.locator("li.ex-and:nth-child(8) > i:nth-child(2)").click()
            page.locator("li.ex-and:nth-child(7) > i:nth-child(2)").click()
            page.locator("li.ex-and:nth-child(6) > i:nth-child(2)").click()
        browser.close()
        return urlv