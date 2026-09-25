import datetime

def seed_initial_data(db):
    """
    Populates MongoDB / Memory Store with clean, 100% English initial seed dataset.
    """
    # Clear existing demo data
    db.documents.delete_many({})
    db.onboardings.delete_many({})
    db.anomalies.delete_many({})
    db.audit_logs.delete_many({})

    # 1. Onboarding Applications
    onboardings_list = [
        {
            "_id": "ONB-2026-001",
            "client_name": "Apex Risk Holdings (Pty) Ltd",
            "trading_name": "Apex Digital Risk",
            "registration_no": "K2021/887412/07",
            "fsp_no": "FSP 48921",
            "contact_email": "compliance@apexrisk.co.za",
            "contact_phone": "+27 11 982 4000",
            "status": "APPROVED",
            "progress_pct": 100,
            "created_at": "2026-08-01 10:15:00",
            "assigned_broker": "Thabo Mbeki Advisory",
            "risk_tier": "Low Risk",
            "documents_submitted": 5,
            "documents_verified": 5
        },
        {
            "_id": "ONB-2026-002",
            "client_name": "Vanguard Commercial Risk Solutions",
            "trading_name": "Vanguard Risk",
            "registration_no": "2019/332114/07",
            "fsp_no": "FSP 14092",
            "contact_email": "compliance@vanguardrisk.co.za",
            "contact_phone": "+27 21 400 1122",
            "status": "UNDER_REVIEW",
            "progress_pct": 80,
            "created_at": "2026-08-08 14:30:00",
            "assigned_broker": "Apex Insurance Partners",
            "risk_tier": "Medium Risk",
            "documents_submitted": 5,
            "documents_verified": 4
        },
        {
            "_id": "ONB-2026-003",
            "client_name": "Zonkizizwe Logistics & Supply Chain",
            "trading_name": "Zonkizizwe Transport",
            "registration_no": "2022/990145/07",
            "fsp_no": "Jurisdiction Exemption Letter",
            "contact_email": "admin@zonkizizwetransport.co.za",
            "contact_phone": "+27 31 301 9988",
            "status": "ACTION_REQUIRED",
            "progress_pct": 60,
            "created_at": "2026-08-12 09:20:00",
            "assigned_broker": "Direct Client Portal",
            "risk_tier": "Suspect Anomaly",
            "documents_submitted": 4,
            "documents_verified": 2
        }
    ]

    for item in onboardings_list:
        db.onboardings.insert_one(item)

    # 2. Documents Dataset (100% English Labels)
    documents_list = [
        {
            "_id": "DOC-101",
            "onboarding_id": "ONB-2026-001",
            "title": "Director_SA_ID_Copy.pdf",
            "doc_type": "id_copy",
            "doc_type_label": "Certified Director SA ID Copy",
            "file_size": "621 KB",
            "extension": "PDF",
            "upload_date": "12/08/2026 15:46",
            "part": "1/1",
            "summary_status": "VERIFIED",
            "confidence_score": 94,
            "badge_color": "success",
            "overall_status": "Completed",
            "status_badge_class": "bg-success",
            "extracted_fields": {
                "Document Type": "South African National ID",
                "ID Number": "8507145892084",
                "Full Name": "Themba Nkosi",
                "Date of Birth": "1985-07-14",
                "Gender": "Male",
                "Citizenship": "South African Citizen",
                "Certification Stamp": "Certified Copy (< 3 Months Old)"
            }
        },
        {
            "_id": "DOC-102",
            "onboarding_id": "ONB-2026-001",
            "title": "CIPC_Company_Registration_Certificate.pdf",
            "doc_type": "cipc",
            "doc_type_label": "CIPC Company Registration Document",
            "file_size": "4.51 MB",
            "extension": "PDF",
            "upload_date": "08/08/2026 16:55",
            "part": "1/1",
            "summary_status": "VERIFIED",
            "confidence_score": 96,
            "badge_color": "success",
            "overall_status": "Completed",
            "status_badge_class": "bg-success",
            "extracted_fields": {
                "Document Type": "CIPC CoR 14.3 Certificate",
                "Enterprise Number": "K2021/887412/07",
                "Company Name": "Apex Risk Holdings (Pty) Ltd",
                "Directors": "2 Active Directors Verified",
                "Tax Compliance": "Tax Pin Validated"
            }
        },
        {
            "_id": "DOC-103",
            "onboarding_id": "ONB-2026-001",
            "title": "FSCA_FSP_Licence_Certificate.pdf",
            "doc_type": "fsp_licence",
            "doc_type_label": "FSP Licence / Registration Letter",
            "file_size": "182.9 KB",
            "extension": "PDF",
            "upload_date": "08/08/2026 16:56",
            "part": "1/1",
            "summary_status": "VERIFIED",
            "confidence_score": 98,
            "badge_color": "success",
            "overall_status": "Completed",
            "status_badge_class": "bg-success",
            "extracted_fields": {
                "Document Type": "FSCA FSP Licence",
                "FSP Number": "FSP 48921",
                "Category": "Category I Advisory & Intermediary",
                "Issue Date": "2022-03-15",
                "Standing": "Good Standing"
            }
        },
        {
            "_id": "DOC-104",
            "onboarding_id": "ONB-2026-001",
            "title": "Claims_Experience_Report_3Years.pdf",
            "doc_type": "claims_report",
            "doc_type_label": "Claims Experience Report (3 Years)",
            "file_size": "628.08 KB",
            "extension": "PDF",
            "upload_date": "08/08/2026 16:56",
            "part": "1/1",
            "summary_status": "VERIFIED",
            "confidence_score": 91,
            "badge_color": "success",
            "overall_status": "Completed",
            "status_badge_class": "bg-success",
            "extracted_fields": {
                "Document Type": "3-Year Claims History",
                "Insurer": "Santam Commercial Insurance",
                "Total Claim Amount": "R 142,500.00",
                "Loss Ratio": "24.5% (Low Risk)",
                "Period Covered": "2023 - 2026"
            }
        },
        {
            "_id": "DOC-105",
            "onboarding_id": "ONB-2026-001",
            "title": "FNB_Proof_Of_Bank_Account.pdf",
            "doc_type": "bank_proof",
            "doc_type_label": "Proof of Bank Account",
            "file_size": "312.4 KB",
            "extension": "PDF",
            "upload_date": "10/08/2026 11:20",
            "part": "1/1",
            "summary_status": "VERIFIED",
            "confidence_score": 95,
            "badge_color": "success",
            "overall_status": "Completed",
            "status_badge_class": "bg-success",
            "extracted_fields": {
                "Bank Institution": "First National Bank (FNB)",
                "Account Holder": "Apex Risk Holdings (Pty) Ltd",
                "Account Number": "6289 **** 4102",
                "Branch Code": "250655",
                "Stamp Date": "2026-08-01"
            }
        }
    ]

    for doc in documents_list:
        db.documents.insert_one(doc)

    # 3. Data Quality Engine Checks
    dq_checks = [
        {"rule": "Freshness Check", "status": "Passed", "detail": "Document timestamps active"},
        {"rule": "13-Digit SA ID Luhn Verification", "status": "Passed", "detail": "Engine Check #114 executed"},
        {"rule": "CIPC Enterprise Format Standard", "status": "Passed", "detail": "100% format compliance"},
        {"rule": "Bank Stamp < 90 Days Recency", "status": "Passed", "detail": "Validated against bank API"},
        {"rule": "FSCA Active FSP Registry Match", "status": "Passed", "detail": "No suspended licences found"}
    ]
    for check in dq_checks:
        db.anomalies.insert_one(check)

    # 4. Audit Log
    db.audit_logs.insert_one({
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": "System Auto-Inspector",
        "action": "AUTOMATED_OCR_VERIFICATION_COMPLETE",
        "details": "Engine analyzed onboarding documents. Health Score: 100/100"
    })
