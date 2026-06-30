from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import quests, tags

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Side Quests API", version="1.0.0", redirect_slashes=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this to your Vercel URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quests.router, prefix="/quests", tags=["quests"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])


@app.get("/")
def health():
    return {"status": "ok"}
