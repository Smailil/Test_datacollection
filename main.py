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
                print(str((i-1)//(len(urls)//16) + 1) + "-" + str(i) + " -> " + urls[i])
                listing.append(multi(urls[i]))
                urls[i] = 0
            except Exception as e:
                print(str((i-1)//(len(urls)//16) + 1) + "-" + str(i) + " -X> " + urls[i])
                print(e)
                print('Restarting!')
                continue
            else:
                break
tab = list()
begin = "2022-02-01"
end = "2022-02-28"
urlv = aifcrow(begin, end) + belcrow(begin, end) + foncrow(begin, end)
print(len(urlv))
count = len(urlv) // 16
thread1 = Thread(target=ranger, args=(tab, urlv, 0, count + 1))
thread2 = Thread(target=ranger, args=(tab, urlv, count + 1, count*2 + 1))
thread3 = Thread(target=ranger, args=(tab, urlv, count*2 + 1, count*3 + 1))
thread4 = Thread(target=ranger, args=(tab, urlv, count*3 + 1, count*4 + 1))
thread5 = Thread(target=ranger, args=(tab, urlv, count*4 + 1, count*5 + 1))
thread6 = Thread(target=ranger, args=(tab, urlv, count*5 + 1, count*6 + 1))
thread7 = Thread(target=ranger, args=(tab, urlv, count*6 + 1, count*7 + 1))
thread8 = Thread(target=ranger, args=(tab, urlv, count*7 + 1, count*8 + 1))
thread9 = Thread(target=ranger, args=(tab, urlv, count*8 + 1, count*9 + 1))
thread10 = Thread(target=ranger, args=(tab, urlv, count*9 + 1, count*10 + 1))
thread11 = Thread(target=ranger, args=(tab, urlv, count*10 + 1, count*11 + 1))
thread12 = Thread(target=ranger, args=(tab, urlv, count*11 + 1, count*12 + 1))
thread13 = Thread(target=ranger, args=(tab, urlv, count*12 + 1, count*13 + 1))
thread14 = Thread(target=ranger, args=(tab, urlv, count*13 + 1, count*14 + 1))
thread15 = Thread(target=ranger, args=(tab, urlv, count*14 + 1, count*15 + 1))
thread16 = Thread(target=ranger, args=(tab, urlv, count*15 + 1, len(urlv)))
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()
thread7.start()
thread8.start()
thread9.start()
thread10.start()
thread11.start()
thread12.start()
thread13.start()
thread14.start()
thread15.start()
thread16.start()
thread1.join()
thread2.join()
thread3.join()
thread4.join()
thread5.join()
thread6.join()
thread7.join()
thread8.join()
thread9.join()
thread10.join()
thread11.join()
thread12.join()
thread13.join()
thread14.join()
thread15.join()
thread16.join()
json = dumps([news.__dict__ for news in tab], ensure_ascii=False, indent=4)
file = open("result.json", 'w', encoding="utf-8")
file.write(json)
file.close()