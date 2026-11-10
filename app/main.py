from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from app.query import query_records
app=FastAPI(title="Structured Data Query Agent",version="0.1.0")
class Query(BaseModel): records:list[dict]=Field(min_length=1); filters:dict[str,dict]={}; group_by:str|None=None; aggregate:str|None=None; value_field:str|None=None
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/query")
def query(req:Query):
    try: return query_records(**req.model_dump())
    except ValueError as e: raise HTTPException(400,str(e)) from e
