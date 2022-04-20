from json import dumps
from bel import belurl, belcrow
from fon import fonurl, foncrow
from aif import aifurl, aifcrow
from threading import Thread
def multi(url):
    if url.find("belpressa") != -1:
        temp = belurl(url)
    elif url.find("fontanka") != -1:
        temp = fonurl(url)
    else:
        temp = aifurl(url)
    return temp
def ranger(listing, urls, begin, end):
    for i in range(begin, end):
        while 1:
            try:
                print(str((i-1)//(len(urls)//8) + 1) + "-" + str(i) + " -> " + urls[i])
                listing.append(multi(urls[i]))
                urls[i] = 0
            except Exception as e:
                print(str((i-1)//(len(urls)//8) + 1) + "-" + str(i) + " -X> " + urls[i])
                print(e)
                print('Restarting!')
                continue
            else:
                break
tab = list()
print("Введите дату начала в формате YYYY-MM-DD")
begin = input()
print("Введите дату конца в формате YYYY-MM-DD")
end = input()
urlv = aifcrow(begin, end) + belcrow(begin, end) + foncrow(begin, end)
print(len(urlv))
count = len(urlv) // 8
thread1 = Thread(target=ranger, args=(tab, urlv, 0, count + 1))
thread2 = Thread(target=ranger, args=(tab, urlv, count + 1, count*2 + 1))
thread3 = Thread(target=ranger, args=(tab, urlv, count*2 + 1, count*3 + 1))
thread4 = Thread(target=ranger, args=(tab, urlv, count*3 + 1, count*4 + 1))
thread5 = Thread(target=ranger, args=(tab, urlv, count*4 + 1, count*5 + 1))
thread6 = Thread(target=ranger, args=(tab, urlv, count*5 + 1, count*6 + 1))
thread7 = Thread(target=ranger, args=(tab, urlv, count*6 + 1, count*7 + 1))
thread8 = Thread(target=ranger, args=(tab, urlv, count*7 + 1, len(urlv)))
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
json = dumps([news.__dict__ for news in tab], ensure_ascii=False, indent=4)
file = open("result.json", 'w', encoding="utf-8")
file.write(json)
file.close()