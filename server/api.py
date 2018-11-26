from flask import Flask, request
import json
import requests

app = Flask(__name__)

"""
Takes in a json. Example:
{
"keywords": "Java, AWS",
"location": "New York",
"full-time": "true"
}
"""
@app.route('/searchJobs/', methods=['POST'])    
def search_jobs():
    if not request.json:
        abort(400)

    # Base
    URL = "https://jobs.github.com/positions.json?"

    # If a category doesn't have an input, 
    # assuming the front end will continue
    # substituting the value with an empty string,
    # the Job API handles it perfectly. 
    # Ex: these two requests have the same output:
    #
    # https://jobs.github.com/positions.json?location=new+york
    # https://jobs.github.com/positions.json?description=&location=new+york
    #
    # This means we can just throw inputs into an very simple URL generator
    # because it won't matter if the values are present or not
    
    keywords = request.json['keywords']
    location = request.json['location']
    fulltime = request.json['full-time']

    # Replace spaces with '+' and add url syntax
    if (', ' in keywords):
        location.replace(', ', '+')
    description = "description=" + keywords

    if (' ' in location):
        location.replace(' ', '+')
    location = "&location=" + location

    fulltime = "&full_time=" + fulltime.upper()

    # Build URL
    URL += description + location + fulltime
    #print(URL)

    # Sending get request and saving the response as response object
    r = requests.get(url=URL)
    data = r.json()

    # We're giving everything to the front end
    return json.dumps(data)


# run the Flask app (which will launch a local webserver)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)