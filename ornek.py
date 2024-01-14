from flask import Flask, request

from flask_restful import Api, Resource

import pandas as pd

import requests





app = Flask(__name__)

api = Api(app)


class Users(Resource):
   def get(self, sayi):
            sayi_int = int(sayi)
            if sayi_int % 2 == 0 or sayi_int %3 == 0:
                url = "https://meowfacts.herokuapp.com/?count=" + sayi
                response = requests.get(url)
                data = response.json()
                return {'data': data['data']}, 200
            else:          
                return {'message': 'Error:Please enter multiples of 2 or 3 '}, 400

   def post(self):

       name = request.args['name']

       age = request.args['age']

       city = request.args['city']



       req_data = pd.DataFrame({

           'name'      : [name],

           'age'       : [age],

           'city'      : [city]

       })

       data = pd.read_csv('kullanici.csv')

       #data = pd.concat([data, req_data], ignore_index=True)

       data = data.append(req_data, ignore_index=True)

       data.to_csv('kullanici.csv', index=False)

       return {'message' : 'Record successfully added.'}, 201





class Name(Resource):

   def get(self,name):

       data = pd.read_csv('kullanici.csv')

       data = data.to_dict('records')

       for entry in data:
              
           if entry['name'] == name :

               return {'data' : entry}, 200

       return {'message' : 'No entry found with this name !'}, 400


class CITY(Resource):

   def get(self,city):

       data = pd.read_csv('kullanici.csv')

       data = data.to_dict('records')

       for entry in data:

           if entry['city'] == city:

               return {'data' : entry}, 200

       return {'message' : 'No entry found with this city !'}, 400



api.add_resource(CITY, '/province/<string:city>')

api.add_resource(Users, '/users/<string:sayi>')

api.add_resource(Name, '/isim/<string:name>')





if __name__ == '__main__':

   app.run(host="0.0.0.0", port=5000)

   app.run()



