# Movie Coast Guard

## Context
This project was developed within 16 hours for [NIAEFEUP](https://ni.fe.up.pt/)'s Hackathon with [Gruvi](https://www.gruvi.tv/), on the weekend of the 10th and 11th of April 2021.

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
1. Get the top 100 most torrented movies 
2. Allow the user to insert movies to track manually given a query to search for matching torrents
3. Extract relevant info about each torrent found, such as:
- infohash (unique identifier)
- seeders and peers
- date of publish
- trackers
- IMDB code
4. Build a dataset with aforementioned information.
5. Extract legal information about the film, such as its budget, release dates, box office, etc.
6. Cross reference with the information that was previously gathered and the OpusData dataset and try to answer the questions: 

    - What makes a movie more likely to be pirated? 
    - What is the impact of piracy in the movie industry?

This aims to create a **snapshot** of the state of piracy in that moment.

## Architecture and information flow
![Architecture and information flow](https://user-images.githubusercontent.com/38894031/114429239-09c19700-9bb5-11eb-8a22-656c230a74c0.png)

### The user
- Can use ThePirateBayAPI to fetch the current top 100 most torrented movies (as explained in the next section) and save it in 'top100.json' file. Instead of getting the top 100, the user could resort to any other kinds of APIs that returns torrents as objects, for as long as those objects have a magnet link and a link to the torrent's webpage (in order to get the imdb code).
- Can indicate movies to keep track on various torrent providers in 'moviesToTrack.json'.

### Torrents module
- For the moviesToTrack.json, since only the query to find torrents is provided, first, it is necessary to use an API to search for torrents for each movie. In this project, we resort to the node package [TorrentSearchAPI](https://www.npmjs.com/package/torrent-search-api), eventhough the query system used by it has limitations. Secondly, parse the torrent to retrieve the infohash using the node package [parse-torrent](https://www.npmjs.com/package/parse-torrent).
- For the top100.json, since the file already has torrents, it is only needed to parse them and store their infohashes.

### IMDB code module
- Retrieve a torrent's IMDB code by curling and querying its webpage (some torrents have the imdb code to the movie, which is a way to ensure that it refers to the movie we are searching for).

### Peers module
Given the infohash we retrieve the peers' IP addresses and, subsequently, their geolocation. This will be used, in the future, to find patterns of movie torrents consumption by regions.

We are aware that some of the peers might be using VPN and therefore the geolocation of the peers might not be absolutely accurate.

**Important:** we do not intend to store IP addresses, but rather their geolocation. 

### Datascience module
The information retrieved by the previous modules regards torrents and their peers' geolocation. This module cross-references all the information with a dataset.

Finally, the information is presented and ready to use by the user.

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

## Dataset
During the Hackathon we used a OpusData dataset (process disclosed in the 'datascience' module), the conclusion were not very decisive since we did not have information about most movies in the top 100 (the data was not up-to-date).

A good dataset should have the following characteristics about movies, among other:
    - Name
    - Release dates
    - Genre
    - Production Budget
    - Box office
    - IMDB code 

A good dataset should also be continuously updated with information about movies, specially movies to be released or recently release, that way it would be possible to start collecting data as soon as possible in order to observe the variations of piracy in the first days, weeks and months of the movie's release.

Another great idea is to collect data about the price of movie tickets, dvds and blu-rays and calculate the financial damage of gross loss caused by piracy. In this project, we used a dataset that contained the average price for a movie ticket in every country.

## Possible issues
### VPN
The conclusions may not be accurate due to the fact that some users might be using VPNs

### Downloaded != Viewed
There’s no way to ensure that a user has actually seen what they downloaded. It is only possible to know if the peer finished downloading the torrent (thus becoming a seeder). Using the same logic, a single download can be shared with/seen by multiple users.

### Counting the exact number of downloads
It is only possible to take into consideration users that are either downloading the torrent, or have finished downloading it and are still seeding it

### Average Movie Ticket Price
The database that we found has data from 2014

### Lack of data
Specially for recent movies

## Future work
### Periodically running server:
- Make our code run periodically and store data about each torrent, in order to create a timeline
- Count the number of distinct seeders of each torrent to get the total number of downloads

This would allow us to create a timeline by registering the evolution of piracy and reach stronger conclusions.

### Cross reference location:
- Cross our data with the locations we found
- Due to lack of time we could not measure downloads per location and, subsequently, their impact
