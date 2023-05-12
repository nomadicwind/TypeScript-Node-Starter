import re
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import json

import html
from newspaper import Article
from openai_utils import summarize, extract_keywords, extract_summary

# Function that use arcticle library to download and extract textual content


def extract_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text


# make a GET request to the Hacker News homepage
r = requests.get("https://news.ycombinator.com/")
soup = BeautifulSoup(r.text, "html.parser")

# extract the top 10 news links and titles
links = soup.select(".titleline > a")[:10]
titles = [link.text for link in links]

# loop through each news article and extract its content
for i, link in enumerate(links):
    content = extract_article(link["href"])

    # Call the ChatGPT API to summarize the content
    summary = summarize(content[:1500])

    raw_document = {
        "title": titles[i],
        "summary": extract_summary(summary),
        "rawContent": content,
        "labels": extract_keywords(summary),
        "url": link["href"],
    }

    # send the RawDocument to the create API endpoint
    headers = {"Content-type": "application/json"}
    response = requests.post(
        "http://localhost:3000/doc", headers=headers, data=json.dumps(raw_document)
    )

    # print response status code and content
    print(response.status_code)
    print(response.content)
