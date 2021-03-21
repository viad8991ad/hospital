from logging import basicConfig, DEBUG, info as log_i
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from repo import insert_patient, get_all_doctors, get_all_patient, insert_direction, get_all_report

from helpers import check_data_from_str, simulation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oaiheiuheih-secret-key'
basicConfig(filename=f'log-{datetime.now()}.log', level=DEBUG)


@app.route("/")
def index():
    log_i(f'open view index. remote_addr - {request.remote_addr}')
    return render_template("index.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == 'POST':
        fio = request.form['fio']
        date = check_data_from_str(request.form['date'], "date")
        snils = check_data_from_str(request.form['snils'], "snils")
        polis = check_data_from_str(request.form['polis'], "polis")
        address = request.form['address']
        phone = check_data_from_str(request.form['phone'], "phone")
        if not fio or not date or not snils or not polis or not address or not phone:
            flash('Данные введены не корректно')
            return redirect(url_for('registration'))
        else:
            log_i(f'registration new patient. remote_addr - {request.remote_addr}')
            insert_patient(fio, date, snils, polis, address, phone)
            return redirect(url_for("index"))
    log_i(f'open view registration. remote_addr - {request.remote_addr}')
    return render_template("registration.html")


@app.route("/issuing", methods=["GET", "POST"])
def issuing():
    if request.method == 'POST':
        doctor = request.form.get('doctor')
        patient = request.form.get('patient')
        cabinet = request.form['cabinet']
        date = check_data_from_str(request.form['date'], "date")
        if not doctor or not patient or not cabinet or not date:
            flash('Данные введены не корректно')
            return redirect(url_for('issuing'))
        else:
            log_i(f'registration new direction. remote_addr - {request.remote_addr}')
            insert_direction(doctor, patient, cabinet, date)
            simulation()
            return redirect(url_for("index"))
    log_i(f'open view issuing. remote_addr - {request.remote_addr}')
    doctors = get_all_doctors()
    patients = get_all_patient()
    return render_template("issuing.html", doctors=doctors, patients=patients)


@app.route("/history", methods=["GET"])
def history():
    reports = get_all_report()
    return render_template("history.html", reports=reports)


if __name__ == "__main__":
    app.run()
