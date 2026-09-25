import os
import unittest

# Force in-memory fallback DB in tests (no MongoDB connection attempt)
os.environ['MONGODB_URI'] = ''

from app import app
from db import get_db, reset_db
from services.document_analyzer import validate_sa_id, DocumentAnalyzer
from services.seed_data import seed_initial_data

class TestInsureAI(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

        # Reset and re-seed data so each test gets a fresh in-memory store
        reset_db()
        with app.app_context():
            db = get_db()
            seed_initial_data(db)

    def tearDown(self):
        reset_db()

    def test_sa_id_validation(self):
        # Test valid SA ID format & checksum
        valid, info = validate_sa_id("8507145892084")
        self.assertIn("dob", info)
        self.assertIn("gender", info)

        # Test invalid checksum SA ID
        valid_bad_check, info_bad = validate_sa_id("8507145892089")
        self.assertFalse(valid_bad_check)

    def test_unauthenticated_redirects(self):
        """Protected routes should redirect unauthenticated users to login."""
        protected = ['/onboarding', '/dashboard', '/verify/DOC-101', '/data-quality', '/analytics']
        for route in protected:
            r = self.app.get(route)
            self.assertEqual(r.status_code, 302, f"Expected redirect on {route}")
            self.assertIn(b'login', r.data.lower() or r.location.lower().encode())

    def test_index_redirects(self):
        """Index route redirects unauthenticated users to login."""
        r = self.app.get('/')
        self.assertEqual(r.status_code, 302)

    def test_login_page(self):
        """Login page should be accessible without authentication."""
        r = self.app.get('/login')
        self.assertEqual(r.status_code, 200)

    def test_authenticated_routes(self):
        """Simulate logged-in session and verify protected routes return 200."""
        with self.app.session_transaction() as sess:
            sess['user_email'] = 'test@insureai.com'

        routes_and_status = [
            ('/', 302),          # Redirects to dashboard
            ('/onboarding', 200),
            ('/dashboard', 200),
            ('/verify/DOC-101', 200),
            ('/data-quality', 200),
            ('/analytics', 200),
        ]
        for route, expected_status in routes_and_status:
            r = self.app.get(route)
            self.assertEqual(r.status_code, expected_status,
                             f"Route {route}: expected {expected_status}, got {r.status_code}")

    def test_document_analyzer(self):
        """DocumentAnalyzer should return proper structure for all doc types."""
        doc_types = ['cipc', 'id_copy', 'fsp_licence', 'claims_report', 'bank_proof']
        for dt in doc_types:
            result = DocumentAnalyzer.analyze_document(dt, '/nonexistent/path.pdf', 'Test Client')
            self.assertIn('confidence_score', result, f"Missing confidence_score for {dt}")
            self.assertIn('summary_tag', result, f"Missing summary_tag for {dt}")
            self.assertIn('extracted_fields', result, f"Missing extracted_fields for {dt}")

if __name__ == '__main__':
    unittest.main()
