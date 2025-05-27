from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import logging
import asyncio
from typing import Dict, Any
from datetime import datetime, timedelta
import time

from app.scraper import check_ulez_compliance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Simple in-memory cache for results (in production, use Redis)
cache = {}
CACHE_TTL = 3600  # 1 hour cache

# Initialize FastAPI app
app = FastAPI(
    title="Fast ULEZ Compliance Checker",
    description="Lightning-fast vehicle emission zone compliance checking using direct API calls",
    version="2.0.0",
)

# Add CORS middleware for better API access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")


def get_cached_result(registration: str):
    """Get cached result if available and not expired"""
    if registration in cache:
        result, timestamp = cache[registration]
        if datetime.now() - timestamp < timedelta(seconds=CACHE_TTL):
            return result
        else:
            # Remove expired cache entry
            del cache[registration]
    return None


def cache_result(registration: str, result):
    """Cache the result with timestamp"""
    cache[registration] = (result, datetime.now())


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with the search form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/stats")
async def get_stats():
    """Get cache statistics"""
    return {
        "cache_size": len(cache),
        "cached_registrations": list(cache.keys()),
        "cache_ttl_seconds": CACHE_TTL
    }


@app.get("/api/{registration}", response_class=JSONResponse)
async def check_compliance_api(registration: str):
    """
    Check emission zone compliance for a given vehicle registration via API.
    Now with caching and optimized for speed!
    
    Args:
        registration: Vehicle registration number
        
    Returns:
        JSON response with compliance data
    """
    start_time = time.time()
    
    try:
        # Clean registration input
        registration = registration.strip().upper().replace(" ", "")
        
        # Validate registration format (basic UK format check)
        if not registration or len(registration) < 2 or len(registration) > 8:
            raise HTTPException(status_code=400, detail="Invalid registration format")
        
        # Check cache first
        cached_result = get_cached_result(registration)
        if cached_result:
            logger.info(f"Cache hit for {registration} - response time: {time.time() - start_time:.3f}s")
            return cached_result.model_dump() if hasattr(cached_result, 'model_dump') else cached_result
        
        # Get compliance data with timeout
        try:
            result = await asyncio.wait_for(
                check_ulez_compliance(registration), 
                timeout=15.0  # 15 second timeout
            )
            
            # Cache the result
            cache_result(registration, result)
            
            response_time = time.time() - start_time
            logger.info(f"API response for {registration} - response time: {response_time:.3f}s")
            
            # Return the result as a dictionary for proper JSON serialization
            return result.model_dump() if hasattr(result, 'model_dump') else result
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout checking compliance for {registration}")
            raise HTTPException(status_code=504, detail="Request timeout - please try again")
        
    except ValueError as e:
        logger.warning(f"Invalid registration: {registration} - {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Error checking compliance for {registration}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error checking compliance")


@app.get("/{registration}", response_class=HTMLResponse)
async def check_compliance_html(request: Request, registration: str):
    """
    Check emission zone compliance and return HTML result page
    
    Args:
        request: FastAPI request object
        registration: Vehicle registration number
        
    Returns:
        HTML response with compliance data
    """
    start_time = time.time()
    
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
        
        # Check cache first
        cached_result = get_cached_result(registration)
        if cached_result:
            logger.info(f"Cache hit for {registration} (HTML) - response time: {time.time() - start_time:.3f}s")
            return templates.TemplateResponse("result.html", {"request": request, "result": cached_result})
        
        # Get compliance data with timeout
        try:
            result = await asyncio.wait_for(
                check_ulez_compliance(registration), 
                timeout=15.0  # 15 second timeout
            )
            
            # Cache the result
            cache_result(registration, result)
            
            response_time = time.time() - start_time
            logger.info(f"API response for {registration} (HTML) - response time: {response_time:.3f}s")
            
            return templates.TemplateResponse("result.html", {"request": request, "result": result})
            
        except asyncio.TimeoutError:
            return templates.TemplateResponse(
                "result.html", 
                {
                    "request": request,
                    "error": "Request timeout - please try again",
                    "registration": registration
                }
            )
            
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
    port = int(os.environ.get("PORT", 5005))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
