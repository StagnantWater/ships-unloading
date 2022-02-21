import json
from flask import Flask, render_template, session
from scenario_query.routes import query_app
from scenario_auth.routes import auth_app
from scenario_edit.routes import edit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'T0P$ECR3T'
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['DB_CONFIG'] = json.load(open('configs/db_config.json'))
app.register_blueprint(query_app, url_prefix='/query')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(edit, url_prefix='/edit')


@app.route('/')
def menu():
    session['group_name'] = session.get('group_name', 'unauthorized')
    return render_template('menu.html', group=session['group_name'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
