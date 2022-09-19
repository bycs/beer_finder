from dataclasses import dataclass
from math import atan2
from math import cos
from math import radians
from math import sin
from math import sqrt

import requests

from config import GRAPHHOPPER_KEY
from config import YANDEXMAP_KEY


@dataclass
class Point:
    latitude: float
    longitude: float

    def __init__(self, latitude: float, longitude: float) -> None:
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"

    def to_dict(self):
        point: dict = {"latitude": self.latitude, "lng": self.longitude}
        return point


def get_distance(point1: Point, point2: Point) -> float:
    R = 6372800  # Earth radius in meters
    latitude_1 = radians(point1.latitude)
    latitude_2 = radians(point2.latitude)
    longitude_1 = radians(point1.longitude)
    longitude_2 = radians(point2.longitude)
    dlat = latitude_2 - latitude_1
    dlon = longitude_2 - longitude_1
    a = sin(dlat / 2) ** 2 + cos(latitude_1) * cos(latitude_2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


class YandexMapGeo:
    KEY = YANDEXMAP_KEY

    def geocode(self, address: str) -> Point | None:
        url = "https://geocode-maps.yandex.ru/1.x/"
        params: dict = {
            "geocode": address,
            "format": "json",
            "results": 1,
            "apikey": self.KEY,
            "lang": "ru_RU",
        }
        r = requests.get(url, params=params)
        response = r.json()
        try:
            featuremember = response["response"]["GeoObjectCollection"]["featureMember"][0]
            coordinates = featuremember["GeoObject"]["Point"]["pos"].split()
            latitude, longitude = coordinates
            point = Point(latitude, longitude)
            return point
        except KeyError or IndexError:
            return None


class GraphhopperGeo:
    KEY = GRAPHHOPPER_KEY

    def geocode(self, address: str) -> Point | None:
        url = "https://graphhopper.com/api/1/geocode"
        params: dict = {"q": address, "locale": "ru", "limit": 1, "key": self.KEY}
        r = requests.get(url, params=params)
        response = r.json()
        try:
            latitude = response["hits"][0]["point"]["lat"]
            longitude = response["hits"][0]["point"]["lng"]
            point = Point(latitude, longitude)
            return point
        except KeyError or IndexError:
            return None

    def route(self, from_p: Point, to_p: Point) -> str | None:
        url = "https://graphhopper.com/api/1/route"
        params = {
            "point": [f"{from_p.latitude},{from_p.longitude}", f"{to_p.latitude},{to_p.longitude}"],
            "vehicle": "foot",
            "locale": "ru",
            "key": self.KEY,
        }
        r = requests.get(url, params=params)
        response = r.json()
        try:
            distance: str = response["paths"][0]["distance"]
            return distance
        except KeyError or IndexError:
            return None
