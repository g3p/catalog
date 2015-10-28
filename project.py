from flask import Flask
from sqlalchemy import create_engine
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
    return "page to show the catalog"

# Task 1: Create route for category here

@app.route('/catalog/<int:category_id>/items/')
def categoryMenu(category_id):
    return "page to show a category items. Task 1 complete!"

# Task 2: Create route for item description function here


@app.route('/catalog/<int:category_id>/<int:item_id>/')
def itemMenu(category_id, item_id):
    return "page to show an item's description. Task 2 complete!"

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

