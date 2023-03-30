import csv
from typing import Literal
from pydantic import BaseModel
from objects import Stop, Place

from rich import print


def get_stop_ids(place: Place) -> set[Stop]:
    with open("./data/stops.txt", "r") as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            if place.lower() in row["stop_name"].lower() and row["platform_code"] != "":
                data.append(row)

    return {
        Stop(id=row["stop_id"], name=row["stop_name"], platform=row["platform_code"])
        for row in data
    }
