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

# employee_data = csv.DictReader(open("data/employees.csv"))
today = datetime.date.today()
# for row in employee_data:
#     # print({"000 row": row})
#     days_since_hired = (today -
#                         (datetime.datetime.strptime(
#                             row["hired_date"], '%Y-%m-%d').date())).days

#     if days_since_hired / 365 > 1:
#         row["title"] = random.choices(
#             titles_by_org[row["org"].lower().replace(' ', '_')])[0]
#         # print({"111 row": row})
#         csv.DictWriter.writerow(employee_data, row)

with open('data/employees.csv', 'a', newline='') as obj:
    employee_data = csv.DictReader(obj)
    print(employee_data)
    for row in employee_data:
        print({"000 row": row})
        days_since_hired = (today -
                            (datetime.datetime.strptime(
                                row["hired_date"], '%Y-%m-%d').date())).days
        print({"000 days_since_hired": days_since_hired})

        # if days_since_hired / 365 > 1:
        #     row["title"] = random.choices(
        #         titles_by_org[row["org"].lower().replace(' ', '_')])[0]
        #     # print({"111 row": row})
        #     csv.DictWriter.writerow(employee_data, row)
        #     # Pass the CSV  file object to the Dictwriter() function
        #     # Result - a DictWriter object
        #     dictwriter_object = csv.DictWriter(employee_data)
        #     # Pass the data in the dictionary as an argument into the writerow() function
        #     dictwriter_object.writerow(row)
        #     # Close the file object
    employee_data.close()
