## Exchange app to PLN

from flask import Flask, request, render_template
import requests
import csv

app = Flask(__name__)


@app.route('/cur/', methods=['GET', 'POST'])
def currency_exercise():
    file = 'nazwa_pliku.csv' #csv file with currencies from nbp page

    if request.method == "GET":
        # download data and save as csv file - currencies from nbp page
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
        data = response.json()
        rates = data[0]['rates']
        fieldnames = ['currency', 'code', 'bid', 'ask']
        with open(file, 'w', newline='', encoding='utf-8') as csv_file:
            write = csv.DictWriter(csv_file, delimiter=';', fieldnames=fieldnames)
            write.writeheader()
            write.writerows(rates)

        #open currencies from csv file and iterate in currency_exercise.html template
        currency = []
        with open(file, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for i in reader:
                currency.append(i['code'])
        return render_template("currency_exercise.html", currency = currency)
    
    elif request.method == "POST":
        #taking data from form
        selected_currency = request.form.get('currency')
        amount_str = request.form.get('amount')

        if selected_currency and amount_str:
            try:
                amount = float(amount_str) #changing data to float variable
                with open(file, 'r', newline='', encoding='utf-8') as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=';')
                    for i in reader: #iterate to select correct currency and calculate the value
                        if i['code'] == selected_currency:
                            try:
                                ask_str = i['ask'].replace(',', '.')
                                ask = float(ask_str)
                                pln_exchange = amount * ask
                                return render_template('currency_exercise_after.html', result = f"Koszt {amount}{selected_currency} wynosi {pln_exchange:.2f}PLN")
                            except ValueError:
                                return render_template('currency_exercise_after.html', result = f"Błąd podczas konwersji")
                    return render_template('currency_exercise.html', result = f"Nie znaleziono wybranej waluty")
            except ValueError:
                return render_template('currency_exercise.html', result = f"Podaj poprawną kwotę")


if __name__ == '__main__':
    app.run(debug=True)