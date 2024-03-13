# Import Fast API
from fastapi import FastAPI
# Import uvicorn
import uvicorn

# Create an app/ instance of FAST API
app = FastAPI()

# ping method to make sure server is alive.
@app.get("/ping")
async def ping():
    return "Hello, I am alive."

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)