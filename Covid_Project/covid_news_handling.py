import requests
import json
import csv


def news_API_request():
    covid_terms = ["Covid&", "COVID-19&", "coronavirus&"]
    f = open('config.json')
    loaded_data = json.load(f)
    filter_data = loaded_data[0]
    api_key = filter_data['api_key']
    url = "https://newsapi.org/v2/"
    headlines = []
    url_builder = url + "top-headlines?" + "q=" + covid_terms[0] + api_key
    data = requests.get(url_builder)
    data_json = data.json()
    articles = data_json["articles"]
    with open('news.json', 'w') as f:
        json.dump(articles, f, indent=2)
    for x in articles:
        headlines.append(x['title'])
    return headlines

print(news_API_request())


