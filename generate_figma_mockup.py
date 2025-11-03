"""
Generate Figma Mockup for AI Medical Diagnosis System
Creates visual mockups that match the actual Streamlit implementation
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Colors from design spec
COLORS = {
    'primary_purple': '#667eea',
    'secondary_purple': '#764ba2',
    'light_blue': '#e3f2fd',
    'light_purple': '#f3e5f5',
    'warning_yellow': '#fff3cd',
    'warning_border': '#ff9800',
    'background_gray': '#f5f7fa',
    'text_dark': '#333333',
    'text_gray': '#666666',
    'white': '#ffffff',
    'user_msg_border': '#2196f3',
    'ai_msg_border': '#9c27b0',
}

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient(draw, bounds, start_color, end_color, direction='horizontal'):
    """Create gradient effect"""
    x1, y1, x2, y2 = bounds
    if direction == 'horizontal':
        for i in range(x1, x2):
            ratio = (i - x1) / (x2 - x1)
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(i, y1), (i, y2)], fill=(r, g, b))
    else:  # vertical
        for i in range(y1, y2):
            ratio = (i - y1) / (y2 - y1)
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(x1, i), (x2, i)], fill=(r, g, b))

def draw_rounded_rectangle(draw, bounds, radius, fill, outline=None, width=1):
    """Draw rounded rectangle"""
    x1, y1, x2, y2 = bounds
    
    # Draw main rectangle
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # Draw corners
    draw.pieslice([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=fill)
    
    if outline:
        # Draw outline
        draw.arc([x1, y1, x1 + 2*radius, y1 + 2*radius], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y1, x2, y1 + 2*radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2*radius, x1 + 2*radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2*radius, y2 - 2*radius, x2, y2], 0, 90, fill=outline, width=width)
        draw.line([(x1 + radius, y1), (x2 - radius, y1)], fill=outline, width=width)
        draw.line([(x1 + radius, y2), (x2 - radius, y2)], fill=outline, width=width)
        draw.line([(x1, y1 + radius), (x1, y2 - radius)], fill=outline, width=width)
        draw.line([(x2, y1 + radius), (x2, y2 - radius)], fill=outline, width=width)

def create_desktop_mockup():
    """Create desktop mockup (1440x1024)"""
    width, height = 1440, 1024
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['background_gray']))
    draw = ImageDraw.Draw(img)
    
    # Sidebar (300px wide)
    sidebar_width = 300
    create_gradient(
        draw,
        (0, 0, sidebar_width, height),
        hex_to_rgb(COLORS['primary_purple']),
        hex_to_rgb(COLORS['secondary_purple']),
        direction='vertical'
    )
    
    # Main content area
    content_x = sidebar_width + 40
    content_width = width - sidebar_width - 80
    
    # Header with gradient
    header_y = 40
    header_height = 120
    header_img = Image.new('RGBA', (content_width, header_height), (0, 0, 0, 0))
    header_draw = ImageDraw.Draw(header_img)
    
    # Create gradient for header
    for i in range(content_width):
        ratio = i / content_width
        r = int(hex_to_rgb(COLORS['primary_purple'])[0] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[0] * ratio)
        g = int(hex_to_rgb(COLORS['primary_purple'])[1] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[1] * ratio)
        b = int(hex_to_rgb(COLORS['primary_purple'])[2] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[2] * ratio)
        header_draw.line([(i, 0), (i, header_height)], fill=(r, g, b, 255))
    
    # Round corners
    mask = Image.new('L', (content_width, header_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, content_width, header_height], radius=15, fill=255)
    
    # Apply mask
    header_img.putalpha(mask)
    img.paste(header_img, (content_x, header_y), header_img)
    
    # Warning box
    warning_y = header_y + header_height + 30
    warning_height = 80
    draw_rounded_rectangle(
        draw,
        (content_x, warning_y, content_x + content_width, warning_y + warning_height),
        radius=8,
        fill=hex_to_rgb(COLORS['warning_yellow'])
    )
    # Warning left border
    draw.rectangle(
        [content_x, warning_y + 8, content_x + 4, warning_y + warning_height - 8],
        fill=hex_to_rgb(COLORS['warning_border'])
    )
    
    # Chat messages
    msg_y = warning_y + warning_height + 40
    
    # AI Message
    ai_msg_height = 100
    draw_rounded_rectangle(
        draw,
        (content_x, msg_y, content_x + content_width, msg_y + ai_msg_height),
        radius=10,
        fill=hex_to_rgb(COLORS['light_purple'])
    )
    draw.rectangle(
        [content_x, msg_y + 10, content_x + 4, msg_y + ai_msg_height - 10],
        fill=hex_to_rgb(COLORS['ai_msg_border'])
    )
    
    # User Message
    user_msg_y = msg_y + ai_msg_height + 20
    user_msg_height = 80
    draw_rounded_rectangle(
        draw,
        (content_x, user_msg_y, content_x + content_width, user_msg_y + user_msg_height),
        radius=10,
        fill=hex_to_rgb(COLORS['light_blue'])
    )
    draw.rectangle(
        [content_x, user_msg_y + 10, content_x + 4, user_msg_y + user_msg_height - 10],
        fill=hex_to_rgb(COLORS['user_msg_border'])
    )
    
    # Another AI Message
    ai_msg_y2 = user_msg_y + user_msg_height + 20
    ai_msg_height2 = 120
    draw_rounded_rectangle(
        draw,
        (content_x, ai_msg_y2, content_x + content_width, ai_msg_y2 + ai_msg_height2),
        radius=10,
        fill=hex_to_rgb(COLORS['light_purple'])
    )
    draw.rectangle(
        [content_x, ai_msg_y2 + 10, content_x + 4, ai_msg_y2 + ai_msg_height2 - 10],
        fill=hex_to_rgb(COLORS['ai_msg_border'])
    )
    
    # Chat input at bottom
    input_y = height - 100
    input_height = 50
    draw_rounded_rectangle(
        draw,
        (content_x, input_y, content_x + content_width - 100, input_y + input_height),
        radius=8,
        fill=hex_to_rgb(COLORS['white']),
        outline=hex_to_rgb('#e0e0e0'),
        width=2
    )
    
    # Send button
    button_x = content_x + content_width - 90
    button_img = Image.new('RGBA', (80, input_height), (0, 0, 0, 0))
    button_draw = ImageDraw.Draw(button_img)
    
    for i in range(80):
        ratio = i / 80
        r = int(hex_to_rgb(COLORS['primary_purple'])[0] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[0] * ratio)
        g = int(hex_to_rgb(COLORS['primary_purple'])[1] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[1] * ratio)
        b = int(hex_to_rgb(COLORS['primary_purple'])[2] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[2] * ratio)
        button_draw.line([(i, 0), (i, input_height)], fill=(r, g, b, 255))
    
    mask = Image.new('L', (80, input_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, 80, input_height], radius=8, fill=255)
    button_img.putalpha(mask)
    img.paste(button_img, (button_x, input_y), button_img)
    
    return img

def create_mobile_mockup():
    """Create mobile mockup (375x812)"""
    width, height = 375, 812
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['background_gray']))
    draw = ImageDraw.Draw(img)
    
    margin = 20
    content_width = width - 2 * margin
    
    # Header
    header_y = 20
    header_height = 100
    header_img = Image.new('RGBA', (content_width, header_height), (0, 0, 0, 0))
    header_draw = ImageDraw.Draw(header_img)
    
    for i in range(content_width):
        ratio = i / content_width
        r = int(hex_to_rgb(COLORS['primary_purple'])[0] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[0] * ratio)
        g = int(hex_to_rgb(COLORS['primary_purple'])[1] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[1] * ratio)
        b = int(hex_to_rgb(COLORS['primary_purple'])[2] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[2] * ratio)
        header_draw.line([(i, 0), (i, header_height)], fill=(r, g, b, 255))
    
    mask = Image.new('L', (content_width, header_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, content_width, header_height], radius=15, fill=255)
    header_img.putalpha(mask)
    img.paste(header_img, (margin, header_y), header_img)
    
    # Warning box
    warning_y = header_y + header_height + 20
    warning_height = 70
    draw_rounded_rectangle(
        draw,
        (margin, warning_y, margin + content_width, warning_y + warning_height),
        radius=8,
        fill=hex_to_rgb(COLORS['warning_yellow'])
    )
    draw.rectangle(
        [margin, warning_y + 8, margin + 4, warning_y + warning_height - 8],
        fill=hex_to_rgb(COLORS['warning_border'])
    )
    
    # Chat messages
    msg_y = warning_y + warning_height + 30
    
    # AI Message
    ai_msg_height = 90
    draw_rounded_rectangle(
        draw,
        (margin, msg_y, margin + content_width, msg_y + ai_msg_height),
        radius=10,
        fill=hex_to_rgb(COLORS['light_purple'])
    )
    draw.rectangle(
        [margin, msg_y + 10, margin + 4, msg_y + ai_msg_height - 10],
        fill=hex_to_rgb(COLORS['ai_msg_border'])
    )
    
    # User Message
    user_msg_y = msg_y + ai_msg_height + 15
    user_msg_height = 70
    draw_rounded_rectangle(
        draw,
        (margin, user_msg_y, margin + content_width, user_msg_y + user_msg_height),
        radius=10,
        fill=hex_to_rgb(COLORS['light_blue'])
    )
    draw.rectangle(
        [margin, user_msg_y + 10, margin + 4, user_msg_y + user_msg_height - 10],
        fill=hex_to_rgb(COLORS['user_msg_border'])
    )
    
    # Another AI Message
    ai_msg_y2 = user_msg_y + user_msg_height + 15
    ai_msg_height2 = 100
    draw_rounded_rectangle(
        draw,
        (margin, ai_msg_y2, margin + content_width, ai_msg_y2 + ai_msg_height2),
        radius=10,
        fill=hex_to_rgb(COLORS['light_purple'])
    )
    draw.rectangle(
        [margin, ai_msg_y2 + 10, margin + 4, ai_msg_y2 + ai_msg_height2 - 10],
        fill=hex_to_rgb(COLORS['ai_msg_border'])
    )
    
    # Chat input
    input_y = height - 80
    input_height = 45
    draw_rounded_rectangle(
        draw,
        (margin, input_y, margin + content_width - 60, input_y + input_height),
        radius=8,
        fill=hex_to_rgb(COLORS['white']),
        outline=hex_to_rgb('#e0e0e0'),
        width=2
    )
    
    # Send button
    button_x = margin + content_width - 50
    button_img = Image.new('RGBA', (50, input_height), (0, 0, 0, 0))
    button_draw = ImageDraw.Draw(button_img)
    
    for i in range(50):
        ratio = i / 50
        r = int(hex_to_rgb(COLORS['primary_purple'])[0] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[0] * ratio)
        g = int(hex_to_rgb(COLORS['primary_purple'])[1] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[1] * ratio)
        b = int(hex_to_rgb(COLORS['primary_purple'])[2] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[2] * ratio)
        button_draw.line([(i, 0), (i, input_height)], fill=(r, g, b, 255))
    
    mask = Image.new('L', (50, input_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, 50, input_height], radius=8, fill=255)
    button_img.putalpha(mask)
    img.paste(button_img, (button_x, input_y), button_img)
    
    return img

def create_tablet_mockup():
    """Create tablet mockup (768x1024)"""
    width, height = 768, 1024
    img = Image.new('RGB', (width, height), hex_to_rgb(COLORS['background_gray']))
    draw = ImageDraw.Draw(img)
    
    margin = 30
    content_width = width - 2 * margin
    
    # Header
    header_y = 30
    header_height = 110
    header_img = Image.new('RGBA', (content_width, header_height), (0, 0, 0, 0))
    header_draw = ImageDraw.Draw(header_img)
    
    for i in range(content_width):
        ratio = i / content_width
        r = int(hex_to_rgb(COLORS['primary_purple'])[0] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[0] * ratio)
        g = int(hex_to_rgb(COLORS['primary_purple'])[1] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[1] * ratio)
        b = int(hex_to_rgb(COLORS['primary_purple'])[2] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[2] * ratio)
        header_draw.line([(i, 0), (i, header_height)], fill=(r, g, b, 255))
    
    mask = Image.new('L', (content_width, header_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, content_width, header_height], radius=15, fill=255)
    header_img.putalpha(mask)
    img.paste(header_img, (margin, header_y), header_img)
    
    # Warning box
    warning_y = header_y + header_height + 25
    warning_height = 75
    draw_rounded_rectangle(
        draw,
        (margin, warning_y, margin + content_width, warning_y + warning_height),
        radius=8,
        fill=hex_to_rgb(COLORS['warning_yellow'])
    )
    draw.rectangle(
        [margin, warning_y + 8, margin + 4, warning_y + warning_height - 8],
        fill=hex_to_rgb(COLORS['warning_border'])
    )
    
    # Chat messages
    msg_y = warning_y + warning_height + 35
    
    # AI Message
    ai_msg_height = 95
    draw_rounded_rectangle(
        draw,
        (margin, msg_y, margin + content_width, msg_y + ai_msg_height),
        radius=10,
        fill=hex_to_rgb(COLORS['light_purple'])
    )
    draw.rectangle(
        [margin, msg_y + 10, margin + 4, msg_y + ai_msg_height - 10],
        fill=hex_to_rgb(COLORS['ai_msg_border'])
    )
    
    # User Message
    user_msg_y = msg_y + ai_msg_height + 18
    user_msg_height = 75
    draw_rounded_rectangle(
        draw,
        (margin, user_msg_y, margin + content_width, user_msg_y + user_msg_height),
        radius=10,
        fill=hex_to_rgb(COLORS['light_blue'])
    )
    draw.rectangle(
        [margin, user_msg_y + 10, margin + 4, user_msg_y + user_msg_height - 10],
        fill=hex_to_rgb(COLORS['user_msg_border'])
    )
    
    # Another AI Message
    ai_msg_y2 = user_msg_y + user_msg_height + 18
    ai_msg_height2 = 110
    draw_rounded_rectangle(
        draw,
        (margin, ai_msg_y2, margin + content_width, ai_msg_y2 + ai_msg_height2),
        radius=10,
        fill=hex_to_rgb(COLORS['light_purple'])
    )
    draw.rectangle(
        [margin, ai_msg_y2 + 10, margin + 4, ai_msg_y2 + ai_msg_height2 - 10],
        fill=hex_to_rgb(COLORS['ai_msg_border'])
    )
    
    # Chat input
    input_y = height - 90
    input_height = 48
    draw_rounded_rectangle(
        draw,
        (margin, input_y, margin + content_width - 80, input_y + input_height),
        radius=8,
        fill=hex_to_rgb(COLORS['white']),
        outline=hex_to_rgb('#e0e0e0'),
        width=2
    )
    
    # Send button
    button_x = margin + content_width - 70
    button_img = Image.new('RGBA', (70, input_height), (0, 0, 0, 0))
    button_draw = ImageDraw.Draw(button_img)
    
    for i in range(70):
        ratio = i / 70
        r = int(hex_to_rgb(COLORS['primary_purple'])[0] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[0] * ratio)
        g = int(hex_to_rgb(COLORS['primary_purple'])[1] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[1] * ratio)
        b = int(hex_to_rgb(COLORS['primary_purple'])[2] * (1 - ratio) + hex_to_rgb(COLORS['secondary_purple'])[2] * ratio)
        button_draw.line([(i, 0), (i, input_height)], fill=(r, g, b, 255))
    
    mask = Image.new('L', (70, input_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, 70, input_height], radius=8, fill=255)
    button_img.putalpha(mask)
    img.paste(button_img, (button_x, input_y), button_img)
    
    return img

if __name__ == "__main__":
    output_dir = "figma_mockups"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🎨 Generating Figma mockups...")
    
    # Desktop
    print("  📱 Creating desktop mockup (1440x1024)...")
    desktop = create_desktop_mockup()
    desktop.save(f"{output_dir}/desktop_1440x1024.png")
    
    # Tablet
    print("  📱 Creating tablet mockup (768x1024)...")
    tablet = create_tablet_mockup()
    tablet.save(f"{output_dir}/tablet_768x1024.png")
    
    # Mobile
    print("  📱 Creating mobile mockup (375x812)...")
    mobile = create_mobile_mockup()
    mobile.save(f"{output_dir}/mobile_375x812.png")
    
    print(f"\n✅ Done! Mockups saved to '{output_dir}/' directory")
    print("\nGenerated files:")
    print(f"  - desktop_1440x1024.png")
    print(f"  - tablet_768x1024.png")
    print(f"  - mobile_375x812.png")
