# overcooking-spaghette

## Top 100

This component uses an API to fetch the top 100 most torrented movies.
In order to update the list, run:

docker build -t pirate-bay thepiratebay
docker container run -e "BASE_URL=https://thepiratebay.asia/" -p 5000:5000 --name pirateBay pirate-bay

curl -G http://localhost:5000/top/201/ >> top100.json

More informations in the original repository for this source: https://github.com/appi147/thepiratebay

None of the content in the folder thepiratebay is made by us, credit to the author: appi147

Important: be sure that the top 100 file is named 'top100.json' and is to be found in the root of the repository.

## Torrents
In the torrents folder there is a javascript file that has functions divided in two components:
    - The top 100: adds information (infohash, trackers and name) about each torrent in the 'top100.json' and stores it in a file named 'top100wInfohash.json'
    - Movies to track: fetches torrents and adds information (infohash, trackers and name) about each for each of the movies in 'moviesToTrack.json' and stores it in a file named 'moviesToTrackTorrents.json'

## 