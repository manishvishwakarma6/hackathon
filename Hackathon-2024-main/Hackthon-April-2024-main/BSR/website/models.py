from flask_login import UserMixin
from mongoengine import Document, StringField, IntField, DateTimeField, SequenceField, ReferenceField, ListField, PULL
import datetime

class Report(Document):
    report_id = SequenceField(primary_key=True)
    report_data = StringField(max_length=10000)
    date = DateTimeField(default=datetime.datetime.now)
    patient_id = ReferenceField('Patient')

class Prescription(Document):
    prescription_id = SequenceField(primary_key=True)
    prescription_data = StringField(max_length=10000)
    date = DateTimeField(default=datetime.datetime.now)
    patient_id = ReferenceField('Patient')

class Receipt(Document):
    receipt_id = SequenceField(primary_key=True)
    receipt_data = StringField(max_length=10000)
    date = DateTimeField(default=datetime.datetime.now)
    patient_id = ReferenceField('Patient')

class Patient(Document, UserMixin):
    user_id = SequenceField(primary_key=True)
    patient_id = SequenceField(required=True)
    name = StringField(max_length=150)
    mobile_number = StringField(max_length=15)
    blood_group = StringField(max_length=10)
    height = IntField()
    weight = IntField()
    # Define reverse delete rule for reports, prescriptions, and receipts
    reports = ListField(ReferenceField('Report', reverse_delete_rule=PULL))
    prescriptions = ListField(ReferenceField('Prescription', reverse_delete_rule=PULL))
    receipts = ListField(ReferenceField('Receipt', reverse_delete_rule=PULL))

class User(UserMixin, Document):
    meta = {'collection': 'users'} 
    email = StringField(max_length=30, unique=True)
    password = StringField()
    