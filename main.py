import asyncio
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Header, Query, Path
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url="/docs")

app.add_middleware(HTTPSRedirectMiddleware)

allowed_hosts = ["www.example.com", "example.com", "127.0.0.1"]
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CORSMiddleware, allowed_hosts=allowed_hosts, allow_credentials=True, allow_methods=["*"])


@app.get("/")
async def get_chat(hello: str = "hello"):
    return hello


@app.get("/large_text")
async def large_text(user: str = "Anonimus"):
    return user * 1000


@app.get("/hello")
async def hello_rout(user: str = "Anonimus"):
    await asyncio.sleep(0.1)
    return f"Hello, {user}!"


@app.get("/path/{user_id}/")
async def index(user_id: int = Path(description="Enter your id, Example: 1"),
                timestamp: Optional[str] = Query(None, description="Enter your time, Example: 12:49"),
                x_client_version: int = Header(description="Enter your client_version, Example: 3.1.1")):
    if not timestamp:
        timestamp = datetime.now().isoformat()

    return {
        "user_id": user_id,
        "timestamp": timestamp,
        "X-Client-Version": x_client_version,
        "message": f"Hello, {user_id}!"
    }


if __name__ == "__main__":
    from server_run import uvicorn_run, hypercorn_run

    # hypercorn_run(app)
    uvicorn_run()