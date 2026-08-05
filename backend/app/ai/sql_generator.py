from sqlalchemy import text
from sqlalchemy.orm import Session
from app.Database import get_db
from groq import Groq
from app.config import settings
from fastapi import Depends
import re

AI=Groq(api_key=settings.api_key)

def get_db_details(db:Session):
     about_tables=db.execute(text(
          """
          SELECT table_name, column_name, data_type
          FROM information_schema.columns
          WHERE table_schema = 'public'
          """
     )).fetchall()

     table_relations=db.execute(text(
          """
          SELECT
          tc.table_name,
          kcu.column_name,
          ccu.table_name AS foreign_table,
          ccu.column_name AS foreign_column
          FROM information_schema.table_constraints AS tc
          JOIN information_schema.key_column_usage AS kcu
          ON tc.constraint_name = kcu.constraint_name
          JOIN information_schema.constraint_column_usage AS ccu
          ON ccu.constraint_name = tc.constraint_name
          WHERE tc.constraint_type = 'FOREIGN KEY'
          """
     )).fetchall()

     return about_tables,table_relations

def build_prompt(question:str,details):

     prompt=f"""
          You are a PostgreSQL expert Data Analyst!

          I am giving you my Database tables , columns ,
          their datatypes and relations if exists any
          between tables.

          DETAILS: 
          -> tables and their columns: {details[0]}
          -> relationships between tables: {details[1]}

          Now, My question is: {question}

          generate and give me only the PostgreSQL query to 
          run in pgadmin.

          your answer should only contain a copy paste reply query.

          NOTE: if question is not related to database,
          simply just deny it.
     """

     return prompt

def clean_sql(response: str) -> str:
     sql = response.strip()
     if sql.startswith("```"):
          sql = sql.split("```")[1]
          if sql.strip().lower().startswith("sql"):
               sql = sql.split("\n", 1)[1] if "\n" in sql else ""
     sql = sql.strip('"').strip("'")

     sql = re.sub(r"--.*", "", sql)

     sql = sql.split(";")[0].strip() + ";"

     return sql.strip()

def generate_sql(question:str,details) -> str:
     response = AI.chat.completions.create(
     model="llama-3.1-8b-instant",
     messages=[
        {"role": "system", "content": "You are a SQL expert"},
        {"role": "user", "content": build_prompt(question,details)}
     ]
     )
     return clean_sql((response.choices[0].message.content))

def generate_description(question:str,data:list) -> str:
     prompt=f"""
     I am giving you a question and the data recieved 
     against that question,In the form of json type containing
     key values and pairs. This data is actually extracted 
     from a PostgreSQL database table.

     Question = {question}
     Data = {data} 

     suppose this data as in the visual graph representation
     now you have you write a 5 lines of visual representation
     for that data but according to the question like 
     i am as a data analyst presenting that data to manager
     can create a image in his mind.take care that dont 
     mention type of graph.

     just give me the 5 lines no text before and after it
     """
     response = AI.chat.completions.create(
     model="llama-3.1-8b-instant",
     messages=[
        {"role": "system", "content": "You are a Visual representative expert"},
        {"role": "user", "content": prompt}
     ]
     )
     return response.choices[0].message.content