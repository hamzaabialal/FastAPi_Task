from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
import auth
from database import engine, SessionLocal
import schemas
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import models

app = FastAPI()

app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/data/", status_code=status.HTTP_200_OK)
def get_data(db: Session = Depends(get_db), current_user: models.Users = Depends(auth.get_current_user)):
    user = db.query(models.Users).filter(models.Users.username == current_user).first()
    query = db.query(models.TodoTask).filter(models.TodoTask.user_id == user.id).all()
    return {"data": query}

@app.post("/data/post/", status_code=status.HTTP_201_CREATED, response_model=schemas.TodoTaskCreate)
def create_student(request: schemas.TodoTaskCreate, db: Session = Depends(get_db), current_user: models.Users = Depends(auth.get_current_user)):
    user = db.query(models.Users).filter(models.Users.username == current_user).first()
    new_task = models.TodoTask(
        task_name=request.task_name,
        status=request.status,
        user_id=user.id,
        created_at=request.created_at
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
@app.post("/templates/", response_model=schemas.TemplateModelCreate)
def create_template(template: schemas.TemplateModelCreate, db: Session = Depends(get_db)):
    template_data = template.dict()

    new_template = models.TemplateModel(name=template_data['name'], rename=template_data['rename'])

    for tab_data in template_data['tabs']:
        new_tab = models.TabModel(tab_name=tab_data['tab_name'], tab_rename=tab_data['tab_rename'],
                                  tab_is_active=tab_data['tab_is_active'], template=new_template)
        if tab_data.get('tab_sections', []):
            for section_data in tab_data.get('tab_sections', []):
                new_section = models.SectionModel(section_name=section_data['section_name'],
                                                  section_rename=section_data['section_rename'],
                                                  section_is_active=section_data['section_is_active'], tab=new_tab)

                for field_data in section_data['section_fields']:
                    new_field = models.FieldModel(field_name=field_data['field_name'],
                                                  field_rename=field_data['field_rename'],
                                                  field_type=field_data['field_type'],
                                                  field_is_active=field_data['field_is_active'], section=new_section)
                    db.add(new_field)

                db.add(new_section)
            db.add(new_tab)

        db.add(new_template)
        db.commit()
        db.refresh(new_template)

    return new_template

@app.get("/template/name/", response_model=List[schemas.TemplateModelCreate])
def get_template(db: Session = Depends(get_db), name=None):
    query = db.query(models.TemplateModel).filter(models.TemplateModel.name==name).all()
    return query
