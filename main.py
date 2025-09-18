from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.story_generator import StoryGenerator
from gtts import gTTS
import os
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

story_generator = StoryGenerator()

class StoryRequest(BaseModel):
    name: str
    age: int
    genre: str

@app.get("/")
def home():
    return {"message": "Welcome to AI Story Teller with  AI! Go to /static/index.html"}

@app.post("/generate_story")
def generate_story(request: StoryRequest):
    try:
        story = story_generator.generate_story(request.name, request.age, request.genre)
        return {"story": story}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/generate_story_audio")
def generate_story_audio(request: StoryRequest):
    try:
        story = story_generator.generate_story(request.name, request.age, request.genre)
        filename = f"story_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join("static", filename)

        # Generate audio file
        tts = gTTS(story)
        tts.save(filepath)

        return {
            "story": story,
            "audio_url": f"/static/{filename}"
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
