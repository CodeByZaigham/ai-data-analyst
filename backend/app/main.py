from fastapi import FastAPI,status,Depends
from fastapi.responses import JSONResponse
from .Database import get_db 
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from .schema import user_query,llm_response
from app.services.query_runner import getdata
from app.ai.sql_generator import generate_sql,get_db_details,generate_description
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="welcome to Ai-Data-Analyst",version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",status_code=status.HTTP_200_OK)
def test():
     return {"msg":"test route working"}

@app.post("/query" ,response_model=llm_response,status_code=status.HTTP_200_OK)
def analyze(question:user_query,db:Session=Depends(get_db)):
     try:
          db_details=get_db_details(db)
          sql_query=generate_sql(question,db_details)
          data=getdata(sql_query,db)
          description=generate_description(question,data)
          return llm_response(Sqlquery=sql_query,Data=data,Description=description)
     except Exception as e:
          return llm_response(Sqlquery=" ",Data=[],Description=str(e))
