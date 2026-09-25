from db import get_db

class DocumentModel:
    """MVC Model representing Insurance Document Data in MongoDB with Dynamic Metrics."""
    
    @staticmethod
    def get_all():
        db = get_db()
        return list(db.documents.find())

    @staticmethod
    def get_by_id(doc_id):
        db = get_db()
        return db.documents.find_one({'_id': doc_id})

    @staticmethod
    def create(doc_data):
        db = get_db()
        return db.documents.insert_one(doc_data)

    @staticmethod
    def update_status(doc_id, status, confidence_score, badge_color):
        db = get_db()
        return db.documents.update_one(
            {'_id': doc_id},
            {'$set': {
                'summary_status': status,
                'confidence_score': confidence_score,
                'badge_color': badge_color
            }}
        )

    @staticmethod
    def count():
        db = get_db()
        return db.documents.count_documents({})

    @staticmethod
    def get_summary_stats():
        """Dynamically computes real-time statistics directly from MongoDB."""
        db = get_db()
        all_docs = list(db.documents.find())
        total = len(all_docs)
        
        verified = sum(1 for d in all_docs if d.get('summary_status') in ['VERIFIED', 'CONFORME'])
        failed = sum(1 for d in all_docs if d.get('summary_status') in ['FAKE', 'REJECTED'])
        pending = sum(1 for d in all_docs if d.get('summary_status') in ['SUSPECT', 'IN_ANALYSIS'])
        
        if total > 0:
            avg_conf = round(sum(d.get('confidence_score', 0) for d in all_docs) / total, 1)
        else:
            avg_conf = 100.0

        return {
            "total": total,
            "verified": verified,
            "failed": failed,
            "pending": pending,
            "in_analysis": 0,
            "avg_confidence": avg_conf
        }
