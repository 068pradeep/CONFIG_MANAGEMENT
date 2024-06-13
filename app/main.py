from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_configuration/", response_model=schemas.Configuration, status_code=status.HTTP_201_CREATED)
def create_configuration(config: schemas.ConfigurationCreate, db: Session = Depends(get_db)):
    db_config = crud.get_configuration(db, country_code=config.country_code)
    if db_config:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Configuration already exists")
    return crud.create_configuration(db=db, config=config)

@app.get("/get_configuration/{country_code}", response_model=schemas.Configuration)
def get_configuration(country_code: str, db: Session = Depends(get_db)):
    db_config = crud.get_configuration(db, country_code=country_code)
    if db_config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration not found")
    return db_config

@app.post("/update_configuration/{country_code}", response_model=schemas.Configuration)
def update_configuration(country_code: str, requirements: schemas.ConfigurationBase, db: Session = Depends(get_db)):
    db_config = crud.get_configuration(db, country_code=country_code)
    if db_config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration not found")
    crud.update_configuration(db, country_code=country_code, requirements=requirements.requirements)
    return crud.get_configuration(db, country_code=country_code)

@app.delete("/delete_configuration/{country_code}", response_model=schemas.Configuration)
def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    db_config = crud.get_configuration(db, country_code=country_code)
    if db_config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Configuration not found")
    crud.delete_configuration(db, country_code=country_code)
    return db_config

# Add exception handlers if needed
# ...

# Run the application using Uvicorn:
# uvicorn app.main:app --reload
