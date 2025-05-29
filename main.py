from collections import defaultdict
from flask import Flask, render_template, request
import pymysql.cursors



app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/calendario')
def calendario():
    connection = pymysql.connect(
        host="138.41.20.102",
        port=53306,
        user="caforio",
        password="studente",
        database="5bi_2025"
    )
    cursor = connection.cursor()
    sql = "SELECT l.data, l.luogo, a.argomento FROM lezioni_corso_competive_programming l INNER JOIN attivita_corso_competive_programming a ON l.id = a.idl ORDER BY l.data, a.id"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()

    # Raggruppa le attività per (data, luogo)
    grouped = defaultdict(list)
    for data, luogo, argomento in result:
        grouped[(data, luogo)].append(argomento)

    # Prepara la lista finale da passare al template
    final_result = [
        (data, luogo, "<br>".join(attivita_list))
        for (data, luogo), attivita_list in grouped.items()
    ]

    return render_template("calendario.html", result=final_result)

@app.route('/elencotutor')
def elencotutor():
    connection = pymysql.connect(
        host="138.41.20.102",
        port=53306,
        user="caforio",
        password="studente",
        database="5bi_2025"
    )
    cursor = connection.cursor()
    sql = "select idl, nome, cognome, ruolo from docenti_corso_competive_programming inner join tenute_da_corso_competive_programming on docenti_corso_competive_programming.id=tenute_da_corso_competive_programming.idd inner join lezioni_corso_competive_programming on tenute_da_corso_competive_programming.idl=lezioni_corso_competive_programming.id order by lezioni_corso_competive_programming.id"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return render_template("tutor.html", result=result)


@app.route('/formselzioneargomentitutor')
def formselzioneargomentitutor():
    connection = pymysql.connect(
        host="138.41.20.102",
        port=53306,
        user="caforio",
        password="studente",
        database="5bi_2025"
    )
    cursor=connection.cursor()
    sql="SELECT DISTINCT cognome FROM docenti_corso_competive_programming GROUP BY cognome"
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    return render_template("formselzioneargomentitutor.html", result=result)


@app.route('/stampaselezioneargomentitutor', methods=('POST',))
def stampaselezioneargomentitutor():
    connection = pymysql.connect(
        host="138.41.20.102",
        port=53306,
        user="caforio",
        password="studente",
        database="5bi_2025"
    )
    cognome=request.form['cognome']
    cursor=connection.cursor()
    sql="select distinct argomento from ((attivita_corso_competive_programming inner join lezioni_corso_competive_programming on lezioni_corso_competive_programming.id=attivita_corso_competive_programming.idl) inner join tenute_da_corso_competive_programming on tenute_da_corso_competive_programming.idl=lezioni_corso_competive_programming.id) inner join docenti_corso_competive_programming on docenti_corso_competive_programming.id=tenute_da_corso_competive_programming.idd where cognome=%s"
    cursor.execute(sql, (cognome,))
    result=cursor.fetchall()
    cursor.close()
    return render_template("visualizzazionestampaform.html", result=result)




app.run(host="0.0.0.0", port=81)
