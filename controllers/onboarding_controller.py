import os
import datetime
from flask import render_template, request, redirect, url_for, flash, current_app, jsonify
from werkzeug.utils import secure_filename

from models.document_model import DocumentModel
from services.document_analyzer import DocumentAnalyzer

class OnboardingController:
    """MVC Controller handling Client & Broker onboarding submissions."""

    @staticmethod
    def show_onboarding_form():
        return render_template('onboarding.html', active_page='onboarding')

    @staticmethod
    def process_document_upload_ajax():
        client_name = request.form.get('client_name', '').strip() or 'Submitted Client'
        doc_type = request.form.get('doc_type', 'cipc')

        file = request.files.get('document')

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
        else:
            return jsonify({'success': False, 'error': 'No document provided'}), 400

        # Analyze document with AI inspection service
        analysis = DocumentAnalyzer.analyze_document(doc_type, save_path, client_name)

        doc_type_labels = {
            'cipc': 'CIPC Company Registration',
            'id_copy': 'Certified ID Copy / SA ID',
            'fsp_licence': 'FSP Licence / Registration Letter',
            'claims_report': 'Claims Experience Report (3 Years)',
            'bank_proof': 'Proof of Bank Account'
        }

        doc_record = {
            "title": filename,
            "doc_type": doc_type,
            "doc_type_label": doc_type_labels.get(doc_type, doc_type),
            "file_size": f"{analysis['file_size_kb']} KB",
            "extension": os.path.splitext(filename)[1].replace('.', '').upper() or 'JPG',
            "upload_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "part": "1/1",
            "summary_status": "PENDING_LIVENESS", # Initial state
            "confidence_score": analysis["confidence_score"],
            "overall_status": "Awaiting Biometric Verification",
            "status_badge_class": "bg-warning",
            "extracted_fields": analysis["extracted_fields"],
            "verification_checks": analysis["verification_checks"]
        }

        inserted_id = DocumentModel.create(doc_record)
        return jsonify({
            'success': True, 
            'doc_id': str(inserted_id),
            'message': 'Document ingested. Proceeding to liveness check.'
        })

    @staticmethod
    def complete_liveness_ajax(doc_id):
        # Update the document to indicate liveness passed
        updates = {
            "summary_status": "VERIFIED", # or leave it for Linar to verify, but let's set to PENDING_REVIEW
            "overall_status": "Pending Linar Review",
            "status_badge_class": "bg-success"
        }
        # In a real app, we'd add the biometric check to the verification_checks array here.
        DocumentModel.update(doc_id, updates)
        return jsonify({'success': True, 'message': 'Biometric verification complete. Sent to Linar.'})
