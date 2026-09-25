from db import get_db

class OnboardingModel:
    """MVC Model representing Client/Broker Onboarding Applications in MongoDB."""

    @staticmethod
    def get_all():
        db = get_db()
        return list(db.onboardings.find())

    @staticmethod
    def get_by_id(onboarding_id):
        db = get_db()
        return db.onboardings.find_one({'_id': onboarding_id})

    @staticmethod
    def create(onboarding_data):
        db = get_db()
        return db.onboardings.insert_one(onboarding_data)

    @staticmethod
    def update_progress(onboarding_id, progress_pct, status=None):
        db = get_db()
        update_fields = {'progress_pct': progress_pct}
        if status:
            update_fields['status'] = status
        return db.onboardings.update_one({'_id': onboarding_id}, {'$set': update_fields})
