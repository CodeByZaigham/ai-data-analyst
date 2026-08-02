from pydantic import BaseModel,Field

class user_query(BaseModel):
     question:str=Field(
          ...,
          description="ask question about your data"
     )

class llm_response(BaseModel):
     sqlquery:str
     data:list