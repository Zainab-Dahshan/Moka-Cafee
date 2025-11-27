from PIL import Image, ImageDraw, ImageFont
import os

def create_logo():
    # Create a new image with a transparent background
    width, height = 400, 200
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Define colors
    coffee_brown = (111, 78, 55)
    creamy_latte = (193, 154, 107)
    
    # Draw a coffee cup shape
    cup_color = coffee_brown
    rim_color = (85, 65, 50)
    
    # Cup body (trapezoid shape)
    cup_points = [
        (width//2 - 100, height//2 - 30),  # Top-left
        (width//2 + 100, height//2 - 30),  # Top-right
        (width//2 + 70, height//2 + 70),   # Bottom-right
        (width//2 - 70, height//2 + 70)    # Bottom-left
    ]
    
    # Draw the cup
    draw.polygon(cup_points, fill=cup_color, outline=rim_color, width=3)
    
    # Draw the coffee inside
    coffee_points = [
        (width//2 - 90, height//2 - 20),  # Top-left
        (width//2 + 90, height//2 - 20),  # Top-right
        (width//2 + 65, height//2 + 60),  # Bottom-right
        (width//2 - 65, height//2 + 60)   # Bottom-left
    ]
    draw.polygon(coffee_points, fill=creamy_latte)
    
    # Add steam
    steam_color = (200, 200, 200, 180)
    for i in range(3):
        x = width//2 - 40 + i * 40
        draw.ellipse((x, height//2 - 60, x + 20, height//2 - 40), fill=steam_color)
    
    # Add text
    try:
        # Try to use a nice font if available, fallback to default
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
    
    text = "CaféLuxe"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Position text below the logo
    text_x = (width - text_width) // 2
    text_y = height//2 + 90
    
    # Draw text with shadow for better visibility
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 150), font=font)
    draw.text((text_x, text_y), text, fill=coffee_brown, font=font)
    
    # Add a small coffee bean
    draw.ellipse((width//2 - 5, height//2 + 130, width//2 + 5, height//2 + 140), fill=coffee_brown)
    
    # Create images directory if it doesn't exist
    os.makedirs("static/images", exist_ok=True)
    
    # Save the image
    image_path = "static/images/logo.png"
    image.save(image_path)
    print(f"Logo created successfully at: {image_path}")

if __name__ == "__main__":
    create_logo()
