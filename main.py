from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def getEvents(skip: int = 0, limit: int = -1):
    db = SessionLocal()
    events = db.query(Event).offset(skip).limit(limit).all()
    db.close()
    return events

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):    
    return templates.TemplateResponse(
        request=request, name="index.html", context={}
    )

@app.get("/events", response_class=HTMLResponse)
async def get_events(request: Request):
    events = getEvents()
    
    return templates.TemplateResponse(
        request=request, name="eventsList.html", context={"events": events}
    )

from database import SessionLocal, Event, EventArgs

# Route to create a new event
@app.post("/events", response_class=HTMLResponse)
async def create_event(request: Request, event: EventArgs):
    db_event = Event(**event.model_dump())
    db = SessionLocal()
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    db.close()
    events = getEvents()

    return templates.TemplateResponse(
        request=request, name="eventsList.html", context={"newId": id, "events": events}
    )