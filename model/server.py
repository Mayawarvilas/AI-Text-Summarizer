from pydantic import BaseModel   # Import BaseModel to define the structure of JSON input
from fastapi import FastAPI      # Import FastAPI to create API endpoints
from fastapi.middleware.cors import CORSMiddleware # Import CORS middleware to handle cross-origin requests
import main                      # Import your main file where text_summary function exists

app = FastAPI()                  # Create a FastAPI application instance

# Configure CORS to allow requests from the frontend
app.add_middleware( 
    CORSMiddleware, 
    allow_origins=["*"],         # Allow all origins (you can specify your frontend URL here) 
    allow_methods=["*"],         # Allow all HTTP methods
    allow_headers=["*"]          # Allow all headers
    )


class TextRequest(BaseModel):    # Define a model that describes the expected request body
    text: str                    # Declare that the JSON must contain a field "text" of type string


@app.post('/summarize')          # Create a POST API endpoint at URL /summarize
async def summarize_text(text_request: TextRequest):  # Receive JSON body and store it in text_request
    summary = main.text_summary(text_request.text)    # Call your summarization function using the input text

    return {                    # Return response in JSON format
        "summary": summary      # Send the generated summary back to the user
    }

if __name__ == "__main__":
   app.run()