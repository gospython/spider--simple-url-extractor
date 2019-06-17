from queue import Queue
import tldextract
from time import sleep
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict


def spider(urls_q):
    while True:
        # check queue
        if urls_q.empty():
            sleep(5)
            if urls_q.empty():
                print('queue is empty')
                break
        try:
            # take url from queue
            url = urls_q.get()

            # start extract urls from page
            r = session.get(url)
            links = r.html.absolute_links

            # check if extracr link is current domain
            for link in links:
                if gen_domain in link:
                    if link in internal_urls:
                        continue
                    else:
                        urls_q.put(link)
                        internal_urls.add(link)

            # check if extract link in database
                else:
                    ext = tldextract.extract(link)
                    domain = ext.domain + '.' + ext.suffix
                    # kostil in attack
                    with open('domain_database.txt', 'r', encoding='UTF-8') as file_domain_database:
                        file_reader = file_domain_database.read()
                        if domain in file_reader:
                            checker = True
                        else:
                            checker = False

                    if checker is True:
                        continue
            # write only unique domain
                    else:
                        with open('domain_database.txt', 'a', encoding='UTF-8') as file_domain_database:
                            file_domain_database.write(domain + '\n')
                        with open(gen_domain+'_all_external.txt', 'a', encoding='utf-8') as domain_external_domains:    
                            domain_external_domains.write(domain + '\n')
                            print(domain)
                            # external_domains.add(domain)
                    
        except Exception as error:
            with open(gen_domain+'_error.txt', 'a', encoding='UTF-8') as file_error:
                file_error.write(domain+'\n')
            print('Error:', str(error), str(type(error)))

gen_domain = 'wikipedia.org'                            # you domain
start_url = 'https://en.wikipedia.org/wiki/Main_Page'   # start url

internal_urls = set()
# external_domains = set()

urls_q = Queue()
urls_q.put(start_url)

session = HTMLSession()

threads = 10

with ThreadPoolExecutor(max_workers=threads) as ex:
    for _ in range(threads):
        ex.submit(spider, urls_q)
