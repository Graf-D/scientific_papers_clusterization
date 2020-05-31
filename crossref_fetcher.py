import csv
import time
import requests


BASE_URL = 'https://api.crossref.org/works'

payload = {
    'filter': 'has-abstract:true',
    'rows': 1000,
    'select': 'DOI,title,abstract,subject',
    'cursor': 'AoJ/qZnrtPECPxhodHRwOi8vZHguZG9pLm9yZy8xMC40MDI4L3d3dy5zY2llbnRpZmljLm5ldC9hbW0uNzkxLjI2',
    'mailto': 'rt.grafd@yandex.ru'
}

with open('crossref_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['DOI', 'title', 'abstract', 'subject']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()

    r = requests.get(BASE_URL, params=payload)
    r_data = r.json()['message']
    
    total_results = r_data['total-results']
    
    for i in range(total_results // 1000 + 1):
        for item in r_data['items']:
            writer.writerow(item)

        payload['cursor'] = r_data['next-cursor']
        with open('cursors.txt', 'a', encoding='utf-8') as txtfile:
            txtfile.write(r_data['next-cursor'] + '\n')

        r = requests.get(BASE_URL, params=payload)
        r_data = r.json()['message']

        time.sleep(int(r.headers['X-Rate-Limit-Interval'][:-1]))
