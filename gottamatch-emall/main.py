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
nolli_Numbers_dict = {}

numberCounter = 0

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
                "Coordinates": nolliCoords
            }
        }
    }

    # Creating a dictionary for nolli numbers for later use
    nolliNumber_dict = {
        numberCounter: nolliNumber
    }

    # adding element_dict to master dictionary for all places from nolli_data
    for key, value in element_dict.items():
        nolli_simplified[key] = value

    # adding nolliNumber_dict to made dictionary for nolliNumbers
    for key1, value1 in nolliNumber_dict.items():
        nolli_Numbers_dict[key1] = value1

    numberCounter = numberCounter + 1
# --------------------------------------------------------------------------------------------------------------------------------

# 5) Fuzzy match with OSM data
###############################
# HINT: The `osm_data["features"]` list contains modern landmarks and roads.
# Each feature has a "name" field in its properties.
#
# For each Nolli entry:
# ✅ Compare its names with the "name" field of OSM features.
# ✅ Use fuzzy matching to find the closest match.
# ✅ Store the best match in the `nolli_relevant_data` dictionary.
#

# creating dictionary to hold matched names
nolli_relevent_data = {}

matchCounter = 0

for name in nolli_simplified:
    listofNames = nolli_simplified[name].get("Possible Names", None)
    find_best_matches(listofNames, osm_data.get("features", None))


print_dict(nolli_relevent_data)
print(matchCounter)

# Use the function `find_best_matches()`:
# - Pass the list of names from Nolli.
# - Search in the OSM dataset using `key_field="name"`.
# - Set `threshold=85` (minimum similarity score).
# - Use `scorer="partial_ratio"` for better matching.
from thefuzz import fuzz, process
 
# Test cases
search_names = ["St. Michael's Cathedral", "Washington Square Park", "Central Plaza"]
geojson_features = [
    {
      "properties": {"name": "Saint Michael Cathedral"}, 
     "geometry": {"coordinates": [10.0, 20.0]}
    },
    {
      "properties": {"name": "Washington Sq. Park"}, 
     "geometry": {"coordinates": [15.0, 25.0]}
    },
    {"properties": {"name": "Plaza Central"}, 
     "geometry": {"coordinates": [30.0, 40.0]}
    },
]
 
# Test different scorers
scorers = ["ratio", "partial_ratio", "token_sort_ratio", "token_set_ratio"]
 
for scorer in scorers:
    print(f"\n### Testing with {scorer} ###")
    
    for feature in geojson_features:
        feature_name = feature["properties"]["name"]
        best_match, score = process.extractOne(feature_name, search_names, 
                                               scorer=getattr(fuzz, scorer))
        
        print(f"Match for '{feature_name}': '{best_match}' → Score: {score}")

print(f"Searching best match for Nolli names:")

# counter = 0  # To track the number of successful matches
# for nolli_id, values in nolli_relevant_data.items():
#     print(f"\t{nolli_id}\t{values['nolli_names'][0]}")  # Print first name for reference
#
#     # Get the best match from OSM data
#     # match, j = find_best_matches(...)
#
#     # counter += j  # Update match counter
#     # nolli_relevant_data[nolli_id]["match"] = match  # Store the match

# print(f"MATCHED {counter} NOLLI ENTRIES")

###############################
# 6) Save results as JSON and GeoJSON
###############################
# HINT: Once all matches are found, save the results in two formats:
# ✅ `matched_nolli_features.json` → Standard JSON format for analysis.
# ✅ `matched_nolli_features.geojson` → A structured GeoJSON file for visualization.
#
# Use:
# - `save_to_json(nolli_relevant_data, "matched_nolli_features.json")`
# - `save_to_geojson(nolli_relevant_data, "matched_nolli_features.geojson")`

# save_to_json(...)
# save_to_geojson(...)

print("Matching complete. Results saved.")

###############################
# 7) Visualization
###############################
# 🎯 **Final Task**: Upload `matched_nolli_features.geojson` to:
# 🔗 **[geojson.io](https://geojson.io/)**
#
# 📌 Observe if the matched features align correctly.
# 📝 Take a screenshot and submit it as proof of completion!
