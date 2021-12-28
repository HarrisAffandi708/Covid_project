import csv
import json
from uk_covid19 import Cov19API
import sched
import time

def parse_csv_data(csv_filename):
    with open(csv_filename, 'r') as csvfile:
        csv_reader =csv.reader(csvfile)
        rows = []
        for row in csv_reader:
            rows.append(row)
    return rows

def process_covid_csv_data(covid_csv_data):
    with open(covid_csv_data, 'r') as covid_data:
        covid_data_reader = csv.DictReader(covid_data)
        daily_cases = []
        current_hospital_cases = []
        total_death_unfiltered = []
        total_death_filtered = None
        total_hospital_cases = []
        last7days_cases = None
        empty = ''
        sum = 0
        for all_cases in covid_data_reader:   
            daily_cases.append(all_cases['newCasesBySpecimenDate'])
            total_death_unfiltered.append(all_cases['cumDailyNsoDeathsByDeathDate'])
            total_hospital_cases.append(all_cases['hospitalCases'])
        for x in range(2, 9):
            sum = sum + int(daily_cases[x])
            if x ==8:
                last7days_cases = sum
        for x in total_death_unfiltered:
            if x == empty:
                pass
            else:
                digit = int(x)
                total_death_filtered = digit
                break
        current_hospital_cases = int(total_hospital_cases[0])
        return last7days_cases, current_hospital_cases, total_death_filtered
        
def covid_api_request(location,location_type):

    Exeter_only = [
        'areaType=ltla',
        'areaName=Exeter'
    ]
    
    cases_and_death = {
    "date": "date",
    "areaName": "areaName",
    "areaCode": "areaCode",
    "newCasesByPublishDate": "newCasesByPublishDate",
    "cumCasesByPublishDate": "cumCasesByPublishDate",
    "newDeaths28DaysByDeathDate": "newDeaths28DaysByDeathDate",
    "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }
    api = Cov19API(filters= Exeter_only, structure= cases_and_death)
    data = api.get_json()
    data_1 = data['data']
    last7days_cases = 0
    sum = 0
    with open('covid_data.csv', 'w') as file:
        json.dump(data, file, indent=2)
    for x in  range (0,8):
        data_2 = data_1[x]
        sum = sum + data_2['newCasesByPublishDate'] 
        last7days_cases = sum     
    return last7days_cases
    

        




def schedule_covid_updates(update_interval):
    s = sched.scheduler(time.time, time.sleep)
    int(update_interval)
    x=0
    s.enter(update_interval, 1, covid_api_request("Exeter", "ltla"))
    while x <10000:
        s.enter(update_interval, 1, covid_api_request("Exeter", "ltla"))
        x += 1



