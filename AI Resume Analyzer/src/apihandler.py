import os
import json
import json, webbrowser, http.client
from urllib.parse import quote
from xml.etree.ElementTree import tostring


class APIHandler:
    def __init__(self):
        self.connection = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
        self.headers = { 'x-rapidapi-key': "ef33a65e16msh5f5ae3dc94c29c2p1d65a3jsn4f04ffc646e9", 'x-rapidapi-host': "jsearch.p.rapidapi.com" }

    # Gets all job listings for the provided query (first) parameter
    def get_listings(self, query, amount = 1):
        results = []

        if amount > len(query): amount = len(query)

        for i in range(amount):
            thisQuery = quote(query[i].lower())
            search_url = "/search?query=" + thisQuery + "&page=1&num_pages=1&country=us&date_posted=all"
            self.connection.request("GET", search_url, headers = self.headers)
            response = self.connection.getresponse()

            data = response.read()
            data = data.decode("utf-8")
            data = json.loads(data)

            if "data" in data:
                for item in data["data"]:
                    results.append(item)
        print (results)
        if len(results) == 0:
            if not "data" in data: return self.open_failsafe()
            self.open_failsafe()

        return results


    # In case the api dies, uses "fail_safe.txt" in the relative directory.
    def open_failsafe(self):
        with open("fail_safe.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["data"]

    '''
    def open_failsafe(self):
    # Locate file relative to THIS file, not the working directory
        base_path = os.path.dirname(os.path.abspath(__file__))
        failsafe_path = os.path.join(base_path, "fail_safe.txt")

        print("Loading failsafe from:", failsafe_path)

        try:
            with open(failsafe_path, "r", encoding="utf-8") as f:
                text = f.read()
            return json.loads(text)
        except Exception as e:
            print("Failed to load fail_safe.txt:", e)
            return []
'''

    # Opens a link directly
    def open_directlink(self, jobApplicationLink): webbrowser.open(jobApplicationLink)

    # Opens a related link from getListings response and job index
    def open_json(self, jobListingsJSON, jobIndex): webbrowser.open(jobListingsJSON[jobIndex]["job_apply_link"])

'''
tempList = ["Python", "Java", "C++"]
str = ""
for i in tempList:
    str += i + " "

# EXAMPLE PROGRAM
api = APIHandler()

print(str)
response = api.get_listings(str)
print(response)
api.open_directlink(response[1]["job_apply_link"])
'''
