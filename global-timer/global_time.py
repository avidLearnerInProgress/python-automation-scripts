import pytz
import datetime
import argparse
from timezonefinder import TimezoneFinder
from pygeocoder import Geocoder

location = str(input("Enter location:"))

if location != "":
    # Obtain longitude, latitude via Geocoder
    result = Geocoder.geocode(location)
    coordinate = result[0].coordinates
    location = ", ".join([result[0].city, result[0].country])
    # Fetch Timezone by longitude, latitude via timezonefinder
    tf = TimezoneFinder()
    timezone = tf.timezone_at(lat=coordinate[0], lng=coordinate[1])
	time = datetime.datetime.now(pytz.timezone(timezone))
	print("%s %s" % (location, str(time).split('.')[0]))