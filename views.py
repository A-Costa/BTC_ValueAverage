from flask import render_template, request, redirect
import MySQLdb, re, time
from BTC_ValueAverage import app

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method=='GET':
        return render_template("insert.html", date = time.strftime("%Y-%m-%d"))
    else:
        DataPattern = re.compile("^20(1[6-9]|[2-9][0-9])-[0-1]?[0-9]-[0-3]?[0-9]$")
        NumPattern = re.compile("^[0-9]{1,2}(($)|\.[0-9]{1,8}$)")
        PricePattern = re.compile("^[0-9]{1,6}(($)|\.[0-9]{1,4}$)")

        in_Data = request.form['Data']
        in_Num = request.form['N_BTC']
        in_Price = request.form['Price_BTC']

        if NumPattern.match(in_Num) and PricePattern.match(in_Price) and DataPattern.match(in_Data):
            conn = MySQLdb.connect("localhost", "root", "toor", "BTC_Value_Average")
            c = conn.cursor()
            query = "INSERT INTO Acquisti(Data, Btc_Acquistati, Prezzo_BTC) VALUES(\"" + in_Data + "\", " + in_Num + ", " + in_Price + ")"
            c.execute(query)
            conn.commit()
            conn.close()
            return render_template("print.html", rows = [('#',in_Data,in_Num,in_Price)])
        else:
            return redirect("/error")

@app.route('/amount', methods=['GET', 'POST'])
def amount():
    if request.method=='GET':
        return render_template("amount.html")
    else:
        PricePattern = re.compile("^[0-9]{1,6}(($)|\.[0-9]{1,4}$)")
        in_Value = request.form['Value']

        if PricePattern.match(in_Value):
            conn = MySQLdb.connect("localhost", "root", "toor", "BTC_Value_Average")
            c = conn.cursor()
            c.execute("SELECT MAX(id) FROM Acquisti")

            w = c.fetchone()[0]

            if w:
                week = float(w) + 1

                c.execute("SELECT SUM(Btc_Acquistati) FROM Acquisti")
                tot = float(c.fetchone()[0])

                ValorePosseduto = float(in_Value)*tot
                ValoreRichiesto = week*100

                result = (ValoreRichiesto - ValorePosseduto)/float(in_Value)
                conn.close()
                return render_template("amount_result.html", result = result)
            else:
                conn.close()
                return redirect("/error")
        else:
            return redirect("/error")


@app.route('/print')
def printTable():
    conn = MySQLdb.connect("localhost", "root", "toor", "BTC_Value_Average")
    c = conn.cursor()
    c.execute("SELECT id, Data, Btc_Acquistati, Prezzo_BTC FROM Acquisti")
    rows = c.fetchall()
    if rows:
        c.execute("SELECT SUM(Btc_Acquistati) FROM Acquisti")
        tot = c.fetchone()[0]
        c.execute("SELECT Prezzo_BTC FROM Acquisti WHERE id = (SELECT MAX(id) from Acquisti)")
        price = c.fetchone()[0]
        c.execute("SELECT SUM(Btc_Acquistati * Prezzo_BTC) FROM Acquisti")
        spent_euro = c.fetchone()[0]
        conn.close()
        return render_template("print_tot.html", rows = rows, tot = tot, value = "{:.2f}".format(price*tot), spent_euro="{:.2f}".format(spent_euro))
    else:
        conn.close()
        return redirect("/error")

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method=='GET':
        return render_template("reset.html")
    else:
        if request.form['Confirm'] == 'RESET':
            conn = MySQLdb.connect("localhost", "root", "toor", "BTC_Value_Average")
            c = conn.cursor()
            c.execute("DELETE FROM Acquisti")
            conn.commit()
            c.execute("ALTER TABLE Acquisti AUTO_INCREMENT = 1")
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            return redirect("/error")

@app.route('/incomecalc', methods=['GET', 'POST'])
def incomecalc():
    if request.method=='GET':
        return render_template("amount.html")
    else:
        PricePattern = re.compile("^[0-9]{1,6}(($)|\.[0-9]{1,4}$)")
        in_Value = request.form['Value']
        if PricePattern.match(in_Value):
            conn = MySQLdb.connect("localhost", "root", "toor", "BTC_Value_Average")
            c = conn.cursor()
            c.execute("SELECT SUM(Btc_Acquistati) FROM Acquisti")
            tot_btc_acquistati = c.fetchone()[0]
            c.execute("SELECT SUM(Btc_Acquistati * Prezzo_BTC) FROM Acquisti")
            spent_euro = c.fetchone()[0]
            conn.close()

            guadagno = (float(tot_btc_acquistati)* float(in_Value)) - float(spent_euro)
            return render_template("amount_result.html", result = "{:.2f}".format(guadagno))
        else:
            return redirect("/error")




@app.route('/error')
def error():
    return render_template("error.html")
