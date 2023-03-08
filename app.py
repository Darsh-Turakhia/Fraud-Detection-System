#Imports
import json
import hashlib
from flask import Flask, render_template, request, jsonify
import mysql.connector
import card_validator
import mail
from datetime import datetime
app = Flask(__name__, template_folder='templates',static_folder='static')
flaggedCard = []


@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/', methods=['post','get'])
def validateTransaction():

    if request.method == 'POST':
        api = request.form['api']
        cardno = request.form['cardno']
        cvv = request.form['cvv']
        pin = request.form['pin']
        amt = request.form['amt']

    else:
        print("GET METHOD?")


    api_key = api

    query = "SELECT * FROM API_KEYS where api_key = (%s)"
    dbcursor.execute(query,(api_key,))
    result = dbcursor.fetchall()

    if len(result) == 0:
        return render_template('/Failure.html')
    else:
        print(result)
        api_owner = result[0][3]
        if(bufffer_api_key[api_key] < 10): #checking if the api key is not being brute forced
            card_number_test = str(cardno)
            card_number = hashlib.sha256(((str(cardno))+ ".0DhairyaDarshDhruvinPraful").encode()).hexdigest()
            query = "SELECT * FROM carddata where card_number = (%s)"
            dbcursor.execute(query, (card_number,))
            result = dbcursor.fetchall()

            if len(result) != 0:
                CVV_CVV2 = hashlib.sha256((str(cvv)+ ".0DhairyaDarshDhruvinPraful").encode()).hexdigest()
                Card_Pin = hashlib.sha256((str(pin)+ ".0DhairyaDarshDhruvinPraful").encode()).hexdigest()
                transact_amt = amt
                if CVV_CVV2 == result[0][4] and Card_Pin == result[0][7] and eval(transact_amt) <= eval(result[0][8]):

                    if eval(transact_amt) <= result[0][9]:
                        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        mail.send(result[0][10],"Transaction Successful",f"Transaction Successful for amount {transact_amt} on {time}\n for card number {card_number_test}")
                        print("Success")
                        return render_template('/Successfull.html')
                    else:
                        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        mail.send(result[0][10], "Verification needed",f"Verification needed for transaction of {transact_amt} on {time}\n"
                                                                      f"Call our agent to verify on +91-9925160602 For card number {card_number_test}")
                        print("Verification needed")
                        return render_template('/Failure.html')


                else:
                    bufffer_api_key[api_key] += 1
                    time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    mail.send(result[0][10],"Transaction Failed",f"Transaction Failed for amount {transact_amt} on {time}")
                    return render_template('/Failure.html')




            else:
                bufffer_api_key[api_key] += 1
                return "Invalid Card Number"
        else:
            time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print("Raise alert")
            mail.send(api_owner, "API KEY BANNED", f"MAX ATTEMPTS FOR API KEY REACHED on {time}")
            return render_template('/Failure.html')



if __name__ == '__main__':

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "dss"
    )
    dbcursor = mydb.cursor(buffered=True)
    print(mydb)
    bufffer_api_key = {}
    dbcursor.execute("SELECT * FROM API_KEYS")
    for i in dbcursor.fetchall():
        bufffer_api_key[i[1]] = 0
    app.debug = True
    app.run()
