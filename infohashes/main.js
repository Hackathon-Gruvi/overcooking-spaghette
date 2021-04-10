const TorrentSearchApi = require('torrent-search-api');
const parseTorrent = require('parse-torrent')

// Get providers
const providers = TorrentSearchApi.getProviders();
 
// Get active providers
const activeProviders = TorrentSearchApi.getActiveProviders();
 
// Enable public providers
TorrentSearchApi.enablePublicProviders();

const getTorrents = (async ()=>{
    return TorrentSearchApi.search('Endgame', 'Movies', 20)
        .then((torrents) => {
            console.log(torrents[0])
            return torrents[0]
        })
        .then(async (torrent) => {
            const magnetLink = torrent.magnet;
            const torrentDetails = parseTorrent(magnetLink);
            console.log(torrentDetails)
            return torrentDetails.infoHash
        })
        .then((infohash)=>{
            console.log(infohash)
        })
        .catch((error)=>{
            console.log(error)
        })
})

getTorrents();