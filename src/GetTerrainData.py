import hou
import requests
import math.cos as cos
import math.radians as radians


elevation_api_endpoint = "https://api.open-elevation.com/api/v1/lookup"

node = hou.pwd()
geo = node.geometry()
digital_asset_node = node.parent()

coord = [
    digital_asset_node.parm("coordx").eval(),
    digital_asset_node.parm("coordy").eval(),
]

samples = 16
sample_locations = []

width = digital_asset_node.parm("width").eval()
half_width = width / 2
width_step = width / 16


# Generate Latitude and Longitude co-ordinates to sample
for x in range(0, samples):
    x_m_change = -half_width + width_step * x
    x_km_change = x_m_change / 1000
    lat = coord[0] + x_km_change / 110.6

    for y in range(0, samples):
        y_m_change = -half_width + width_step * y
        y_km_change = y_m_change / 1000
        lon = coord[1] + y_km_change / (111.3 * cos(radians(lat)))

        sample_locations.append({"latitude": lat, "longitude": lon})

# Obtain elevation data
request_body = {"locations": sample_locations}
request = requests.post(elevation_api_endpoint, json=request_body)

# Assign Elevation data to heightfield
prims = geo.prims()
elevation = prims[0]
mask = prims[1]

voxel_index = elevation.posToIndex()


print(request)
