from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/Chat") # A decorator to create a route for the predict endpoint
async def predict():
    return {"Bot": "Fuck"}


if __name__ == "__main__":
   uvicorn.run(app, host="localhost", port=8009)
