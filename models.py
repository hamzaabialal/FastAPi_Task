import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return f"Users(id={self.id!r}, username={self.username!r}, email={self.email!r})"

class TodoTask(Base):
    __tablename__ = "todo_task"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String)
    status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class FieldModel(Base):
    __tablename__ = "field_model"
    id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String)
    field_rename = Column(String)
    field_type = Column(String)
    field_is_active = Column(String)
    section_id = Column(Integer, ForeignKey('section_model.id'))
    section = relationship("SectionModel", back_populates="section_fields")

class SectionModel(Base):
    __tablename__ = "section_model"
    id = Column(Integer, primary_key=True, index=True)
    section_name = Column(String)
    section_rename = Column(String)
    section_is_active = Column(String)
    section_fields = relationship("FieldModel", back_populates="section")
    tab_id = Column(Integer, ForeignKey('tab_model.id'))
    tab = relationship("TabModel", back_populates="tab_sections")

class TabModel(Base):
    __tablename__ = "tab_model"
    id = Column(Integer, primary_key=True, index=True)
    tab_name = Column(String)
    tab_rename = Column(String)
    tab_is_active = Column(String)
    tab_sections = relationship("SectionModel", back_populates="tab")
    template_id = Column(Integer, ForeignKey('template_model.id'))  # Ensure this line exists
    template = relationship("TemplateModel", back_populates="tabs")

class TemplateModel(Base):
    __tablename__ = "template_model"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rename = Column(String)
    tabs = relationship("TabModel", back_populates="template")

class FormDataModel(Base):
    __tablename__ = "form_data_model"
    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String)
    data = Column(String)