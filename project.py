from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, SportItem

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog/')
def catalogMenu():
  categories = session.query(Category).order_by(asc(Category.name))
  items = session.query(SportItem).order_by(asc(SportItem.id))
  return render_template('catalog.html', categories = categories, items = items)	


# Task 1: Create route for category here

@app.route('/catalog/<int:category_id>/items/')
def categoryMenu(category_id):
	categories = session.query(Category).order_by(asc(Category.name))
	items = session.query(SportItem).filter_by(category_id = category_id)
	return render_template('category.html', categories = categories, items = items)	

# Task 2: Create route for item description function here


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def itemMenu(category_id, item_id):
	item = session.query(SportItem).filter_by(id = item_id).one()
#return "page to show a category items. Task 1 complete!"
	return render_template('description.html', item = item)

# Task 3: Create a route for edit item function here

@app.route('/catalog/<int:category_id>/<int:item_id>/edit/')
def editItem(category_id, item_id):
    return "page to edit an item's description. Task 3 complete!"


# Task 4: Create a route for edit item function here

@app.route('/catalog/<int:category_id>/<int:item_id>/delete/')
def deleteItem(category_id, item_id):
    return "page to delete an item'. Task 4 complete!"


# Task 5: Create a route for edit item function here

@app.route('/catalog/add/')
def addItem():
    return "page to add a newitem'. Task 5 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

