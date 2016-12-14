import os




def start_requests():
    pages = []
    f = open("input.txt", "r")
    line = f.readline().replace('\n', '')
    for filename in os.listdir(line):
        pages.append("http://127.0.0.1:80/" + filename + "/Contents0.html")
    return pages


print start_requests()


    def start_requests(self):
        pages = []
        f = open("input.txt", "r")
        line = f.readline().replace('\n', '')
        print line
        print '\n'
        for filename in os.listdir(line):
            url = "http://127.0.0.1:80/" + filename + "/Contents0.html"
            page = scrapy.Request(url)
            pages.append(page)
        return pages
