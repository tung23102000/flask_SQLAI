
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'mtp'
api = Api(app)

 # phai them may dong o duoi neu ko se bi loi
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app,authenticate,identity) #/auth



api.add_resource(Item, '/item/<string:name>')     #http://127.0.0.1:5000/item/Rolf
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')     #http://127.0.0.1:5000/item/Rolf
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User,'/user/<int:user_id>')



if __name__ == '__main__':
 from db import db
 db.init_app(app)
 
 app.run(port=5000, debug=True)
