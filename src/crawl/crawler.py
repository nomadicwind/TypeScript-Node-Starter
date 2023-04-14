import requests
from bs4 import BeautifulSoup
import json
from unidecode import unidecode

# make a GET request to the Hacker News homepage
r = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(r.text, 'html.parser')

# extract the top 10 news links and titles
links = soup.select('.titleline > a')[:10]
titles = [link.text for link in links]

# loop through each news article and extract its content
for i, link in enumerate(links):
    r = requests.get(link['href'])
    soup = BeautifulSoup(r.text, 'html.parser')

    # extract the content of the article and construct a RawDocument object
    content = unidecode(soup.text)
    raw_document = {
        "title": titles[i],
        # use first 200 characters of content as summary
        "summary": content[:200],
        "rawContent": content,
        "url": link['href']
    }

    # send the RawDocument to the create API endpoint
    headers = {'Content-type': 'application/json'}
    response = requests.post('http://localhost:3000/doc',
                             headers=headers, data=json.dumps(raw_document))

    # print response status code and content
    print(response.status_code)
    print(response.content)
