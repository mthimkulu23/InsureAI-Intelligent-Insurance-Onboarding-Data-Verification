from flask import render_template
from models.anomaly_model import AnomalyModel

class DataQualityController:
    """MVC Controller handling Data Quality & Anomaly Reporting."""

    @staticmethod
    def show_data_quality_portal():
        anomalies = AnomalyModel.get_all()
        dq_metrics = AnomalyModel.get_dq_metrics()
        return render_template('data_quality.html', anomalies=anomalies, dq_metrics=dq_metrics, active_page='data_quality')
