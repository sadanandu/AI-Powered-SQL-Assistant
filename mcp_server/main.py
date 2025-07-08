from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from mcp_server.db_client import run_query
from typing import Optional, List

app = FastAPI()

class QueryRequest(BaseModel):
    action: str
    query: str
    embedding:Optional[List[float]] = Field(
        default=None, description="Optional embedding vector for semantic queries"
    )

@app.post("/mcp/run")
async def run_sql(req: QueryRequest):
    if req.action != "run_sql":
        return {"error": "Unsupported action"}
    try:
        print(req.query)
        print(len(req.embedding))
        #vector = 
        results = run_query(req.query, req.embedding)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
