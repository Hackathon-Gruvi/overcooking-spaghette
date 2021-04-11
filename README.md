# overcooking-spaghette

## Top 100

In order to update the list of the top 100 most torrented movies, run:

docker build -t pirate-bay thepiratebay
docker container run -e "BASE_URL=https://thepiratebay.asia/" -p 5000:5000 --name pirateBay pirate-bay

curl -G http://localhost:5000/top/201/ >> top100.json

More informations in the original repository for this source: https://github.com/appi147/thepiratebay

None of the content in the folder thepiratebay is made by us, credit to the author: appi147

## 