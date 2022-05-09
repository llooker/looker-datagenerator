import csv
import datetime
import random
titles_by_org = {
    "sales": ["AE", "SE", "FSR"],
    "marketing": ["Marketing Analyst", "Marketing Manager"],
    "engineering": ["SWE", "Data Eng"],
    "product": ["PM", "UI", "UX"],
    "customer_success": ["CSM", "CSE", "TSM"],
}

today = datetime.date.today()

with open('data/employees.csv', 'a', newline='') as obj:
    employee_data = csv.DictReader(obj)
    print(employee_data)
    for row in employee_data:
        print({"000 row": row})
        days_since_hired = (today -
                            (datetime.datetime.strptime(
                                row["hired_date"], '%Y-%m-%d').date())).days
        print({"000 days_since_hired": days_since_hired})
    employee_data.close()