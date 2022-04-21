from app import create_app, socketio
from app.models.Users import db

app = create_app(debug=True)

@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':

    socketio.run(app, host='127.0.0.1', port=1664)