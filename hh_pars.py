import time
import csv
import requests
from bs4 import BeautifulSoup as bs

accept = r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
user_agent = r'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'

headers = {'accept': accept,
           'user-agent': user_agent}

base_url = r'https://krasnodar.hh.ru/search/vacancy?L_is_autosearch=false&area=53&clusters=true&enable_snippets=true&text=python&page=0'


def hh_parse(base_url, headers):
    jobs = []
    urls = [base_url]
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://krasnodar.hh.ru/search/vacancy?L_is_autosearch=false&area=53&clusters=true' \
                      f'&enable_snippets=true&text=python&page={i} '
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                content = text1 + ' ' + text2
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'content': content
                })
            except:
                pass
        print(len(jobs))
    else:
        print('ERROR or DONE', request.status_code)

    return jobs


def files_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название ваканисии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))


jobs = hh_parse(base_url, headers)
files_writer(jobs)