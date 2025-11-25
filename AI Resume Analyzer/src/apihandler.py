import json, webbrowser, http.client
from urllib.parse import quote
class APIHandler:
    def __init__(self):
        self.connection = http.client.HTTPSConnection("jsearch.p.rapidapi.com")
        self.headers = { 'x-rapidapi-key': "ef33a65e16msh5f5ae3dc94c29c2p1d65a3jsn4f04ffc646e9", 'x-rapidapi-host': "jsearch.p.rapidapi.com" }

    # Gets all job listings for the provided query (first) parameter
    def get_listings(self, query):
        query = quote(query)
        search_url = "/search?" + query + "&page=1&num_pages=1&country=us&date_posted=all"
        self.connection.request("GET", search_url, headers = self.headers)
        response = self.connection.getresponse()

        data = response.read()
        data = data.decode("utf-8")
        data = json.loads(data)

        if not "data" in data: return self.open_FailSafe()
        else: return data["data"]

    # In case the api dies, uses "fail_safe.txt" in the relative directory.
    def open_failsafe(self):
        with open("fail_safe.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["data"]

    # Opens a link directly
    def open_directlink(self, jobApplicationLink): webbrowser.open(jobApplicationLink)

    # Opens a related link from getListings response and job index
    def open_json(self, jobListingsJSON, jobIndex): webbrowser.open(jobListingsJSON[jobIndex]["job_apply_link"])



'''
# EXAMPLE PROGRAM
api = api_Handler()

response = api.get_Listings("developer jobs in chicago")

api.openDirectLink(response[1]["job_apply_link"])
'''
