from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.calculate import router as calculate_router  # Import the router

app = FastAPI(root_path="/api")

# CORS middleware to allow frontend React to communicate with FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React frontend runs on port 3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the calculator router
app.include_router(calculate_router)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
