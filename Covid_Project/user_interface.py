from flask import Flask, render_template
from flask import request
from covid_data_handler import process_covid_csv_data, covid_api_request, schedule_covid_updates
from covid_news_handling import news_API_request


app = Flask(__name__)

@app.route('/')
def main():
    national7day_cases = process_covid_csv_data('nation_2021-10-28.csv')
    local_cases = covid_api_request('Exeter', 'ltla')
    news_data = news_API_request()
    return render_template('home.html', location= 'Exeter', 
    nation_location = 'United Kingdom',
    local_7day_infections = local_cases,
    national_7day_infections = national7day_cases[0],
    hospital_cases = national7day_cases[1],
    deaths_total = national7day_cases[2],
    news_articles = news_data,
    )

@app.route('/index?update=&covid-data=covid-data&news=news')
def updated_news():
    national7day_cases = process_covid_csv_data('nation_2021-10-28.csv')
    local_cases = covid_api_request('Exeter', 'ltla')
    news_data = news_API_request()
    return render_template('home.html', location= 'Exeter', 
    nation_location = 'United Kingdom',
    local_7day_infections = local_cases,
    national_7day_infections = national7day_cases[0],
    hospital_cases = national7day_cases[1],
    deaths_total = national7day_cases[2],
    news_articles = news_data,
    )    

if __name__ == '__main__':
    app.run() 