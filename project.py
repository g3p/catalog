from flask import Flask, render_template, request,\
 redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, SportItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog-app"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        login_session['credentials'] = credentials.access_token
        print "1 ", credentials
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token

    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    print "stored_credentials", stored_credentials
    stored_gplus_id = login_session.get('gplus_id')
    print "stored_gplus_id", stored_gplus_id
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user'
                                            'is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    '150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    print credentials

    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('catalogMenu'))
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/categories.json')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/items.json')
def categoryItemsJSON():
    items = session.query(SportItem).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/')
@app.route('/catalog/')
def catalogMenu():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(SportItem).order_by(desc(SportItem.id))
    if 'username' not in login_session:
        return render_template('catalog.html',
                               categories=categories, items=items)
    else:
        return render_template('catalog_logged_in.html',
                               categories=categories, items=items)

# Task 1: Create route for category here


@app.route('/catalog/<int:category_id>/items/')
def categoryMenu(category_id):
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(SportItem).filter_by(category_id=category_id)
    return render_template('category.html', categories=categories, items=items)

# Task 2: Create route for item description function here


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def itemMenu(category_id, item_id):
    item = session.query(SportItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template('description.html', item=item)
    else:
        return render_template('description_logged_in.html', item=item)


# Task 3: Create a route for edit item function here

@app.route('/catalog/<int:category_id>/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    editedItem = session.query(SportItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        # edit item's name
        if request.form['name']:
            editedItem.name = request.form['name']
            flash('Item Successfully Edited: %s' % editedItem.name)
        #edit item's description
        if request.form['description']:
            editedItem.description = request.form['description']
            flash('%s description Successfully Edited.' % editedItem.name)
        session.commit()
        return redirect(url_for('catalogMenu'))
    else:
        return render_template('editItem.html', item=editedItem)

# Task 4: Create a route for delete item function here


@app.route('/catalog/<int:category_id>/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    itemToDelete = session.query(
            SportItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        # delete selected item, itemToDelete, from database
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.name)
        session.commit()
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)


# Task 5: Create a route for add item function here

@app.route('/catalog/add/', methods=['GET', 'POST'])
def addItem():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    else:
        if request.method == 'POST':
            newItem = SportItem(name=request.form['name'],
                                description=request.form['description'],
                                category_id=request.form['category'])
            session.add(newItem)
            flash('New Item %s Successfully Created' % newItem.name)
            session.commit()
            return redirect(url_for('catalogMenu'))
        else:
            categories = session.query(Category).order_by(asc(Category.name))
            return render_template('newItem.html', categories=categories)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='0.0.0.0', port=5000)
