from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import logging
from typing import Dict, Any

from app.scraper import check_ulez_compliance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Emission Zone Compliance Checker",
    description="Check if your vehicle is compliant with emission zone regulations",
    version="1.0.0",
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with the search form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{registration}", response_class=JSONResponse)
async def check_compliance(registration: str):
    """
    Check emission zone compliance for a given vehicle registration.
    
    Args:
        registration: Vehicle registration number
        
    Returns:
        JSON response with compliance data
    """
    try:
        # Clean registration input
        registration = registration.strip().upper().replace(" ", "")
        
        # Validate registration format (basic UK format check)
        if not registration or len(registration) < 2 or len(registration) > 8:
            raise HTTPException(status_code=400, detail="Invalid registration format")
            
        # Get compliance data
        result = await check_ulez_compliance(registration)
        return result
        
    except ValueError as e:
        logger.warning(f"Invalid registration: {registration} - {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        logger.error(f"Error checking compliance for {registration}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error checking compliance")


@app.get("/{registration}/html", response_class=HTMLResponse)
async def check_compliance_html(request: Request, registration: str):
    """
    Check emission zone compliance and return HTML result page
    
    Args:
        request: FastAPI request object
        registration: Vehicle registration number
        
    Returns:
        HTML response with compliance data
    """
    try:
        # Clean registration input
        registration = registration.strip().upper().replace(" ", "")
        
        # Validate registration format (basic UK format check)
        if not registration or len(registration) < 2 or len(registration) > 8:
            return templates.TemplateResponse(
                "result.html", 
                {
                    "request": request,
                    "error": "Invalid registration format",
                    "registration": registration
                }
            )
            
        # Get compliance data
        result = await check_ulez_compliance(registration)
        return templates.TemplateResponse("result.html", {"request": request, "result": result})
        
    except ValueError as e:
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request,
                "error": str(e),
                "registration": registration
            }
        )
        
    except Exception as e:
        logger.error(f"Error checking compliance for {registration}: {str(e)}")
        return templates.TemplateResponse(
            "result.html", 
            {
                "request": request,
                "error": "Error checking compliance. Please try again later.",
                "registration": registration
            }
        )


if __name__ == "__main__":
    # Run the application with uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
