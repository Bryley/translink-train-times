from google.transit import gtfs_realtime_pb2
from datetime import datetime
import urllib.request
from objects import Trip

from read import get_stop_ids

from rich import print, inspect

FLIP = False

START_STOP = "TODO Fill here"
END_STOP = "TODO Fill here"

def find_from(place_from: set[int], place_to: set[int]) -> list[tuple[int, int, Trip]]:
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.request.urlopen(
        "https://gtfsrt.api.translink.com.au/api/realtime/SEQ/TripUpdates"
    )

    # response = urllib.request.urlopen(
    #     "https://gtfsrt.api.translink.com.au/api/realtime/SEQ/VehiclePositions"
    # )

    items: list[tuple[int, int, Trip]] = []

    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            places = []
            for t in entity.trip_update.stop_time_update:
                stop = int(t.stop_id)
                if stop in place_from or stop in place_to:
                    places.append((stop, t.departure.time, t.arrival.time))
            if len(places) == 2 and places[0][0] in place_from:
                items.append(
                    (
                        places[0][0],
                        places[1][0],
                        Trip(dep_time=places[0][1], arrive_time=places[1][2]),
                    )
                )

    return sorted(items, key=lambda x: x[2].dep_time)


from_stops = {stop.id: stop for stop in get_stop_ids(START_STOP)}
to_stops = {stop.id: stop for stop in get_stop_ids(END_STOP)}

a = find_from(set(from_stops.keys()), set(to_stops.keys()))

for i in a:
    stop_from = from_stops[i[0]]
    stop_to = to_stops[i[1]]
    if i[2].dep_time > datetime.now():
        print(i[2].output(stop_from, stop_to))
