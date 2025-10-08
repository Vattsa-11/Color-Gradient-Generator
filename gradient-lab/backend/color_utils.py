"""
Color utility functions for gradient generation and color space conversions.
Supports RGB, HSL, and HSV color spaces with smooth interpolation.
"""

import colorsys
import math
from typing import List, Tuple, Dict, Any


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Convert hex color string to RGB tuple.
    
    Args:
        hex_color: Hex color string like '#FF0000' or 'FF0000'
        
    Returns:
        RGB tuple (r, g, b) with values 0-255
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex color string.
    
    Args:
        r, g, b: RGB values (0-255)
        
    Returns:
        Hex color string like '#FF0000'
    """
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB to HSL color space.
    
    Args:
        r, g, b: RGB values (0-255)
        
    Returns:
        HSL tuple (h, s, l) where h is 0-360, s and l are 0-100
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (h * 360, s * 100, l * 100)


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """Convert HSL to RGB color space.
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-100)
        l: Lightness (0-100)
        
    Returns:
        RGB tuple (r, g, b) with values 0-255
    """
    h, s, l = h / 360.0, s / 100.0, l / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (int(r * 255), int(g * 255), int(b * 255))


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB to HSV color space.
    
    Args:
        r, g, b: RGB values (0-255)
        
    Returns:
        HSV tuple (h, s, v) where h is 0-360, s and v are 0-100
    """
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (h * 360, s * 100, v * 100)


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """Convert HSV to RGB color space.
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-100)
        v: Value (0-100)
        
    Returns:
        RGB tuple (r, g, b) with values 0-255
    """
    h, s, v = h / 360.0, s / 100.0, v / 100.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(r * 255), int(g * 255), int(b * 255))


def interpolate_hue(h1: float, h2: float, t: float) -> float:
    """Interpolate between two hue values using shortest arc.
    
    Args:
        h1, h2: Hue values (0-360)
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated hue value (0-360)
    """
    # Normalize hues to 0-360
    h1 = h1 % 360
    h2 = h2 % 360
    
    # Calculate the shortest distance
    diff = h2 - h1
    if abs(diff) > 180:
        if diff > 0:
            h1 += 360
        else:
            h2 += 360
    
    # Interpolate and normalize result
    result = h1 + (h2 - h1) * t
    return result % 360


def interpolate_rgb(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """Interpolate between two RGB colors.
    
    Args:
        color1, color2: RGB tuples (r, g, b)
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated RGB tuple
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    
    return (r, g, b)


def interpolate_hsl(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """Interpolate between two colors in HSL space.
    
    Args:
        color1, color2: RGB tuples (r, g, b)
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated RGB tuple
    """
    h1, s1, l1 = rgb_to_hsl(*color1)
    h2, s2, l2 = rgb_to_hsl(*color2)
    
    h = interpolate_hue(h1, h2, t)
    s = s1 + (s2 - s1) * t
    l = l1 + (l2 - l1) * t
    
    return hsl_to_rgb(h, s, l)


def interpolate_hsv(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    """Interpolate between two colors in HSV space.
    
    Args:
        color1, color2: RGB tuples (r, g, b)
        t: Interpolation factor (0-1)
        
    Returns:
        Interpolated RGB tuple
    """
    h1, s1, v1 = rgb_to_hsv(*color1)
    h2, s2, v2 = rgb_to_hsv(*color2)
    
    h = interpolate_hue(h1, h2, t)
    s = s1 + (s2 - s1) * t
    v = v1 + (v2 - v1) * t
    
    return hsv_to_rgb(h, s, v)


def build_palette(stops: List[Dict[str, Any]], steps: int, space: str = "rgb") -> List[str]:
    """Build a color palette by interpolating between color stops.
    
    Args:
        stops: List of color stops with 'color' (hex) and 'position' (0-100)
        steps: Number of colors in the final palette
        space: Color space for interpolation ('rgb', 'hsl', 'hsv')
        
    Returns:
        List of hex color strings
    """
    if len(stops) < 2:
        raise ValueError("At least 2 color stops are required")
    
    # Sort stops by position
    sorted_stops = sorted(stops, key=lambda x: x['position'])
    
    # Convert hex colors to RGB
    rgb_stops = [(hex_to_rgb(stop['color']), stop['position']) for stop in sorted_stops]
    
    # Choose interpolation function
    interpolate_func = {
        'rgb': interpolate_rgb,
        'hsl': interpolate_hsl,
        'hsv': interpolate_hsv
    }.get(space, interpolate_rgb)
    
    palette = []
    
    for i in range(steps):
        # Calculate position in the gradient (0-100)
        position = (i / (steps - 1)) * 100 if steps > 1 else 0
        
        # Find the two stops to interpolate between
        if position <= rgb_stops[0][1]:
            # Before first stop
            color = rgb_stops[0][0]
        elif position >= rgb_stops[-1][1]:
            # After last stop
            color = rgb_stops[-1][0]
        else:
            # Between two stops
            for j in range(len(rgb_stops) - 1):
                if rgb_stops[j][1] <= position <= rgb_stops[j + 1][1]:
                    # Interpolate between stops j and j+1
                    color1, pos1 = rgb_stops[j]
                    color2, pos2 = rgb_stops[j + 1]
                    
                    if pos2 == pos1:
                        t = 0
                    else:
                        t = (position - pos1) / (pos2 - pos1)
                    
                    color = interpolate_func(color1, color2, t)
                    break
        
        palette.append(rgb_to_hex(*color))
    
    return palette


def css_gradient(stops: List[Dict[str, Any]], gradient_type: str = "linear", angle: int = 90) -> str:
    """Generate CSS gradient string from color stops.
    
    Args:
        stops: List of color stops with 'color' (hex) and 'position' (0-100)
        gradient_type: Type of gradient ('linear', 'radial', 'conic')
        angle: Angle for linear/conic gradients (0-360 degrees)
        
    Returns:
        CSS gradient string
    """
    # Sort stops by position
    sorted_stops = sorted(stops, key=lambda x: x['position'])
    
    # Format color stops for CSS
    css_stops = []
    for stop in sorted_stops:
        pos = round(stop['position'], 2)
        css_stops.append(f"{stop['color']} {pos}%")
    
    stops_str = ", ".join(css_stops)
    
    if gradient_type == "linear":
        return f"linear-gradient({angle}deg, {stops_str})"
    elif gradient_type == "radial":
        return f"radial-gradient(circle, {stops_str})"
    elif gradient_type == "conic":
        return f"conic-gradient(from {angle}deg, {stops_str})"
    else:
        # Default to linear
        return f"linear-gradient({angle}deg, {stops_str})"


def calculate_luminance(hex_color: str) -> float:
    """Calculate relative luminance of a color for contrast calculations.
    
    Args:
        hex_color: Hex color string like '#FF0000'
        
    Returns:
        Relative luminance (0-1)
    """
    r, g, b = hex_to_rgb(hex_color)
    
    # Convert to linear RGB
    def linearize(c):
        c = c / 255.0
        if c <= 0.03928:
            return c / 12.92
        else:
            return pow((c + 0.055) / 1.055, 2.4)
    
    r_lin = linearize(r)
    g_lin = linearize(g)
    b_lin = linearize(b)
    
    # Calculate luminance
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def contrast_ratio(color1: str, color2: str) -> float:
    """Calculate contrast ratio between two colors.
    
    Args:
        color1, color2: Hex color strings
        
    Returns:
        Contrast ratio (1-21)
    """
    lum1 = calculate_luminance(color1)
    lum2 = calculate_luminance(color2)
    
    # Ensure lighter color is in numerator
    if lum1 < lum2:
        lum1, lum2 = lum2, lum1
    
    return (lum1 + 0.05) / (lum2 + 0.05)


if __name__ == "__main__":
    # Simple self-tests
    print("Testing color utilities...")
    
    # Test hex <-> RGB conversion
    assert hex_to_rgb("#FF0000") == (255, 0, 0)
    assert rgb_to_hex(255, 0, 0) == "#ff0000"
    
    # Test color space conversions
    r, g, b = 255, 128, 0
    h, s, l = rgb_to_hsl(r, g, b)
    r2, g2, b2 = hsl_to_rgb(h, s, l)
    assert abs(r - r2) <= 1 and abs(g - g2) <= 1 and abs(b - b2) <= 1
    
    # Test palette generation
    stops = [
        {"color": "#FF0000", "position": 0},
        {"color": "#0000FF", "position": 100}
    ]
    palette = build_palette(stops, 5, "rgb")
    assert len(palette) == 5
    assert palette[0] == "#ff0000"
    assert palette[-1] == "#0000ff"
    
    # Test CSS generation
    css = css_gradient(stops, "linear", 90)
    assert "linear-gradient(90deg" in css
    assert "#FF0000 0%" in css
    assert "#0000FF 100%" in css
    
    print("All tests passed!")