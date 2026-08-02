from fastapi import FastAPI,status,Depends
from fastapi.responses import JSONResponse
from app.schema import user_query,llm_response
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI(title="welcome to Ai-Data-Analyst",version="1.0")

app.get("/",status_code=status.HTTP_200_OK)
def test():
     return {"msg":"test route working"}
