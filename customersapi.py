from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime, date

app = Flask(__name__)
api = Api(app)

customers = []

class Customer(Resource):

    def get(self, id):
        for cust in customers:
            if cust['id'] == id:
                return {'data': cust}
        return {'data': None}


    def delete(self, id):
        for index, cust in enumerate(customers):
            if cust['id'] == id:
                customers.pop(index)
                return {'message': 'Deletado com sucesso!'}
        return {'data': None}
    
    def put(self, id):
        request_data = request.get_json()
        for index, cust in enumerate(customers):
            if cust['id'] == id:
                cust = request_data
                customers[index] = cust
                return {'data': cust}
        return {'data': None}


class CustomerList(Resource):

    def get(self):
        args = request.args
        if "month" in args:
            month = int(args.get("month"))
            if "day" in args:
                day = int(args.get("day"))
                birthday_list = []
                for cust in customers:
                    birth_date = datetime.strptime(cust['birth_date'], '%d-%m-%Y')
                    if birth_date.day == day and birth_date.month == month:
                        birthday_list.append(cust)
                return {'data': birthday_list}
        return {'data': customers}
    
    def post(self):
        request_data = request.get_json()
        cust = {
            'id': len(customers) + 1,
            'name': request_data['name'],
            'birth_date': request_data['birth_date']
        }
        customers.append(cust)
        return {'data': cust}


api.add_resource(Customer, '/customers/<int:id>')
api.add_resource(CustomerList, '/customers')

if __name__ == '__main__':
    app.run(debug=True)
