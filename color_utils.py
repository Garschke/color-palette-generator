import numpy as np
from PIL import Image
from collections import defaultdict

# Web-safe X11 colors (subset)
X11_COLORS = {
    '#FFFFFF': 'White',
    '#C0C0C0': 'Silver',
    '#808080': 'Gray',
    '#000000': 'Black',
    '#FF0000': 'Red',
    '#800000': 'Maroon',
    '#FFFF00': 'Yellow',
    '#808000': 'Olive',
    '#00FF00': 'Lime',
    '#008000': 'Green',
    '#00FFFF': 'Aqua',
    '#008080': 'Teal',
    '#0000FF': 'Blue',
    '#000080': 'Navy',
    '#FF00FF': 'Fuchsia',
    '#800080': 'Purple'
}

def rgb_to_hex(rgb):
    """Convert RGB tuple to hexadecimal color code"""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def closest_x11_color(rgb):
    """Find the closest X11 web-safe color for a given RGB"""
    hex_color = rgb_to_hex(rgb)

    # If exact match exists, return it
    if hex_color in X11_COLORS:
        return hex_color, X11_COLORS[hex_color]

    # Otherwise find the closest color
    r, g, b = rgb
    min_distance = float('inf')
    closest_color = None

    for x11_hex in X11_COLORS:
        x11_rgb = tuple(int(x11_hex[i:i+2], 16) for i in (1, 3, 5))

        # Calculate Euclidean distance between colors
        distance = sum((c1 - c2)**2 for c1, c2 in zip(rgb, x11_rgb))**0.5

        if distance < min_distance:
            min_distance = distance
            closest_color = x11_hex

    return closest_color, X11_COLORS[closest_color]

def extract_colors(image_path, num_colors=10):
    """Extract the most common colors from an image"""
    # Open image and convert to numpy array
    img = Image.open(image_path)
    img = img.convert('RGB')
    arr = np.array(img)

    # Reshape array to 2D (pixels x RGB)
    pixels = arr.reshape(-1, 3)

    # Count color frequencies
    color_counts = defaultdict(int)
    for pixel in pixels:
        # Round to nearest X11 color
        hex_color, _ = closest_x11_color(tuple(pixel))
        color_counts[hex_color] += 1

    # Sort by frequency and get top colors
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    top_colors = sorted_colors[:num_colors]

    # Prepare result with color name and percentage
    total_pixels = len(pixels)
    result = []
    for hex_color, count in top_colors:
        percentage = round((count / total_pixels) * 100, 2)
        result.append({
            'hex': hex_color,
            'name': X11_COLORS[hex_color],
            'percentage': percentage
        })

    return result
