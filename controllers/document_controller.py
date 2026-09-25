import datetime
from flask import render_template, request, jsonify, flash, redirect, url_for
from models.document_model import DocumentModel

class DocumentController:
    """MVC Controller managing Document Verification views & API operations."""

    @staticmethod
    def show_dashboard():
        documents = DocumentModel.get_all()
        stats = DocumentModel.get_summary_stats()
        
        # Check for newly submitted documents from brokers
        pending_count = sum(1 for doc in documents if doc.get('overall_status') == 'Pending Linar Review')
        if pending_count > 0:
            flash(f"System Alert: You have {pending_count} new document(s) from brokers awaiting verification.", "info")
            
        return render_template('dashboard.html', documents=documents, stats=stats, active_page='dashboard')

    @staticmethod
    def show_visual_verification(doc_id):
        doc = DocumentModel.get_by_id(doc_id)
        if not doc:
            all_docs = DocumentModel.get_all()
            doc = all_docs[0] if all_docs else {}
        return render_template('visual_verification.html', doc=doc, active_page='dashboard')

    @staticmethod
    def update_verification_status(doc_id):
        data = request.get_json() or {}
        new_status = data.get('status', 'VERIFIED')

        badge_color = 'success' if new_status in ['VERIFIED', 'CONFORME'] else ('danger' if new_status in ['FAKE', 'REJECTED'] else 'warning')
        confidence = 98 if new_status in ['VERIFIED', 'CONFORME'] else (0 if new_status in ['FAKE', 'REJECTED'] else 40)

        res = DocumentModel.update_status(doc_id, new_status, confidence, badge_color)
        return jsonify({"success": True, "modified": res.modified_count})
