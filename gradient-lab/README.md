# 🎨 Gradient Lab

**A modern, interactive Color Gradient Generator with real-time preview and export capabilities**

Craft, test, and export beautiful color gradients with a polished web UI and a Python backend. Gradient Lab helps you design multi-stop gradients, preview them live, copy CSS, and export high‑resolution images.

## ✨ Features

- 🎯 **Interactive UI**: Responsive design with light/dark theme support
- 🎨 **Color Management**: Add, remove, and reorder color stops with precise positioning (0–100%)
- 📐 **Multiple Gradient Types**: Linear, radial, and conic gradients
- 🌈 **Advanced Color Interpolation**: RGB, HSL, HSV color spaces with smart hue wrap-around
- 👁️ **Live Preview**: Real-time gradient preview with instant CSS generation
- ⚡ **Quick Actions**: Randomize palette, reverse stops, equalize spacing
- 📸 **High-Quality Export**: Export PNG images at custom resolutions (up to 8K)
- ♿ **Accessibility**: ARIA labels, keyboard navigation, and contrast indicators
- 📱 **Mobile-Friendly**: Fully responsive design that works on all devices

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python with FastAPI framework
- **Image Processing**: Pillow (PIL) for PNG export
- **Server**: Uvicorn ASGI server with hot-reload
- **API Documentation**: Auto-generated Swagger UI and ReDoc

## 🚀 Getting Started

### Prerequisites

- Python 3.11+ (recommended)
- pip package manager

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd gradient-lab
   ```

2. **Create a virtual environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate it
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   # Navigate to backend directory
   cd backend
   python server.py
   ```

5. **Open in browser**
   
   Navigate to: **http://127.0.0.1:8000/**

🎉 **That's it!** Your gradient generator is now running locally.

## 📖 How to Use

### 1. 🎨 **Managing Color Stops**
- Click **"+ Add Stop"** to create new color points
- Use the **color picker** to choose colors
- Drag the **position slider** to adjust placement (0–100%)
- **Remove stops** with the delete button (minimum 2 required)

### 2. 📐 **Gradient Types**
- **Linear**: Traditional directional gradients with adjustable angle (0–360°)
- **Radial**: Circular gradients expanding from center
- **Conic**: Rotational gradients with customizable start angle

### 3. 🌈 **Color Interpolation**
- **RGB**: Direct color mixing (simple, fast)
- **HSL**: Hue-Saturation-Lightness (smoother transitions)
- **HSV**: Hue-Saturation-Value (vibrant color blending)

### 4. ⚡ **Quick Actions**
- **🎲 Randomize**: Generate random color palette
- **🔄 Reverse**: Flip the gradient direction
- **⚖️ Equalize**: Distribute stops evenly

### 5. 📋 **Export Options**
- **Copy CSS**: Get ready-to-use CSS code
- **Download PNG**: Export high-resolution images (32px to 8K)

## 🔌 API Reference

The application provides a RESTful API for programmatic gradient generation.

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### Health Check
```http
GET /health
```
**Response:**
```json
{ "status": "ok" }
```

#### Generate Gradient
```http
POST /api/gradient
```

**Request Body:**
```json
{
  "stops": [
    { "color": "#ff6b6b", "position": 0 },
    { "color": "#ffd93d", "position": 50 },
    { "color": "#6bcb77", "position": 100 }
  ],
  "steps": 32,
  "space": "hsl",
  "type": "linear",
  "angle": 135
}
```

**Response:**
```json
{
  "colors": ["#ff6b6b", "#ff7b5a", "..."],
  "css": "background: linear-gradient(135deg, #ff6b6b 0%, #ffd93d 50%, #6bcb77 100%);",
  "meta": { "space": "hsl", "type": "linear", "angle": 135, "steps": 32 }
}
```

**Validation Rules:**
- `stops`: 2-12 color stops with hex colors (#RRGGBB) and positions (0-100)
- `steps`: 2-1024 gradient steps
- `space`: `rgb` | `hsl` | `hsv`
- `type`: `linear` | `radial` | `conic`
- `angle`: 0-360 degrees (for linear/conic)

#### Export Image
```http
POST /api/export
```

**Request Body:**
```json
{
  "stops": [
    { "color": "#ff0000", "position": 0 },
    { "color": "#0000ff", "position": 100 }
  ],
  "steps": 256,
  "space": "hsl",
  "type": "linear",
  "angle": 90,
  "width": 1920,
  "height": 1080,
  "format": "png"
}
```

**Response:** Binary PNG image file with appropriate headers for download.

**Additional Validation:**
- `width`/`height`: 32-8192 pixels
- `format`: Currently only `png` supported

### Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/api/docs
- **ReDoc**: http://127.0.0.1:8000/api/redoc

These interfaces allow you to test endpoints directly from your browser with request/response examples and automatic validation.

### Example Usage

**cURL Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/gradient \
  -H "Content-Type: application/json" \
  -d '{
    "stops": [
      {"color": "#ff0000", "position": 0},
      {"color": "#0000ff", "position": 100}
    ],
    "steps": 8,
    "space": "hsl",
    "type": "linear",
    "angle": 90
  }'
```

## 🎯 Advanced Features

### Color Mathematics & Interpolation

- **Color Space Conversions**: Seamless conversion between HEX ↔ RGB ↔ HSL ↔ HSV
- **Smart Hue Interpolation**: HSL/HSV use shortest-arc blending (350° to 10° = 20° forward, not 340° backward)
- **Anti-Banding**: High-quality interpolation algorithms minimize color banding
- **Precision Control**: Configurable step count (2-1024) for smooth or discrete effects

### User Experience

- **Theme System**: Automatic dark/light mode detection with manual override
- **Keyboard Shortcuts**: Full keyboard navigation support
- **State Persistence**: Automatically saves your work to browser localStorage
- **Responsive Design**: Mobile-first approach with touch-friendly controls
- **Accessibility**: WCAG 2.1 compliant with screen reader support

### Performance Optimizations

- **Debounced Updates**: Smooth real-time preview without overwhelming the API
- **Efficient Rendering**: Optimized CSS and JavaScript for fast interaction
- **Memory Management**: Smart cleanup of event listeners and API calls
- **Progressive Enhancement**: Core functionality works even with JavaScript disabled

## 🛠️ Development

### Architecture Overview

**Frontend Structure:**
- `frontend/index.html` - Main application interface
- `frontend/css/styles.css` - Complete styling with CSS variables and themes
- `frontend/js/app.js` - Application logic with modular class-based architecture

**Backend Structure:**
- `backend/server.py` - FastAPI application with async endpoints
- `backend/color_utils.py` - Color conversion and interpolation utilities
- `backend/requirements.txt` - Python dependencies

### Key Features Implementation

- **Real-time Preview**: Debounced API calls with fallback CSS generation
- **Color Interpolation**: Mathematical algorithms for smooth color transitions
- **Image Export**: PIL-based high-resolution image generation
- **API Validation**: Pydantic models for robust request/response handling

## 🎨 Color Science

### Interpolation Spaces

- **RGB**: Linear interpolation per channel - simple but can produce muddy mid-tones
- **HSL**: Hue-Saturation-Lightness - perceptually smooth with natural hue transitions
- **HSV**: Hue-Saturation-Value - vibrant colors with maintained saturation

### Best Practices

- Use **HSL** for natural color transitions (sunsets, rainbows)
- Use **RGB** for technical/precise color matching
- Use **HSV** for vibrant, saturated gradients
- Keep **step count** between 32-128 for optimal file size vs. quality balance

## 📱 Browser Support

- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Mobile**: iOS Safari 14+, Chrome Mobile 90+
- **Features**: CSS Grid, CSS Variables, Fetch API, ES6+ JavaScript
- **Fallbacks**: Graceful degradation for older browsers

## 🚀 Deployment

### Production Setup

1. **Environment Configuration**
   ```bash
   # Production environment variables
   export ENVIRONMENT=production
   export HOST=0.0.0.0
   export PORT=8000
   ```

2. **Security Considerations**
   - Enable HTTPS in production
   - Configure CORS policies for your domain
   - Set up rate limiting for API endpoints
   - Use environment variables for sensitive configuration

3. **Performance Optimization**
   - Enable gzip compression
   - Use a reverse proxy (nginx/Apache)
   - Configure static file caching
   - Monitor memory usage for large image exports

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with proper testing
4. **Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **Push to the branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Add JSDoc comments for functions
- Include unit tests for new features
- Update documentation as needed

## 📋 Roadmap

### Upcoming Features

- [ ] **Color Palette Generator**: AI-powered color palette creation with various themes (complementary, analogous, triadic, monochromatic) and mood-based suggestions
- [ ] **SVG Export**: Scalable vector graphics output
- [ ] **Color Palette Sharing**: URL-based palette sharing
- [ ] **Batch Export**: Multiple resolution exports
- [ ] **Advanced Color Spaces**: OKLab, OKLCH support
- [ ] **Animation**: Animated gradient transitions
- [ ] **Presets**: Built-in gradient libraries
- [ ] **Plugin System**: Extensible architecture

### Performance Improvements

- [ ] **WebGL Rendering**: GPU-accelerated preview
- [ ] **Worker Threads**: Background image processing
- [ ] **Caching**: Intelligent result caching
- [ ] **Compression**: Optimized image output

## 🐛 Troubleshooting

### Common Issues

**Q: Colors look muddy in RGB mode**
- **Solution**: Switch to HSL or HSV interpolation for smoother hue transitions

**Q: Large exports are slow**
- **Solution**: Reduce image dimensions or step count. Consider using fewer color stops

**Q: CSS not loading**
- **Solution**: Ensure you're accessing via http://127.0.0.1:8000/ not opening HTML file directly

**Q: API requests failing**
- **Solution**: Check that the FastAPI server is running and accessible

### Debug Mode

Enable debug logging by setting:
```bash
export DEBUG=true
```

This provides detailed console output for troubleshooting.

## 📄 License

**MIT License**

Copyright (c) 2025 Gradient Lab

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 🙏 Acknowledgments

- **Design Inspiration**: Modern gradient tools and color theory principles
- **Accessibility**: WCAG guidelines and inclusive design practices
- **Performance**: Web performance best practices and optimization techniques
- **Color Science**: Research in perceptual color spaces and interpolation algorithms

---

**Made with ❤️ for designers and developers who love beautiful gradients**