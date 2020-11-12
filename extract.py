#!/usr/bin/env python3

import os
import yaml
import json
from rdflib import Graph, plugin, URIRef, Literal
import urllib.request

data_path = "../lineage_wiki/_data/devices/"
rdf_dump = "./lineage.nt"
stats_url = "https://stats.lineageos.org/api/v1/stats"

def urlencode(k):
    if isinstance(k, str):
        return k.replace(' ', '%20')
    return k

def urlencode_keys(dictionary):
    if isinstance(dictionary, dict):
        return {urlencode(k): urlencode_keys(v) for k, v in dictionary.items()}
    elif isinstance(dictionary, list):
        return [urlencode_keys(v) for v in dictionary]
    return dictionary

g = Graph()

def get_devices():
    print("get devices")
    for subdir, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith(".yml"):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r') as device_info_in:
                    device_info = yaml.safe_load(device_info_in)
                    # Add JSON-LD context
                    device_info["@context"] = {"@vocab": "https://wiki.lineageos.org/devices/schema#"}
                    device_info["@id"] = "https://wiki.lineageos.org/devices/" + file[:-4]
                    device_info["@type"] = "https://wiki.lineageos.org/devices/schema#Mobile"
                    # replace spaces in keys
                    device_info = urlencode_keys(device_info)
                    try:
                        json_data = json.dumps(device_info, default=str)
                        g.parse(data=json_data, format='json-ld')
                    except Exception as e:
                        print(file_path)
                        print(device_info)
                        print(e)
                        break

def get_stats():
    """
    Get stats for the devices.
    The endpoint implementation is here: https://github.com/lineageos-infra/tribble-tracker/blob/master/app.py
    """
    print("get stats")
    with urllib.request.urlopen(stats_url) as stats_in:
        stats_json = json.load(stats_in)
        for model, value in stats_json["model"].items():
            if value < 2:
                continue
            model = model.replace(' ', '%20')
            g.add((URIRef("https://wiki.lineageos.org/devices/" + model), URIRef("https://wiki.lineageos.org/devices/schema#usage_stat"), Literal(value)))

get_devices()
get_stats()

with open(rdf_dump, 'w') as rdf_out:
    rdf_out.write("\n".join(sorted(set(g.serialize(format="ntriples").decode("utf-8").strip().split("\n")))))
