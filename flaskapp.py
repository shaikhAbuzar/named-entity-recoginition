import wikipediaapi
import spacy
import jwt
from datetime import datetime, timedelta
from spacy import displacy
from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anadleagnrgunsjrnlgajnJNFRLGNJlJLJNAJENJJKnfjengjkrsnr'


def token_required(function):
	@wraps(function)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		# print('TOKEN:', token)

		if not token:
			return jsonify({'msg': 'Token is missing'})

		try:
			data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
		except Exception as e:
			print('EXCEPTION:', e)
			return jsonify({'msg': 'Token is invalid'})

		return function(*args, **kwargs)
	return decorated


@app.route('/perform-ner', methods=['POST'])
@token_required
def perform_ner():
	topic = request.args.get('topic')
	if topic is None or len(topic) <= 0:
		return jsonify({
			'message': 'Unable to find the topic in url'
		})
	else:
		wiki_wiki = wikipediaapi.Wikipedia(
			language='en',
			extract_format=wikipediaapi.ExtractFormat.WIKI
		)

		# get the page
		page = wiki_wiki.page(topic)

		# check if the page exists
		if page.exists():
			# text from the page
			text = page.text

			# create the nlp object for ner
			nlp = spacy.load('en_core_web_sm')
			# return the result of the ner in the markdown format
			# through the api
			return displacy.render(nlp(text), style='ent')
		else:
			return jsonify({'Message': 'Page not found'})


@app.route('/login', methods=["POST"])
def login():
	auth = request.authorization
	# we are using a temporary implementation of the token for the
	# implementation, though in real world scenarios the password will
	# be fetched from database via username, and then password will be
	# verified and the further process will happen
	if auth and auth.password == 'Password':
		# The token is generated from the username and the secret key of our app
		# the expiration period of our token is set to 30 minutes
		token = jwt.encode(
			{'user': auth.username, 'exp': datetime.utcnow() + timedelta(minutes=30)},
			app.config["SECRET_KEY"],
			algorithm='HS256'
		)
		# return the token
		return jsonify({'token': token})
	# if the passwords didn't match
	return jsonify({
		'msg': 'Invalid Password or missing'
		'the field is required field'
	})


if __name__ == '__main__':
	app.run(threaded=True)
