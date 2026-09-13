from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from sqlalchemy import UUID, DateTime, Text, String, ForeignKey
from typing import Optional, List
from model.base import Base
import uuid
# from model.workspace import Workspace

class TimeBlock(Base):
  __tablename__ = 'time_blocks'
  
  id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
  end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
  
  task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('tasks.id'), nullable=False)
  task: Mapped['Task'] = relationship(back_populates='time_blocks')
  
  @property
  def computed_duration(self) -> Optional[int]:
    if self.start_time and self.end_time:
      return int((self.end_time - self.start_time).total_seconds())
    return None
  
  def to_dict(self):
    return {
      "id": str(self.id),
      "title": self.title,
      "start_time": self.start_time.isoformat() if self.start_time else None,
      "end_time": self.end_time.isoformat() if self.end_time else None,
      "duration": self.computed_duration,
      "task_id": str(self.task_id),
    }
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# from sqlalchemy.orm import mapped_column, Mapped, relationship
# from datetime import datetime
# from sqlalchemy import UUID, DateTime, Text, String, ForeignKey
# from typing import Optional, List
# from model.base import Base
# import uuid
# # from model.workspace import Workspace

# class TimeBlock(Base):
#   __tablename__ = 'time_blocks'
  
#   id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#   title: Mapped[str] = mapped_column(String(100), nullable=False)
#   description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
#   start_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
#   end_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
  
#   creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
#   workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=False)
#   workspace: Mapped["Workspace"] = relationship(back_populates='events')
  
#   @property
#   def computed_duration(self) -> Optional[int]:
#     if self.start_time and self.end_time:
#       return int((self.end_time - self.start_time).total_seconds())
#     return None
  
#   def to_dict(self):
#     return {
#         "id": str(self.id),
#         "title": self.title,
#         "description": self.description,
#         "start_time": self.start_time.isoformat(),
#         "end_time": self.end_time.isoformat(),
#         "duration": self.computed_duration,
#         "workspace_id": str(self.workspace_id),
#     }    