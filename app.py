from flask import Flask, render_template, request, redirect, url_for, \
    session, make_response, flash


app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/user_id/<int:user_id>')
def ser_id(user_id):
    return f'The user id is {user_id}'


@app.route('/')
@app.route('/<name>')
def index(name=None):
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    resp = make_response(render_template('translator/index.html', name=name))
    resp.set_cookie('test', 'test_cookie')
    return resp


@app.route('/see_cookie')
def see_cookie():
    return {
        'cookie': request.cookies.get('test')
    }


@app.route('/translator')
def translator():
    if 'username' in session:
        return render_template('translator/translator.html', name=session['username'], logout='true')
    return 'You are not logged yet'


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if len(request.form['username']) < 4 or len(request.form['password']) < 8:
            error = 'Invalid username/password'    
        else:
            flash('You were successfully logged in')
            session['username'] = request.form['username']
            return redirect(url_for('translator'))
    return render_template('translator/login.html', error=error), 400


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))
