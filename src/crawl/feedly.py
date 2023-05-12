import json
import requests
import feedparser
import os
from openai_utils import summarize, extract_keywords, extract_summary

# Set your Feedly API credentials and access token
# client_id = 'your_client_id'
# client_secret = 'your_client_secret'
access_token = os.getenv('FEEDLY_ACCESS_TOKEN')
user_id = os.getenv('FEEDLY_USER_ID')


def fetch_by_streamId(id):
    # Set the Feedly API endpoint
    feedly_api_url = 'https://cloud.feedly.com/v3/streams/contents'
    # Replace the following with your Feedly category or feed ID
    stream_id = 'user/' + user_id + '/category/your_category'

    # Set the number of unread articles to retrieve (max: 1000)
    count = 10

    # Make a request to the Feedly API
    headers = {'Authorization': f'OAuth {access_token}'}
    params = {'streamId': id, 'count': count, 'unreadOnly': 'true'}
    response = requests.get(feedly_api_url, headers=headers, params=params)

    if response.status_code == 200:
        feed_data = response.json()
        for entry in feed_data['items']:
            title = entry['title']
            url = ''
            content = ''

            if 'canonical' in entry:
                url = entry['canonical'][0]['href']
            elif 'canonicalUrl' in entry:
                url = entry['canonicalUrl']

            if 'summary' in entry:
                content = entry['summary']['content']

            if len(entry['summary']['content']) > 200:
                # Call the ChatGPT API to summarize the content
                summary = summarize(content[:1500])

                raw_document = {
                    "title": title,
                    "summary": extract_summary(summary),
                    "rawContent": content,
                    "labels": extract_keywords(summary),
                    "url": url
                }
                # send the RawDocument to the create API endpoint
                headers = {'Content-type': 'application/json'}
                response = requests.post('http://localhost:3000/doc',
                                         headers=headers, data=json.dumps(raw_document))

                # print response status code and content
                print(response.status_code)
                print(response.content)
    else:
        print('Error:', response.status_code)


def list_subs():
    # Set the Feedly API endpoint
    feedly_api_url = 'https://cloud.feedly.com/v3/subscriptions'

    # Make a request to the Feedly API
    headers = {'Authorization': f'OAuth {access_token}'}
    response = requests.get(feedly_api_url, headers=headers)
    stream_ids = []
    if response.status_code == 200:
        subscriptions = response.json()

        for subscription in subscriptions:
            print('Subscription Title:', subscription['title'])
            print('Stream ID:', subscription['id'])
            print('----')
            stream_ids.append(subscription['id'])
    else:
        print('Error:', response.status_code)
    return stream_ids


for stream_id in list_subs():
    print(" unread content: " + stream_id)
    fetch_by_streamId(stream_id)
