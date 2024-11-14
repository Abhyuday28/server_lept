from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import uvicorn

app = FastAPI()

# Define the enrichment API URL and authorization token
enrichment_api_url = "https://api.coresignal.com/enrichment/companies"
headers = {
    "Authorization": "Bearer eyJhbGciOiJFZERTQSIsImtpZCI6ImFlOTU2M2MxLTdkYTgtMmU5Ny04YjU1LTFiZmZhZjVkODg3YSJ9.eyJhdWQiOiJkZXdhbGxhZHMuY29tIiwiZXhwIjoxNzYyOTc3NzA4LCJpYXQiOjE3MzE0MjA3NTYsImlzcyI6Imh0dHBzOi8vb3BzLmNvcmVzaWduYWwuY29tOjgzMDAvdjEvaWRlbnRpdHkvb2lkYyIsIm5hbWVzcGFjZSI6InJvb3QiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJkZXdhbGxhZHMuY29tIiwic3ViIjoiZmEwYzRjOWMtYzIxYy1mZmRmLWMwYjktNDhhZWQ1YWY5YzE2IiwidXNlcmluZm8iOnsic2NvcGVzIjoiY2RhcGkifX0.VpjAdnVjm0aj4KGaZyb1GQ1XhpmGKaJuI7UCdZvWX5O8ttIXihWRNqPBAJPDZIuUGpMMCUGxDde6wC7ntsOnBw"
}

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://lept-enrichment-tool.vercel.app"], 
    allow_credentials=True,
    allow_methods=["GET"],  
    allow_headers=["*"],  
)

@app.get("/")
def home():
    return {"message": "welcome"}

@app.get("/api/enrich")
def enrich_company(website: str = Query(..., description="The website URL of the company"), lookalikes: bool = True):
    # Build the full API URL with query parameters
    params = {
        "website": website,
        "lookalikes": str(lookalikes).lower()  # Convert to lowercase for compatibility
    }

    try:
        # Make the API request to the enrichment service
        response = requests.get(enrichment_api_url, headers=headers, params=params)

        # Check if the response is successful
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Enrichment API call failed.") from e

# Run the FastAPI app when executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
