from flask import Flask,Blueprint,request
from .validation import processPaymentValidation
from datetime import datetime
api_function_v1 = Blueprint('api_function_v1',__name__)



def processPayment():
    response = {"status":"","message":"","error":""}
    try:
        data = request.get_json()
        try:
            validate_data = {"CreditCardNumber":data['CreditCardNumber'],
                             "ExpirationDate":data['ExpirationDate'],
                             "SecurityCode":data['SecurityCode'] if 'SecurityCode' in data else "",
                             "Amount": data['Amount']
            }
            processPaymentValidation().load(data)
            currentDate = datetime.now()
            creditcardnumber = int(data['CreditCardNumber'])
            expirationDate = datetime.strptime(data['ExpirationDate'],"%Y/%m/%d")
            if len(data['CreditCardNumber'])<12:
                raise Exception('Credit Card Digit Is Not Valid')
            if expirationDate<currentDate:
                raise Exception('Expiration Date Is Not Valid')
            if data['Amount']<=0:
                raise Exception('Amount should be greater than 0')
            if 'SecurityCode' in data and data['SecurityCode']!='':
                securitycode = data['SecurityCode']
                if len(data['SecurityCode'])>3 or len(data['SecurityCode'])<3:
                    raise Exception('Security code is not valid')
        except Exception as e:
            response['status'] = 400
            response['message'] = 'bad Request'
            response['error'] = e.__str__()
            return  response
        if data['Amount']<20:
            print('call CheapPaymentGateway Function')
            response['status']=200
            response['message']='Payment is processed'
        elif data['Amount']>20 and data['Amount']<501:
            print('call ExpensivePaymentGateway')
            # if ExpensivePaymentGateway status is not success then call CheapPaymentGateway function
            response['status'] = 200
            response['message'] = 'Payment is processed'
        elif data['Amount']>500:
            print('call PremiumPaymentGateway')
            count = 1
            # if PremiumPaymentGateway status failed then increase the count with +1 and make payment until count>3
            response['status'] = 200
            response['message'] = 'Payment is processed'
    except Exception as e:
        response['status'] = 400
        response['message'] = 'bad Request'
        response['error'] = e.__str__()
    return response


api_function_v1.add_url_rule('/process-payment','processPayemnt',processPayment,methods=['POST'])