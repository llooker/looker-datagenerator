import csv
import datetime
import random
titles_by_org = {
    "Sales": ["AE", "SE", "FSR"],
    "Marketing": ["Marketing Analyst", "Marketing Manager"],
    "Engineering": ["SWE", "Data Eng"],
    "Product": ["PM", "UI", "UX"],
    "Customer Success": ["CSM", "CSE", "TSM"],
}

today = datetime.date.today()

with open('data/employees.csv', 'r+', newline='') as obj:
    dict_reader = csv.DictReader(obj)
    dict_writer = csv.writer(obj)

    for row in list(dict_reader):
        days_since_hired = (today -
                            (datetime.datetime.strptime(
                                row["hired_date"], '%Y-%m-%d').date())).days
        if days_since_hired / 365 > 6:
            row["title"] = random.choices(
                [i for i in titles_by_org[row["org"]] if i != row["org"]])[0]
            dict_writer.writerow(row.values())
