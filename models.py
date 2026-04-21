from sqlalchemy import Column, Integer, String, Date, Text, JSON
from database import Base

class BugReport(Base):
    __tablename__ = "bug_reports"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    author = Column(String)
    release_build_no = Column(String)
    fixed_by = Column(String, nullable=True)
    open_date = Column(Date)
    close_date = Column(Date, nullable=True)
    description = Column(Text)
    priority = Column(String)
    severity = Column(String)
    defect_types = Column(JSON)