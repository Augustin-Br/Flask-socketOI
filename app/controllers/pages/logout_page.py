from flask import redirect, session

#delete the session of user
def logout():
    session['username'] = None
    return redirect('/')