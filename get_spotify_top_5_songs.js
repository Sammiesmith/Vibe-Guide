// Authorization token that must have been created previously. See : https://developer.spotify.com/documentation/web-api/concepts/authorization
const token = 'BQB1bbT6vsEpiALGOSSDzgGNCvE12lgWVRQem8ncjzCgZRmsgmMyr1S9W06TrHX1WSCiB6mOn21TH39B2llagXB8vhdrfcYa4jO3lFNFvZqjKsmZgEJHf0lCXxa8yefIRzRRhbQG7oFfY3jYAJxoiqcL-9UQ2j5GSizB5bFZTMTrQeWMBwuBJ-4RWJTeBEWSpwG2jepu8N7lg9a7OeoGdjj291h8gPoDfC2oVrhfrflnBQbyEnRBT9A3Hg0BqiBzM_WisiWTI9kls8NTXd4j-HsF1tgZIWc6fzylJYdR2OHbov7miGwbFaBPcF8iPYoSGXrd';
async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

async function getTopTracks(){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
  return (await fetchWebApi(
    'v1/me/top/tracks?time_range=long_term&limit=10', 'GET'
  )).items;
}

const topTracks = await getTopTracks();
console.log(
  topTracks?.map(
    ({name, artists}) =>
      `${name} by ${artists.map(artist => artist.name).join(', ')}`
  )
);