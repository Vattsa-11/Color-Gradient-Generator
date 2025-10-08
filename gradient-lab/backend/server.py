"""
FastAPI server for Gradient Lab - Color Gradient Generator
Provides web interface and API endpoints for gradient generation and image export.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional
from PIL import Image
import math
import io
import sys
import os

# Import color utilities directly since they're in the same directory now
from color_utils import build_palette, css_gradient, hex_to_rgb

app = FastAPI(
    title="Gradient Lab API",
    description="A modern Color Gradient Generator with real-time preview and export capabilities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Mount static files from frontend directory
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")
app.mount("/img", StaticFiles(directory=os.path.join(frontend_path, "img")), name="img")

# Templates - we'll serve the index.html directly
templates = None


# Pydantic models for request/response validation
class ColorStop(BaseModel):
    color: str = Field(..., pattern=r'^#[0-9A-Fa-f]{6}$', description="Hex color code like #FF0000")
    position: float = Field(..., ge=0, le=100, description="Position percentage (0-100)")


class GradientRequest(BaseModel):
    stops: List[ColorStop] = Field(..., description="Color stops")
    steps: int = Field(32, ge=2, le=1024, description="Number of gradient steps")
    space: Literal["rgb", "hsl", "hsv"] = Field("rgb", description="Color interpolation space")
    type: Literal["linear", "radial", "conic"] = Field("linear", description="Gradient type")
    angle: int = Field(90, ge=0, le=360, description="Gradient angle in degrees")

    @validator('stops')
    def validate_stops_positions(cls, v):
        # Validate length constraints
        if len(v) < 2:
            raise ValueError("At least 2 color stops are required")
        if len(v) > 12:
            raise ValueError("Maximum 12 color stops allowed")
        # Ensure positions are in ascending order (optional, we can sort them)
        return sorted(v, key=lambda x: x.position)


class ExportRequest(GradientRequest):
    width: int = Field(1920, ge=32, le=8192, description="Export image width")
    height: int = Field(1080, ge=32, le=8192, description="Export image height")
    format: Literal["png"] = Field("png", description="Export format")


class GradientResponse(BaseModel):
    colors: List[str] = Field(..., description="Generated color palette")
    css: str = Field(..., description="CSS gradient string")
    meta: dict = Field(..., description="Gradient metadata")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")





def create_gradient_image(stops: List[ColorStop], steps: int, space: str, gradient_type: str, angle: int, width: int, height: int) -> Image.Image:
    """Create a gradient image using PIL."""
    # Convert Pydantic models to dict format for color_utils
    stops_dict = [{"color": stop.color, "position": stop.position} for stop in stops]
    
    # Generate color palette
    palette = build_palette(stops_dict, steps, space)
    
    # Create image
    image = Image.new('RGB', (width, height))
    
    if gradient_type == 'linear':
        # Linear gradient
        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        # Calculate gradient vector
        if abs(cos_angle) > abs(sin_angle):
            # More horizontal
            length = width / abs(cos_angle)
        else:
            # More vertical
            length = height / abs(sin_angle)
        
        pixels = []
        for y in range(height):
            for x in range(width):
                # Project point onto gradient line
                # Normalize coordinates to center
                nx = (x - width / 2) / (width / 2)
                ny = (y - height / 2) / (height / 2)
                
                # Calculate position along gradient
                t = (nx * cos_angle + ny * sin_angle + 1) / 2
                t = max(0, min(1, t))  # Clamp to [0, 1]
                
                # Get color from palette
                color_index = int(t * (len(palette) - 1))
                color_index = max(0, min(len(palette) - 1, color_index))
                
                pixels.append(hex_to_rgb(palette[color_index]))
        
        # Set pixels efficiently
        image.putdata(pixels)
    
    elif gradient_type == 'radial':
        # Radial gradient
        center_x, center_y = width // 2, height // 2
        max_radius = math.sqrt(center_x**2 + center_y**2)
        
        pixels = []
        for y in range(height):
            for x in range(width):
                # Calculate distance from center
                dx = x - center_x
                dy = y - center_y
                distance = math.sqrt(dx**2 + dy**2)
                
                # Normalize to [0, 1]
                t = distance / max_radius
                t = max(0, min(1, t))
                
                # Get color from palette
                color_index = int(t * (len(palette) - 1))
                color_index = max(0, min(len(palette) - 1, color_index))
                
                pixels.append(hex_to_rgb(palette[color_index]))
        
        image.putdata(pixels)
    
    elif gradient_type == 'conic':
        # Conic gradient
        center_x, center_y = width // 2, height // 2
        start_angle_rad = math.radians(angle)
        
        pixels = []
        for y in range(height):
            for x in range(width):
                # Calculate angle from center
                dx = x - center_x
                dy = y - center_y
                
                if dx == 0 and dy == 0:
                    pixel_angle = 0
                else:
                    pixel_angle = math.atan2(dy, dx)
                
                # Adjust for start angle and normalize to [0, 2π]
                adjusted_angle = (pixel_angle - start_angle_rad) % (2 * math.pi)
                
                # Normalize to [0, 1]
                t = adjusted_angle / (2 * math.pi)
                
                # Get color from palette
                color_index = int(t * (len(palette) - 1))
                color_index = max(0, min(len(palette) - 1, color_index))
                
                pixels.append(hex_to_rgb(palette[color_index]))
        
        image.putdata(pixels)
    
    return image


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve the main application page."""
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
    index_path = os.path.join(frontend_path, "index.html")
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return HTMLResponse(content=content)


@app.get("/test", response_class=HTMLResponse)
async def test_page():
    """Test page to check if static files are working."""
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <body>
        <h1>Test Page</h1>
        <p>If you can see this styled correctly, static files are working!</p>
        <script src="/js/app.js"></script>
        <script>console.log('JavaScript is working!');</script>
    </body>
    </html>
    """)


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post("/api/gradient", response_model=GradientResponse)
async def generate_gradient(gradient_request: GradientRequest):
    """Generate gradient palette and CSS."""
    try:
        # Convert Pydantic models to dict format for color_utils
        stops_dict = [{"color": stop.color, "position": stop.position} for stop in gradient_request.stops]
        
        # Generate palette
        colors = build_palette(stops_dict, gradient_request.steps, gradient_request.space)
        
        # Generate CSS
        css = css_gradient(stops_dict, gradient_request.type, gradient_request.angle)
        
        return GradientResponse(
            colors=colors,
            css=f"background: {css};",
            meta={
                "space": gradient_request.space,
                "type": gradient_request.type,
                "angle": gradient_request.angle,
                "steps": gradient_request.steps
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export")
async def export_gradient(export_request: ExportRequest):
    """Export gradient as PNG image."""
    try:
        # Create gradient image
        image = create_gradient_image(
            export_request.stops,
            256,  # High quality for export
            export_request.space,
            export_request.type,
            export_request.angle,
            export_request.width,
            export_request.height
        )
        
        # Save to memory buffer
        buffer = io.BytesIO()
        image.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        
        # Create filename
        filename = f'gradient_{export_request.type}_{export_request.width}x{export_request.height}.png'
        
        return StreamingResponse(
            io.BytesIO(buffer.read()),
            media_type='image/png',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    print("Starting Gradient Lab server...")
    print("Open http://127.0.0.1:8000/ in your browser")
    print("API Documentation: http://127.0.0.1:8000/api/docs")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)