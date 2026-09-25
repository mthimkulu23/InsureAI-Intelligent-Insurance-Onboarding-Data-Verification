from flask import render_template
from models.document_model import DocumentModel
from models.anomaly_model import AnomalyModel

class AnalyticsController:
    """MVC Controller handling Agency Pipeline Analytics."""

    @staticmethod
    def show_analytics_dashboard():
        stats = DocumentModel.get_summary_stats()
        dq_metrics = AnomalyModel.get_dq_metrics()
        return render_template('analytics.html', stats=stats, dq_metrics=dq_metrics, active_page='analytics')
