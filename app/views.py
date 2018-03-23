from app import myapp
from flask import request, render_template, session, redirect, url_for, escape
import os
from pprint import pprint
from app import spotifyAPI
import urllib

# CLIENT_ID = '1a006043c49f417f9056ca176155891b'
CLIENT_ID = 'd07e28903b25490581ad3bea0004546e'
# CLIENT_SECRET = '4bb90711004f4513bac3a032278fc80e'
CLIENT_SECRET = '2a38bd1411af410a8764807b2f3290e2'
REDIRECT_URI = 'http://localhost:5000/spotify-token'
token = ''

# myapp.secret_key = os.urandom(24)

@myapp.route('/')
def index():
	# Look for the User's Access Key in session
	try:
		access_token = token['access_token']
		print
		print ('------- SPOTIFY ACCESS TOKEN:', access_token, '-------')
		print
		spotifyPlaylists = spotifyAPI.getSpotifyPlaylists(access_token)
		return render_template("myPlaylists.html", playlists=spotifyPlaylists['data'])
	# If Access Key not available, begin User OAuth flow by redirecting User to Spotify Auth URL with appropriate parameters per Spotify API docs
	except:
		print
		print ('------- USER API ACCESS KEY NOT FOUND! -------')
		print ('------- PROMPTING USER FOR SPOTIFY AUTHORIZATION -------')
		print
		return redirect('/connect-spotify')


@myapp.route('/connect-spotify')
def connectSpotify():
	# INSERT YOUR CODE HERE TO REDIRECT USER TO SPOTIFY AUTH PAGE & BEGIN AUTH FLOW
	return redirect('https://accounts.spotify.com/authorize/?'+\
		'client_id='+CLIENT_ID+\
		'&response_type=code'+\
		'&redirect_uri='+REDIRECT_URI+\
		'&scope=playlist-read-private%20playlist-read-collaborative')

@myapp.route('/spotify-token')
def spotifyToken():
	global token
	# GET CODE FROM REDIRECT URL
	code = request.args.get('code')
	# USE CODE TO GET AN ACCESS TOKEN FROM SPOTIFY API
	token = spotifyAPI.authorizeSpotify(code)
	# REDIRECT USER TO INDEX ONCE USER IS AUTHORIZED
	return redirect('/')

@myapp.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'), 404
