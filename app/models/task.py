from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime, timezone
import enum

class TaskStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ESCALATED = "Escalated"


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    assigned_by_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime, default=datetime.now(timezone.utc))
    due_date = Column(DateTime)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    dependency_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    escalation_flagged = Column(Boolean, default=False)

    # Relations
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    assigned_by = relationship("User", foreign_keys=[assigned_by_id])
    remarks = relationship("TaskRemark", back_populates="task")



class RemarkSource(str, enum.Enum):
    SUPERVISOR = "Supervisor"
    COMPLIANCE = "Compliance"
    HR = "HR"

class TaskRemark(Base):
    __tablename__ = "task_remarks"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    source = Column(Enum(RemarkSource))
    remark = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))

    task = relationship("Task", back_populates="remarks")
    user = relationship("User")



class EscalationLog(Base):
    __tablename__ = "escalations"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    escalated_by_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    reason = Column(Text)

    task = relationship("Task")
    escalated_by = relationship("User")

