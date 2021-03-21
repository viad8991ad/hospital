from datetime import date

from peewee import Model, AutoField, TextField, DateField, SqliteDatabase, CharField, ForeignKeyField

from constant import NEW, CLOSE

db = SqliteDatabase('hospital.sqlite')
cursor = db.cursor()


class BaseModel(Model):
    class Meta:
        database = db


class Doctor(BaseModel):
    id = AutoField(column_name='id')
    fio = TextField(column_name="fio", null=False)
    speciality = CharField(column_name="speciality", max_length=70, null=False)

    class Meta:
        table_name = 'doctor'


class Patient(BaseModel):
    id = AutoField(column_name='id')
    fio = TextField(column_name="fio", null=False)
    birthday = DateField(column_name="birthday", null=False)
    snils = CharField(column_name="snils", max_length=11, null=False)
    polis = CharField(column_name="polis", max_length=16, null=False)
    address = TextField(column_name="address", null=False)
    phone = CharField(column_name="phone", max_length=10, null=False)

    class Meta:
        table_name = 'patient'


class Direction(BaseModel):
    id = AutoField(column_name='id')
    doctor = ForeignKeyField(Doctor, backref="doctor_id", null=False)
    patient = ForeignKeyField(Patient, backref="patient_id", null=False)
    cabinet = CharField(column_name="cabinet", max_length=10, null=False)
    date = DateField(column_name="date", null=False)
    state = CharField(column_name="state", max_length=5, null=False, default=NEW)

    class Meta:
        table_name = 'direction'


class Receipt(BaseModel):
    id = AutoField(column_name='id')
    doctor = ForeignKeyField(Doctor, backref="doctor_id", null=False)
    patient = ForeignKeyField(Patient, backref="patient_id", null=False)
    description = TextField(column_name="description", null=False)

    class Meta:
        table_name = 'receipt'


class Analyzes(BaseModel):
    doctor = ForeignKeyField(Doctor, backref="doctor_id", null=False)
    patient = ForeignKeyField(Patient, backref="patient_id", null=False)
    description = TextField(column_name="description", null=False)
    result = TextField(column_name="result", null=False)
    date = DateField(column_name="date", null=False)

    class Meta:
        table_name = 'analyzes'


class Report(BaseModel):
    id = AutoField(column_name='id')
    patient = ForeignKeyField(Patient, backref="patient_id", null=False)
    direction = ForeignKeyField(Direction, backref="direction_id", null=False)
    receipt = ForeignKeyField(Receipt, backref="receipt_id", null=False)
    analyzes = ForeignKeyField(Analyzes, backref="analyzes_id", null=False)

    class Meta:
        table_name = 'report'


def get_all_patient():
    return list(Patient.select().execute())


def get_all_doctors():
    return list(Doctor.select().execute())


def get_all_report():
    return list(Report.select().execute())


def find_new_directions():
    return list(Direction.select().where(Direction.state == NEW).execute())


def close_direction(direction):
    direction.state = CLOSE
    direction.save()


def insert_patient(fio, date, snils, polis, address, phone):
    Patient.create(fio=fio, birthday=date, snils=snils, polis=polis, address=address, phone=phone)


def insert_direction(doctor_id, patient_id, cabinet, date):
    doctor = Doctor.get(Doctor.id == int(doctor_id))
    patient = Patient.get(Patient.id == int(patient_id))
    Direction.create(doctor=doctor, patient=patient, cabinet=cabinet, date=date)


def insert_receipt(doctor, patient, description):
    return Receipt.create(doctor=doctor, patient=patient, description=description)


def insert_analyzes(doctor, patient, description, result, date):
    return Analyzes.create(doctor=doctor, patient=patient, description=description, result=result, date=date)


def insert_report(patient, direction, receipt, analyzes):
    Report.create(patient=patient, direction=direction, receipt=receipt, analyzes=analyzes)


db.create_tables([Doctor, Patient, Direction, Receipt, Analyzes, Report])

if not Patient.select().limit(1).dicts().execute():
    Patient.create(fio="Иванов Иван Иванович", birthday=date.today(), snils="snils", polis="polis", address="address",
                   phone="phone")
    Patient.create(fio="Петров Петр Петрович", birthday=date.today(), snils="snils", polis="polis", address="address",
                   phone="phone")

if not Doctor.select().limit(1).dicts().execute():
    Doctor.create(fio="Айболит Сказочников", speciality="хирург")
    Doctor.create(fio="Глазов Глазин Сергеевич", speciality="терапевт")
