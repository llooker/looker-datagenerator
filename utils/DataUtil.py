import datetime
import random
import os
import requests
import json

class DataUtil:
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
      url = f"https://roads.googleapis.com/v1/snapToRoads?path={coord}&interpolate=true&key={GOOGLE_MAPS_API_KEY}"
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
