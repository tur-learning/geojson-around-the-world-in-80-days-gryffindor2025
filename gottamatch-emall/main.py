# Import necessary functions from utils.py
from utils import extract_files, load_data, find_best_matches, save_to_json, save_to_geojson, print_dict

# --------------------------------------------------------------------------------------------------------------------------------

# 1) Define the input files

zip_file = "geojson_data.zip"
geojson_files = ["nolli_points_open.geojson", "osm_node_way_relation.geojson"]

###############################
# 2) Extract GeoJSON files

# Don't need these functioning because already completed these functions (one time uses)
#extracted_files = extract_files(zip_file, geojson_files)
#nolli_file, osm_file = extracted_files  # Unpack the extracted file paths

# --------------------------------------------------------------------------------------------------------------------------------

# 3) Load the GeoJSON data

nolli_data = load_data("nolli_points_open.geojson")
osm_data = load_data("osm_node_way_relation.geojson")

# --------------------------------------------------------------------------------------------------------------------------------

# 4) Extract relevant info from Nolli data

# creating a value holding all information from nolli_data and osm_data
features = nolli_data.get("features", None)

# creating empty master dictionary for all places from nolli_data
nolli_simplified = {}

# reading every entry from nolli_data and storing simplified data
for element in features:
    # extracting data from nolli_data
    properties = element.get("properties", None)
    geometry = element.get("geometry", None)

    # Creating varable holding nolli number
    nolliNumber = properties.get("Nolli Number", None)

    # Creating list of possible names for the object
    possibleNames = []
    possibleNames.append(properties.get("Nolli Name", None))
    possibleNames.append(properties.get("Unravelled Name", None))
    possibleNames.append(properties.get("Modern Name"))

    # for if there there is a missing value
    if geometry is not None:
        nolliType = geometry.get("type", None)
        nolliCoords = geometry.get("coordinates", None)
    else:
        nolliType = None
        nolliCoords = None

    # creating dictionary for single place from nolli_data
    element_dict = {
        nolliNumber : {
            "Possible Names": possibleNames,
            "Geometry": {
                "Type": nolliType,
                "coordinates": nolliCoords
            }
        }
    }

    # adding element_dict to master dictionary for all places from nolli_data
    for key, value in element_dict.items():
        nolli_simplified[key] = value

# --------------------------------------------------------------------------------------------------------------------------------

# 5) Fuzzy match with OSM data

# creating dictionary for matches
nolli_relevant_data = {}

# creating counter for # of matches
matchCounter = 0

# stating he have begun matching
print(f"Searching best match for Nolli names:")

# looking through each elemnt of nolli_simplified
for name in nolli_simplified:
    # gettings names to check against in osm_data
    listofNames = nolli_simplified[name].get("Possible Names", None)

    # getting coordinates of elements of nolli_simplified
    nolli_coords = nolli_simplified[name].get("Geometry", None)

    # finding matches
    match = find_best_matches(listofNames, osm_data.get("features", None))

    # creating open dictionary to add matches to master dictionary
    openDict = {}

    # checking to make sure match isn't null
    if match != (None, 0):
        # creating element for master dictionary
        openDict = {
            matchCounter : {
                "nolli_names" : listofNames,
                "nolli_coords" : nolli_coords,
                "match" : match
            }
        }

        # adding element dictionary into master dictionary
        for keys, values in openDict.items():
            nolli_relevant_data[keys] = values

        # stating another match was made
        matchCounter = matchCounter + 1
    # if match is empty, don't bother
    else:
        pass

# stating how many matches have been made
print(f"MATCHED {matchCounter} NOLLI ENTRIES")

# --------------------------------------------------------------------------------------------------------------------------------

# 6) Save results as JSON and GeoJSON

# Already used these. Don't need to use again

save_to_json(nolli_relevant_data, "matched_nolli_features.json")
save_to_geojson(nolli_relevant_data, "matched_nolli_features.geojson")

print("Matching complete. Results saved.")

###############################
# 7) Visualization
###############################
# 🎯 **Final Task**: Upload `matched_nolli_features.geojson` to:
# 🔗 **[geojson.io](https://geojson.io/)**
#
# 📌 Observe if the matched features align correctly.
# 📝 Take a screenshot and submit it as proof of completion!
