import xml.etree.ElementTree as ET
from requests import get
from datetime import datetime
import sys

# private data! DO NOT PUSH
URL = 'YOUR_URL'
LOGIN = 'YOUR_LOGIN'
PASSWORD = 'YOUR_PW'

LOCATIONS = {
    "hauptmensa": "3.500"
}

TYP = {
    "essen1": "500",
    "essen2": "505",
    "aktionsstand": "535"
}

def get_local_mealplan():
    with open(sys.argv[1], 'r') as file:
        return " ".join(file.readlines())

def get_mealplan():
    return get(URL, auth=(LOGIN, PASSWORD)).text

def parse_mealplan(xml_string):
    root = ET.fromstring(xml_string)[1]

    def row_filter(row):
        rules = [
            row.get("ORT") == LOCATIONS["hauptmensa"],
            row.get("DATUM") == '{0:%d.%m.%Y 00:00}'.format(datetime.now()),
            row.get("TYP") in TYP.values(),
            row.get("AUSGABETEXT") != "Theke geschlossen",
        ]
        return all(rules)

    return list(filter(row_filter, root.findall('ROW')))



if __name__ == '__main__':
    mealplan = get_local_mealplan() if len(sys.argv) > 1 else get_mealplan()

    result = parse_mealplan(mealplan)

    print("\n".join([row.get("AUSGABETEXT").strip() for row in result]))
