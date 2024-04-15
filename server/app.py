from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods=['GET', 'POST'])
def messages():
   
    # if to GET/POST
    if request.method == 'GET':
        
     # get the messeges ordered by id in ascending order
        messages = Message.query.order_by('created_at').all()
    # GET- list to dict then make reponse
        return make_response([message.to_dict() for message in messages],200 )

    # Post- make dict, add, commit the return the make response with the 200
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )
        #   add
        db.session.add(message)
        # commit
        db.session.commit()
        #  return the make response  to_dict with the 200
        return  make_response(message.to_dict(),  201,)


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # get the messange by id
    message = Message.query.filter_by(id=id).first()
     #  if PATCH loop though the object , use setattr(message, attr, assign), add, commit 
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
            
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(),200 )
   
    # if DEl delete and commit
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return make_response( {'deleted': True} , 200)
    # return the response in both
    pass








if __name__ == '__main__':
    app.run(port=5555)