from fastapi import FastAPI
from api.places_app.places_view import router as places_router
from api.hotels_app.hotels_views import router as hotels_router

app = FastAPI()

app.include_router(places_router, prefix="/api")
app.include_router(hotels_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to TravelCompanion"}
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
