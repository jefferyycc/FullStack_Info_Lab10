from flask import session
import base64
import requests
from pprint import pprint

# CLIENT_ID_SECRET = b'1a006043c49f417f9056ca176155891b:4bb90711004f4513bac3a032278fc80e'
CLIENT_ID_SECRET = b'd07e28903b25490581ad3bea0004546e:2a38bd1411af410a8764807b2f3290e2'
# CLIENT_SECRET = '4bb90711004f4513bac3a032278fc80e'
REDIRECT_URI = 'http://localhost:5000/spotify-token'

def authorizeSpotify(code):
	code=code
	print ('-------- CODE ------------', code)
	data = {
	'grant_type': 'authorization_code',
	'code': code,
	'redirect_uri': REDIRECT_URI
	}

	# unencodedAuthHeader = CLIENT_ID+':'+CLIENT_SECRET
	encodedHeader = base64.b64encode(CLIENT_ID_SECRET)

	headers = {
	'Authorization': 'Basic ' + encodedHeader.decode('utf-8')
	}

	response = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
	decodedResponse = response.json()

	print
	print ('------- FULL REPONSE -------')
	print (response)

	print
	print ('------- SPOTIFY TOKEN RESPONSE -------')
	print (decodedResponse)
	print

	# SET USER SESSION WITH SPOTIFY ACCESS TOKEN & REFRESH TOKEN
	access_token = decodedResponse['access_token']
	refresh_token = decodedResponse['refresh_token']
	expires_in = decodedResponse['expires_in']

	responseToken = {}
	responseToken['access_token'] = access_token
	responseToken['refresh_token'] = refresh_token
	responseToken['expires_in']	= expires_in
	print
	print ('------- RESPONSE TOKEN -------')
	print (responseToken)
	print
	return (responseToken)

def getSpotifyPlaylists(access_token):
	# Initialize an object in which to store playlist data
	playlistsObj = {'data': []}

	# Set API headers
	headers = {
	'Authorization': 'Bearer ' + access_token
	}

	# Set API params
	params = {
		'limit': 50
	}

	# API endpoint
	endpoint = 'https://api.spotify.com/v1/me/playlists'

	# Call API
	try:
		response = requests.get(endpoint, params=params, headers=headers)
		decodedResponse = response.json()
		print ('------- FULL DECODED RESPONSE -------')
		pprint(decodedResponse)

		for playlist in decodedResponse['items']:
			tempPlaylist = {}
			tempPlaylist['name'] = playlist['name']
			try:
				tempPlaylist['image'] = playlist['images'][0]['url']
			except:
				tempPlaylist['image'] = ''
			tempPlaylist['tracksUrl'] = playlist['tracks']
			playlistsObj['data'].append(tempPlaylist)
			#print tempPlaylist
		return playlistsObj

	except Exception as e:
		print
		print ('------- ERROR GETTING PLAYLIST DATA FROM SPOTIFY API -------', e)
		print
