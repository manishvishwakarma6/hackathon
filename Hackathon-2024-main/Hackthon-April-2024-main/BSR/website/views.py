from flask import Blueprint, json, render_template, request, flash, jsonify,  redirect, url_for
from flask_login import login_required, current_user
from .models import Receipt, Report, Prescription, Patient
from mongoengine.errors import DoesNotExist, ValidationError




views = Blueprint('views', __name__)


@views.route('/portal', methods=['GET'])
@login_required
def portal():
    if request.method == 'POST': 
        patient_id = request.form.get('Patient_ID')  #Gets the patient id from the HTML 
        report = request.form.get('Report')  #Gets the report from the HTML 
        receipt = request.form.get('Receipt')  #Gets the reciept from the HTML
        prescription = request.form.get('Prescription')  #Gets the prescription from the HTML


# ***************** Insertion ******************************

# insert a Report in the database
@views.route('/add-report', methods=['POST'])
@login_required
def add_report():
    patient_id = request.form.get('patient_id')
    report_data = request.form.get('report_data')
    
    patient = Patient.objects(patient_id=patient_id).first()
    if patient:
        report = Report(report_data=report_data, patient_id=patient)
        report.save()
        flash('Report added successfully!', category='success')
    else:
        flash('Patient not found.', category='error')

    return redirect(url_for('views.dashboard'))   

# insert a Reciept in the database
@views.route('/add-receipt', methods=['POST'])
@login_required
def add_receipt():
    patient_id = request.form.get('patient_id')
    receipt_data = request.form.get('receipt_data')
    
    patient = Patient.objects(patient_id=patient_id).first()
    if patient:
        receipt = Receipt(receipt_data=receipt_data, patient_id=patient)
        receipt.save()
        flash('Receipt added successfully!', category='success')
    else:
        flash('Patient not found.', category='error')

    return redirect(url_for('views.dashboard'))

# insert a Prescription in the database
@views.route('/add-prescription', methods=['POST'])
@login_required
def add_prescription():
    patient_id = request.form.get('patient_id')
    prescription_data = request.form.get('prescription_data')
    
    patient = Patient.objects(patient_id=patient_id).first()
    if patient:
        prescription = Prescription(prescription_data = prescription_data, patient_id=patient)
        prescription.save()
        flash('Prescription added successfully!', category='success')
    else:
        flash('Patient not found.', category='error')

    return redirect(url_for('views.dashboard'))

# **************** Deletion ******************


# delete a report from the database
@views.route('/delete-report', methods=['DELETE'])
@login_required
def delete_report():
    try:
        data = request.get_json()
        report_id = data['report_id']
        report = Report.objects.get(id=report_id, patient_id=current_user.patient_id)
        report.delete()
        return jsonify({"message": "Report deleted successfully"}), 200
    except DoesNotExist:
        return jsonify({"error": "Report not found or unauthorized"}), 404
    except ValidationError:
        return jsonify({"error": "Invalid report ID"}), 400
    except KeyError:
        return jsonify({"error": "Report ID not provided"}), 400


# delete a prescription from the database
@views.route('/delete-prescription', methods=['DELETE'])
@login_required
def delete_prescription():
    try:
        data = request.get_json()
        prescription_id = data['prescription_id']
        prescription = Prescription.objects.get(id=prescription_id, patient_id=current_user.patient_id)
        prescription.delete()
        return jsonify({"message": "Prescription deleted successfully"}), 200
    except DoesNotExist:
        return jsonify({"error": "Prescription not found or unauthorized"}), 404
    except ValidationError:
        return jsonify({"error": "Invalid Prescription ID"}), 400
    except KeyError:
        return jsonify({"error": "Prescription ID not provided"}), 400
    

# delete a receipt from the database
@views.route('/delete-reciept', methods=['DELETE'])
@login_required
def delete_receipt():
    try:
        data = request.get_json()
        receipt_id = data['receipt_id']
        receipt = Receipt.objects.get(id=receipt_id, patient_id=current_user.patient_id)
        receipt.delete()
        return jsonify({"message": "Receipt deleted successfully"}), 200
    except DoesNotExist:
        return jsonify({"error": "Receipt not found or unauthorized"}), 404
    except ValidationError:
        return jsonify({"error": "Invalid Receipt ID"}), 400
    except KeyError:
        return jsonify({"error": "Receipt ID not provided"}), 400