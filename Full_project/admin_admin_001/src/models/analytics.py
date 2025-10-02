from sqlalchemy import Column, Integer, String, Float, DateTime
from src.common.database import Base

class AnalyticsView(Base):
    __tablename__ = "analytics_view"
    __table_args__ = ({'extend_existing': True},)

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    time_bucket = Column(DateTime, nullable=False)
