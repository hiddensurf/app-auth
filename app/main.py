from fastapi import FastAPI
from app.users.routes import router as user_router
from app.posts.routes import router as post_router
from app.auth.routes import router as auth_router
from app import model_registry
app=FastAPI()
@app.get("/")
def root():
    return {
        "message": "App Auth API",
        "docs": "/docs",
        "health": "/health"
    }
@app.get("/health")
def health():
    return {"status": "healthy"}
app.include_router(auth_router,tags=["Login/Signup"])
app.include_router(user_router,tags=["Users"])
app.include_router(post_router,tags=["Posts"])
