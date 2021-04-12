# Movie Coast Guard

## Context


## Team
| Name | GitHub | Linkedin |
| ---- | ------ | -------- |
| Andreia Gouveia | https://github.com/AndreiaGouveia | https://www.linkedin.com/in/andreia-gouveia/ |
| Carlos Albuquerque | https://github.com/CajoAlbuquerque | |
| Carlos Duarte | https://github.com/carlosnovaduarte | https://www.linkedin.com/in/carlosnovaduarte/ |
| Sofia Lajes | https://github.com/SALajes | https://www.linkedin.com/in/salajes/ |

## Problem
Piracy in the movie industry has been steadily increasing, and there are not many tools available for tracking, control and statistics regarding it.

## Goals
1. Gather information from torrents, including their peers, and subsequently their consumption patterns
2. Compare with relevant values such as the movie’s production budget and box office
3. Create a timeline

## Approach
1. Get the top 100 most torrented movies and extract relevant info (info hash, seeders and their IPs, geographical location)
2. Gather relevant info from movie titles the user provided
3. Build a dataset with aforementioned information
4. Cross reference with the information that was previously gathered and the OpusData dataset and try to answer the questions: 

    - What makes a movie more likely to be pirated? 
    - What is the impact of piracy in the movie industry?


## Top 100

This component uses an API to fetch the top 100 most torrented movies.

In order to update the list, run:

`docker build -t pirate-bay thepiratebay`

`docker container run -e "BASE_URL=https://thepiratebay.asia/" -p 5000:5000 --name pirateBay pirate-bay`

`curl -G http://localhost:5000/top/201/ >> top100.json`

More informations in the original repository for this source: https://github.com/appi147/thepiratebay


None of the content in the folder thepiratebay is made by us, credit to the author: appi147


**Important**: be sure that the top 100 file is named 'top100.json' and is to be found in the root of the repository.

## Movies to track
Usually the movies that are released take some time to be pirated, therefore, we suggest you create json objects - with the movie query (to be search in the SearchTorrentAPI) and its IMDB code - on the file 'moviesToTrack.json'.

## Torrents
In the torrents folder there is a javascript file that has functions divided in two components:

- The top 100: adds information (infohash, trackers and name) about each torrent in the 'top100.json' and stores it in a file named 'top100wInfohash.json'
- Movies to track: fetches torrents and adds information (infohash, trackers and name) about each for each of the movies in 'moviesToTrack.json' and stores it in a file named 'moviesToTrackTorrents.json'

## IMDB codes
In order to compare the information we gathered to OpusData dataset and reach conclusions, it is necessary to retrieve the IMDB codes.

For the movies to track this information is expected to be given beforehand.

For the top 100, it is necessary to curl the torrent's download web page and retrieve the imdb code (when it exists).

## Peers
Given the infohash we retrieve the peers' IP addresses and, subsequently, their geolocation. This will be used, in the future, to find patterns of movie torrents consumption by regions.

We are aware that some of the peers might be using VPN and therefore the geolocation of the peers might not be absolutely accurate.

## Data science
Cross reference with the information that was previously gathered and the OpusData dataset and try to answer the questions.
