import os
import httpx
import argparse
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

API_KEY = os.getenv("MINIMAX_API_KEY")

if not API_KEY:
    raise ValueError("MINIMAX_API_KEY not set!")

parser = argparse.ArgumentParser(description="MiniMax Proxy")
parser.add_argument("--port", "-p", type=int, default=3333, help="Port to listen on (default: 3333)")
parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
args = parser.parse_args()

PORT = args.port

app = FastAPI()

@app.post("/{full_path:path}")
async def proxy(full_path: str, request: Request):
    """Proxy all POST requests to MiniMax API"""
    body = await request.body()
    
    if args.verbose:
        print(f"[REQUEST] {request.method} {request.url.path}")
        print(f"  Headers: {dict(request.headers)}")
        print(f"  Body: {body.decode()[:200]}...{body.decode()[-100:]}...")
    
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "Host": "api.minimax.io"
    }
    
    url = f"https://api.minimax.io/{full_path}"
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        try:
            response = await client.post(url, headers=headers, content=body)
            
            if args.verbose:
                print(f"[RESPONSE] Status: {response.status_code}")
                print(f"  Response: {response.text[:200]}...")
            
            async def stream():
                yield response.content
            
            return StreamingResponse(stream(), status_code=response.status_code, headers=dict(response.headers))
        except Exception as e:
            print(f"[ERROR] Proxy error: {e}")
            return JSONResponse(content={"error": str(e)}, status_code=502)

if __name__ == "__main__":
    import uvicorn
    print(f"MiniMax Proxy starting on port {PORT} (FastAPI/uvicorn)...")
    uvicorn.run(app, host="localhost", port=PORT)