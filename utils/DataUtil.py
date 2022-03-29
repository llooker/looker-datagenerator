import constants
import csv
import datetime
from faker import Faker
import json
import os
import requests
import random

fake = Faker()
class DataUtil:
    def __init__(self):
        self.location_data = self.generate_locations()

    def child_created_at(
        self, probability: str = "uniform"
    ) -> datetime.datetime:  # returns a random timestamp between now and parent date
        time_between_dates = datetime.datetime.now() - self.parent.created_at
        days_between_dates = time_between_dates.days
        if days_between_dates <= 1:
            days_between_dates = 2
        random_number_of_days = random.randrange(
            1, days_between_dates
        )  # generates random day between now and when user initially got created
        created_at = self.parent.created_at + datetime.timedelta(
            days=random_number_of_days
        )
        return created_at

    def random_item(
        self, population, **distribution
    ) -> str:  # returns single random item from a list based off distribution
        if distribution:
            return random.choices(
                population=population, weights=distribution["distribution"]
            )[0]
        else:
            return random.choices(population=population)[0]

    def random_float(self, max_num) -> float:
        return random.uniform(0, max_num)

    def random_int(self, max_num) -> int:
        return random.randrange(max_num)

    def snap_to_road(self, x_coord: float, y_coord: float) -> float:
      coord = str(x_coord) + "," + str(y_coord)
      url = f"https://roads.googleapis.com/v1/snapToRoads?path={coord}&interpolate=true&key={constants.GOOGLE_MAPS_API_KEY}"
      payload={}
      headers = {}
      location = None
      response = requests.request("GET", url, headers=headers, data=payload)
      try:
          location = json.loads(response.text)["snappedPoints"][0]["location"]
      except:
          location = response.text
      return location

    def created_at(self, start_date: datetime.datetime) -> datetime.datetime:
      end_date = datetime.datetime.now()
      time_between_dates = end_date - start_date
      days_between_dates = time_between_dates.days
      if days_between_dates <= 1:
          days_between_dates = 2
      random_number_of_days = random.randrange(1, days_between_dates)
      created_at = (
          start_date
          + datetime.timedelta(days=random_number_of_days))
      return created_at

    #get coordinates using Google Maps API
    def get_coordinates(self):
        # while location_found:
        tmp_lat_coord = constants.MIN_LAT_COORD + self.random_float(constants.MIN_LAT_COORD_DIFF)
        tmp_lng_coord = constants.MIN_LNG_COORD + self.random_float(constants.MIN_LNG_COORD_DIFF)
        location = self.snap_to_road( tmp_lng_coord, tmp_lat_coord)
        while len(location) == 3:
            tmp_lat_coord = constants.MIN_LAT_COORD + self.random_float(constants.MIN_LAT_COORD_DIFF)
            tmp_lng_coord = constants.MIN_LNG_COORD + self.random_float(constants.MIN_LNG_COORD_DIFF)
            location = self.snap_to_road(tmp_lat_coord, tmp_lng_coord)
        return location

    #read from local csv and return locations
    def generate_locations(self):
        location_data  = []
        with open("helper/world_pop.csv", encoding="utf-8") as worldcsv:
            csvReader = csv.DictReader(worldcsv)
            for rows in csvReader:
                location_data.append(rows)
        return location_data

    #returns random address based off specified distribution
    def get_address(self, *, country='*',state='*',postal_code='*'):
        # country = '*' OR country = 'USA' OR country={'USA':.75,'UK':.25}
        # state = '*' OR state = 'California' OR state={'California':.75,'New York':.25}
        # postal_code = '*' OR postal_code = '95060' OR postal_code={'94117':.75,'95060':.25}
        universe = []
        if postal_code != '*':
            if type(postal_code) == str:
                universe += list(filter(lambda row: row['postal_code'] == postal_code, self.location_data))
            elif type(postal_code) == dict:
                universe += list(filter(lambda row: row['postal_code'] in postal_code.keys(), self.location_data))
        if state != '*':
            if type(state) == str:
                universe += list(filter(lambda row: row['state'] == state, self.location_data))
            elif type(state) == dict:
                universe += list(filter(lambda row: row['state'] in state.keys(), self.location_data))
        if country != '*':
            if type(country) == str:
                universe += list(filter(lambda row: row['country'] == country, self.location_data))
            elif type(country) == dict:
                universe += list(filter(lambda row: row['country'] in country.keys(), self.location_data))
        if len(universe) == 0:
            universe = self.generate_locations()

        total_pop = sum([int(loc['population']) for loc in universe])

        for loc in universe:
            loc['population'] = int(loc["population"])
            if type(postal_code) == dict:
                if loc['postal_code'] in postal_code.keys():
                    loc['population'] = postal_code[loc['postal_code']] * total_pop
            if type(state) == dict:
                if loc['state'] in state.keys():
                    loc['population'] = state[loc['state']] * \
                        (loc['population']/sum([loc2['population'] for loc2 in universe if loc['state']==loc2['state']])) * \
                            total_pop
            if type(country) == dict:
                if loc['country'] in country.keys():
                    loc['population'] = country[loc['country']] * (loc['population']/sum([loc2['population'] for loc2 in universe if loc['country']==loc2['country']])) * \
                            total_pop

        loc = random.choices(universe, weights = [loc['population']/total_pop for loc in universe])[0]
        return {
            'street_address': fake.street_address(),
            'city': loc['city'],
            'state': loc['state'],
            'postal_code': loc['postal_code'],
            'country': loc['country'],
            'latitude': loc["latitude"],
            'longitude': loc['longitude']
        }

