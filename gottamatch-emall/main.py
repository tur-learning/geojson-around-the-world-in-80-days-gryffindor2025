# Import necessary functions from utils.py
from utils import extract_files, load_data, find_best_matches, save_to_json, save_to_geojson, normalize_text

###############################
# 1) Define the input files
###############################
# HINT: The data is stored inside a ZIP archive.
# You need to extract two GeoJSON files:
# - `nolli_points_open.geojson`: Contains historical Nolli map features.
# - `osm_node_way_relation.geojson`: Contains OpenStreetMap (OSM) features.

zip_file = "geojson_data.zip"
geojson_files = ["nolli_points_open.geojson", "osm_node_way_relation.geojson"]

#nolli = "nolli_points_open.geojson"
#osm = "osm_node_way_relation.geojson"

###############################
# 2) Extract GeoJSON files
###############################
# HINT: Use the function `extract_files()` to extract the required files.
# This function returns a list of extracted file paths.

# extracted_files = ...
# nolli_file, osm_file = extracted_files  # Unpack the extracted file paths

nolli = extract_files("geojson_data.zip", "nolli_points_open.geojson")
osm = extract_files("geojson_data.zip", "osm_node_way_relation.geojson")

###############################
# 3) Load the GeoJSON data
###############################
# HINT: Use the function `load_data()` to read the JSON content of each extracted file.
# You should end up with two dictionaries:
# - `nolli_data`: Contains the historical map data.
# - `osm_data`: Contains modern OpenStreetMap features.

extracted_files = extract_files(zip_file, geojson_files)

# nolli_data = ...
# osm_data = ...

nolli_data = load_data("nolli_points_open.geojson")
osm_data = load_data("osm_node_way_relation.geojson")

#nolli_data("features") = nolli_features

###############################
# 4) Extract relevant info from Nolli data
###############################
# HINT: Each feature in `nolli_data["features"]` represents a historical landmark or road.
# You need to:
# 1️⃣ Extract the unique "Nolli Number" for each feature (use it as the dictionary key).
# 2️⃣ Extract the possible names for each feature from:
#    - "Nolli Name"
#    - "Unravelled Name"
#    - "Modern Name"
# 3️⃣ Store the feature's coordinates (geometry).
#
# Expected structure:
# {
#   "1319": {
#       "nolli_names": [
#           "Mole Adriana, or Castel S. Angelo",
#           "Mole Adriana, or Castel Sant'Angelo",
#           "Castel Sant'Angelo"
#       ],
#       "nolli_coords": {
#           "type": "Point",
#           "coordinates": [12.46670095, 41.90329709]
#       }
#   }
# }

# nolli_relevant_data = {}
# nolli_features = nolli_data["features"]

# for feature in nolli_features:
#     properties = feature.get("properties", {})
#     # Extract the Nolli Number as the key
#     # Extract the names
#     # Extract the geometry
#     # Store them inside nolli_relevant_data
features = ("Nolli Name", "Unravelled Name", "Modern Name")

Nolli_Number = 0
for feature in nolli_features:
    Nolli_Name = feature.get("Nolli Name", Nolli_Number, default=None)
    Unraveled_Name = feature.get("Unravelled Name", Nolli_Number, default=None)
    Modern_Name = feature.get("Modern Name", Nolli_Number, default=None)
    geometry = feature.get("geometry", Nolli_Number, default=None)

    feature.update_dict(nolli_relevant_data)

    Nolli_Number = Nolli_Number + 1




###############################
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
