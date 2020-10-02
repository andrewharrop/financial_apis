import requests
import json
import prettytable
from datetime import datetime

headers = {'Content-type': 'application/json'}
api_key = your_api_key                                # requires user input
_start = datetime.now().year - 15
_end = datetime.now().year
_table = True


#some of the following code was sourced from BLS, found here: https://www.bls.gov/developers/api_signature_v2.htm and here: https://www.bls.gov/developers/api_python.htm

#this function formats the api call
def request_json(start, end, series='', multiple_series=None):
    if multiple_series is None:
        multiple_series = []
    if multiple_series:
        data = json.dumps({"seriesid": multiple_series, "startyear": str(start), "endyear": str(end),
                           "registrationkey": api_key})
    else:
        data = json.dumps({"seriesid": [series], "startyear": str(start), "endyear": str(end),
                           "registrationkey": api_key})

    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data,
                      headers={'Content-type': 'application/json'})
    return [p, json.loads(p.text)]


#this function was derived from the bls souce code & returns data
def table_series(json_data_form):
    for series in json_data_form['Results']['series']:
        x = prettytable.PrettyTable(["seriesID", "year", "period", "value", "footnotes"])
        seriesId = series['seriesID']
        for item in series['data']:
            year = item['year']
            period = item['period']
            value = item['value']
            footnotes = ""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','
            x.add_row([seriesId, year, period, value, footnotes[0:-1]])

        
        return x.get_string()


#this is the function designated for user input
def data_hub(series_id, table=_table, start=_start, end=_end):
    if table:
        return table_series(request_json(start, end, series_id)[1])
    else:
        return json.dumps(request_json(start, end, series_id)[0].json(), indent=4, sort_keys=True)

#sample usage
print(data_hub("some series")) //prints 15 years of the most recent data in a table 
print(data_hub("some series", table = False)) //prints 15 years of the most recent data in formatted json
print(data_hub("some series", table = False, start=2010)) //prints 10 years of the most recent data, starting in 2010, in formatted json
print(data_hub("some series", start=2010, end=2018)) //prints 8 years of data, starting in 2010 and ending in 2018, in a table


