from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError


def getdata(sql:str,db:Session):
     try:
          blocked = ["drop", "delete", "truncate", "update"]
          if any(word in sql.lower() for word in blocked):
               raise Exception("Unsafe query! I can't edit existing data")
          result=db.execute(text(sql))
          rows=result.fetchall()
          table=[dict(row._mapping) for row in rows]
          if table:
               return table
          else:
               return ["No data to show!"]
     except ProgrammingError:
          return ["wrong SQL syntax!"]



