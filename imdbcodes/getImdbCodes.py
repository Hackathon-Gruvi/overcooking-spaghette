import json
import requests
import re as regex

def getIMDBcode(url):
    response = requests.get(url)
    result = regex.findall('www.imdb.com/title/\w*', response.text)
    if len(result) > 0:
        return result[0][19:]
    return 'NA'


with open('top100wInfohash.json') as json_file:
    data = json.load(json_file)
    for movie in data:
        movie['imdb'] = getIMDBcode(movie['id'])

datafile = open('top100complete.json', 'w')
datafile.write(json.dumps(data))