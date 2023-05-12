import re
import requests
import openai
import os

ORGANIZATION = os.getenv("ORGANIZATION")
API_KEY = os.getenv("OPENAI_KEY")
SAMPLE_OUTPUT = "Key words: [key_words1], [key_words2], [key_words3], [key_words4], [key_words5]; \n Summary: this is a summary of certain article."

KEYWORD_REGEX = r"Key words:((?:,? ?[A-Za-z0-9_]+)+)"
SUMMARIZATION_PROMPT = f"Please first summerize 5 key words that best describe the content of the provided article, and then a summary of it within 300 words in same laugage as the input. Sample output should be something like this:\n{SAMPLE_OUTPUT}\n. Note: the summary part must starts with Summary:. \nArticle: \n\n"

openai.organization = ORGANIZATION
openai.api_key = API_KEY
openai.Model.list()


def summarize(document, SUMMARY_ON=True):
    if not SUMMARY_ON:
        return ""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    prompt = SUMMARIZATION_PROMPT + "\n" + document
    data = {
        "max_tokens": 200,
        "model": "gpt-3.5-turbo-0301",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    response = requests.post(url, headers=headers, json=data)
    summary = response.json()["choices"][0]["message"]["content"].strip()
    return summary


def extract_keywords(document):
    key_words = re.findall(r"Key words:((?:,? ?[A-Za-z0-9_]+)+)", document)
    if key_words:
        return key_words[0].split(",")
    else:
        return None


def extract_summary(input_text):
    if "Summary:" in input_text:
        summary = input_text.split("Summary:", 1)[1]
        return summary.strip()
    else:
        return "No summary found."
