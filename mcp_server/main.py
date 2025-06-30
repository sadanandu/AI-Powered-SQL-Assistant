from fastapi import FastAPI, Request
from pydantic import BaseModel
from mcp_server.db_client import run_query

app = FastAPI()

class QueryRequest(BaseModel):
    action: str
    query: str

@app.post("/mcp/run")
async def run_sql(req: QueryRequest):
    if req.action != "run_sql":
        return {"error": "Unsupported action"}
    try:
        results = run_query(req.query)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
