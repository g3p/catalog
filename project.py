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
	return render_template('description.html', item = item)

# Task 3: Create a route for edit item function here

@app.route('/catalog/<int:category_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem= session.query(
        SportItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            flash('Item Successfully Edited: %s' % editedItem.name)            
        if request.form['description']:
            editedItem.description = request.form['description']
            flash('%s description Successfully Edited.' % editedItem.name)
        return redirect(url_for('catalogMenu'))

    else:
        return render_template('editItem.html', item=editedItem)    


# Task 4: Create a route for delete item function here

@app.route('/catalog/<int:category_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    itemToDelete = session.query(
        SportItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.name)
        session.commit()
        return redirect(url_for('categoryMenu', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)



# Task 5: Create a route for edit item function here

@app.route('/catalog/add/', methods=['GET', 'POST'])
def addItem():
    if request.method == 'POST':
        newItem = SportItem(name=request.form['name'], description=request.form['description'], category_id=request.form['category'])
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.name)
        session.commit()
        return redirect(url_for('catalogMenu'))
    else:
    	categories = session.query(Category).order_by(asc(Category.name))    	
    	return render_template('newItem.html', categories = categories)    


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.debug = True
    app.run(host='0.0.0.0', port=5000)