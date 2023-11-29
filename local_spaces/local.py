from flask import Blueprint, render_template, current_app
from math import radians, cos, sin, asin, sqrt
import requests
from cachetools.func import ttl_cache

local = Blueprint(
    "local", __name__, template_folder="templates", static_folder="static"
)


def calculate_distance(src: tuple, dest: tuple) -> float:
    # https://stackoverflow.com/a/4913653
    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [src[0], src[1], dest[0], dest[1]])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


@local.route("/")
def index():
    return render_template("index.html")


@local.route("/local_spaces.json")
@ttl_cache(ttl=1800)
def spaces():
    # Get the local hackspace Space JSON
    resp = requests.get(current_app.config.get("LOCALSPACES_LOCAL_ENDPOINT"))

    if resp.ok:
        data = resp.json()
        source = data["location"]["lat"], data["location"]["lon"]

    # Iterate through hackspaces
    spaces = []
    resp = requests.get(current_app.config.get("LOCALSPACES_SPACEAPI_ENDPOINT"))
    if resp.ok:
        data = resp.json()

        for space in data:
            # If the SpaceAPI hasn't had a valid response, skip
            if not space["valid"]:
                continue
            # If the hackspace is the source, skip
            if space["url"] == current_app.config.get("LOCALSPACES_LOCAL_ENDPOINT"):
                continue

            # Check if the hackspace has a lat/lon
            if "location" in space["data"] and "lat" in space["data"]["location"]:
                dest = (
                    space["data"]["location"]["lat"],
                    space["data"]["location"]["lon"],
                )

                # If its within the radius, add it to the list
                distance = calculate_distance(source, dest)
                if distance <= float(current_app.config.get("LOCALSPACES_DISTANCE")):
                    print("Added {0}".format(space["data"]["space"]))
                    space['distance'] = distance
                    spaces.append(space)

    return sorted(spaces, key=lambda d: d['distance'])
