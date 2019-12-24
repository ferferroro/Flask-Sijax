from flask import Flask, render_template, request, g
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import flask_sijax
import os

# instantiate the app
app =  Flask(__name__)
app.config['SECRET_KEY'] = 'sekretolang'

# app config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# instantiate db
db = SQLAlchemy(app)

# sijax setup and config 
path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

# create model class
class TestTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80))

# create form
class myForm(FlaskForm):
    text = StringField('Search')
    submit = SubmitField('Submit')

# standard flask search route
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = myForm()

    # on start get all the records 
    if request.method == 'GET':
        results = TestTable.query.all()
        return render_template('index.html', form=form, results=results)

    # on submit click get all records that matches the search text data
    if request.method == 'POST':
        # get the text data from the html
        text = '%' + request.form['text'] + '%'
        # query using the text data
        results = TestTable.query.filter(TestTable.text.like(text)).all()
        # return html
        return render_template('index.html', form=form, results=results)

# sijax search route
@flask_sijax.route(app, '/search_sijax')
def search_sijax():

    # sijax function
    def sijax_search_function(obj_response, search_text):
        # obj_response.alert('Search text box value: ' + search_text)
        
        # get the text data from the html
        text = '%' + search_text + '%'
        # query using the text data
        results = TestTable.query.filter(TestTable.text.like(text)).all()

        # build response
        content = ''
        for result in results:
            content += '<tr>'
            content += '<td>' + str(result.id)  + '</td>'
            content += '<td>' + result.text  + '</td>'
            content += '</tr>'
        
        # replace html content
        obj_response.html('#test_body', content)
        
    
    # check if its sijax request
    if g.sijax.is_sijax_request:
        g.sijax.register_callback('sijax_search', sijax_search_function)
        return g.sijax.process_request()

    # normal rendering 
    form = myForm()
    # on start get all the records 
    if request.method == 'GET':
        results = TestTable.query.all()
        return render_template('index.html', form=form, results=results)

    # on submit click get all records that matches the search text data
    if request.method == 'POST':
        # get the text data from the html
        text = '%' + request.form['text'] + '%'
        # query using the text data
        results = TestTable.query.filter(TestTable.text.like(text)).all()
        # return html
        return render_template('index.html', form=form, results=results)

if __name__ == '__main__':
    app.run(debug=True)
