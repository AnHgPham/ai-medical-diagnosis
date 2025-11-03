# Hướng Dẫn Sử Dụng Figma Design

## Tổng Quan

Tài liệu này hướng dẫn cách import và sử dụng design mockups trong Figma để phát triển giao diện AI Medical Diagnosis System.

## Files Mockup

Trong thư mục `figma_mockups/` có 3 files mockup:

1. **desktop_1440x1024.png** - Desktop layout
2. **tablet_768x1024.png** - Tablet layout  
3. **mobile_375x812.png** - Mobile layout

## Cách Import vào Figma

### Bước 1: Tạo Project Mới

1. Truy cập [Figma](https://www.figma.com)
2. Đăng nhập hoặc tạo tài khoản miễn phí
3. Click **New design file**
4. Đặt tên: "AI Medical Diagnosis - UI Design"

### Bước 2: Import Mockups

#### Option 1: Drag & Drop (Khuyến nghị)

1. Mở file Figma vừa tạo
2. Kéo thả 3 files PNG vào canvas
3. Figma sẽ tự động tạo frames cho mỗi mockup

#### Option 2: Import qua Menu

1. Click **File** → **Place image**
2. Chọn file mockup muốn import
3. Click vào canvas để đặt image
4. Lặp lại cho các mockup khác

### Bước 3: Tổ Chức Frames

1. **Tạo Pages:**
   - Click **+** bên cạnh "Page 1"
   - Tạo pages: "Desktop", "Tablet", "Mobile"
   - Di chuyển mockups vào pages tương ứng

2. **Tạo Frames:**
   - Select mockup image
   - Right-click → **Frame selection**
   - Hoặc press `Ctrl/Cmd + Alt + G`
   - Đặt tên frame theo kích thước

3. **Set Frame Sizes:**
   - Desktop: 1440 x 1024
   - Tablet: 768 x 1024
   - Mobile: 375 x 812

## Cách Tạo Components từ Mockups

### 1. Tạo Design System Page

1. Tạo page mới: "Design System"
2. Sẽ chứa tất cả components có thể tái sử dụng

### 2. Extract Colors

**Sử dụng Color Picker:**

1. Select mockup
2. Click vào màu cần lấy
3. Copy hex code
4. Tạo color styles:
   - Click **Local styles** (4 dots icon)
   - Click **+** → **Color**
   - Paste hex code
   - Đặt tên (vd: "Primary Purple")

**Colors cần tạo:**
- Primary Purple: `#667eea`
- Secondary Purple: `#764ba2`
- Light Blue: `#e3f2fd`
- Light Purple: `#f3e5f5`
- Warning Yellow: `#fff3cd`
- Warning Border: `#ff9800`
- Background Gray: `#f5f7fa`
- Text Dark: `#333333`
- Text Gray: `#666666`

### 3. Create Components

#### Header Component

1. Vẽ rectangle với kích thước tương tự mockup
2. Apply gradient:
   - Fill → Linear gradient
   - Start: Primary Purple
   - End: Secondary Purple
   - Angle: 135°
3. Set corner radius: 15px
4. Add shadow: 0px 4px 15px rgba(102, 126, 234, 0.3)
5. Add text: "🏥 AI Medical Diagnosis"
6. Right-click → **Create component**
7. Đặt tên: "Header"

#### Chat Message Components

**User Message:**

1. Vẽ rectangle
2. Fill: Light Blue (#e3f2fd)
3. Corner radius: 10px
4. Add left border: 4px, #2196f3
5. Add text layers:
   - "👤 Bạn" (bold)
   - "10:30" (small, gray)
   - Message content
6. Create component: "User Message"

**AI Message:**

1. Vẽ rectangle
2. Fill: Light Purple (#f3e5f5)
3. Corner radius: 10px
4. Add left border: 4px, #9c27b0
5. Add text layers:
   - "🏥 AI Doctor" (bold)
   - "10:30" (small, gray)
   - Message content
6. Create component: "AI Message"

#### Warning Box

1. Vẽ rectangle
2. Fill: Warning Yellow (#fff3cd)
3. Corner radius: 8px
4. Add left border: 4px, Warning Border (#ff9800)
5. Add text: "⚠️ LƯU Ý QUAN TRỌNG"
6. Create component: "Warning Box"

#### Button

1. Vẽ rectangle
2. Fill: Gradient (Primary → Secondary Purple)
3. Corner radius: 8px
4. Add text: "Send" (white, bold)
5. Add hover state:
   - Shadow: 0px 4px 12px rgba(102, 126, 234, 0.4)
   - Transform: translateY(-2px)
6. Create component: "Button Primary"

#### Chat Input

1. Vẽ rectangle
2. Fill: White
3. Border: 2px, #e0e0e0
4. Corner radius: 8px
5. Add placeholder text
6. Add focus state:
   - Border color: Primary Purple
   - Shadow: 0px 0px 0px 3px rgba(102, 126, 234, 0.1)
7. Create component: "Chat Input"

### 4. Create Auto Layout

**Cho Chat Messages:**

1. Select message component
2. Press `Shift + A` (Auto Layout)
3. Set:
   - Direction: Vertical
   - Spacing: 12px
   - Padding: 16px

**Cho Button:**

1. Select button
2. Auto Layout
3. Set:
   - Direction: Horizontal
   - Padding: 12px 24px
   - Horizontal align: Center

## Typography Setup

### 1. Import Font

1. Click **Text** tool (T)
2. Click font dropdown
3. Search "Inter"
4. Click **Get font** nếu chưa có

### 2. Create Text Styles

**H1 - Header:**
- Font: Inter Bold
- Size: 35px (2.2rem)
- Line height: 120%
- Color: White

**H2 - Section:**
- Font: Inter Semi-bold
- Size: 24px (1.5rem)
- Line height: 130%
- Color: Text Dark

**Body:**
- Font: Inter Regular
- Size: 16px (1rem)
- Line height: 150%
- Color: Text Dark

**Small:**
- Font: Inter Regular
- Size: 14px (0.85rem)
- Line height: 140%
- Color: Text Gray

**Button:**
- Font: Inter Semi-bold
- Size: 16px
- Line height: 100%
- Color: White

## Responsive Design

### Desktop (1440px)

- Sidebar: 300px fixed width
- Content: Flexible width
- Max content width: 1140px

### Tablet (768px)

- Sidebar: Collapsible/Hidden
- Content: Full width with margins
- Margins: 30px

### Mobile (375px)

- Sidebar: Hidden (hamburger menu)
- Content: Full width
- Margins: 20px

## Prototyping

### 1. Create Interactions

**Chat Input → Send:**

1. Select chat input
2. Click **Prototype** tab
3. Add interaction:
   - Trigger: On click
   - Action: Navigate to
   - Destination: New message frame
   - Animation: Smart animate

**Button Hover:**

1. Create hover variant
2. Add interaction:
   - Trigger: On hover
   - Action: Change to
   - Destination: Hover variant
   - Animation: Ease out, 300ms

### 2. Create Flow

1. Tạo frame "Start"
2. Tạo frame "Chat Active"
3. Tạo frame "Message Sent"
4. Link các frames với interactions

## Export Settings

### For Development

**Components:**

1. Select component
2. Click **Export** (bottom right)
3. Settings:
   - Format: PNG
   - Scale: 2x (for retina)
   - Suffix: @2x

**Icons:**

1. Format: SVG
2. Scale: 1x
3. Outline stroke

**Full Mockups:**

1. Format: PNG
2. Scale: 2x
3. Quality: High

### For Presentation

1. Format: PDF
2. Include all pages
3. Quality: High

## Collaboration

### Share Design

1. Click **Share** (top right)
2. Set permissions:
   - **View**: Cho stakeholders
   - **Edit**: Cho designers
   - **Developer**: Cho developers
3. Copy link

### Developer Handoff

1. Select frame/component
2. Click **Code** tab (right panel)
3. Copy CSS/iOS/Android code
4. Share with developers

### Comments

1. Press `C` để comment
2. Click vào element
3. Type comment
4. Tag người cần review: `@username`

## Tips & Best Practices

### 1. Naming Convention

**Components:**
- Format: `Category/Name/Variant`
- Example: `Button/Primary/Default`
- Example: `Message/User/Active`

**Layers:**
- Descriptive names
- No "Rectangle 1", "Text 2"
- Use: "Header Title", "Message Content"

### 2. Organization

**Use Pages:**
- Cover
- Design System
- Desktop
- Tablet
- Mobile
- Prototypes

**Use Frames:**
- Group related elements
- Name clearly
- Use consistent sizes

### 3. Components

**Create variants:**
- Different states (default, hover, active)
- Different sizes (small, medium, large)
- Different types (primary, secondary)

**Use instances:**
- Don't duplicate components
- Use instances from main component
- Override text/colors as needed

### 4. Constraints

**Set constraints for responsive:**
- Left & Right: For full-width elements
- Center: For centered content
- Scale: For proportional sizing

### 5. Styles

**Create styles for:**
- Colors (all brand colors)
- Text (all typography)
- Effects (shadows, blurs)
- Grids (layout grids)

## Resources

### Figma Learning

- [Figma Official Tutorials](https://www.figma.com/resources/learn-design/)
- [Figma YouTube Channel](https://www.youtube.com/c/Figma)
- [Figma Community](https://www.figma.com/community)

### Design System Examples

- [Material Design](https://material.io/design)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/)
- [Ant Design](https://ant.design/)

### Plugins Useful

- **Unsplash** - Free images
- **Iconify** - Icon library
- **Content Reel** - Dummy content
- **Stark** - Accessibility checker
- **Autoflow** - User flow diagrams

## Troubleshooting

### Mockup không đúng kích thước

1. Select image
2. Right panel → Width/Height
3. Nhập kích thước chính xác
4. Lock aspect ratio nếu cần

### Colors không khớp

1. Sử dụng Color Picker (I)
2. Click vào mockup
3. Copy exact hex code
4. Paste vào color style

### Font không giống

1. Đảm bảo dùng Inter font
2. Check font weight (400, 600, 700)
3. Check font size (px to rem conversion)

### Export bị mờ

1. Đảm bảo export ở 2x scale
2. Check "Include in export" cho tất cả layers
3. Sử dụng PNG cho raster, SVG cho vector

## Next Steps

1. ✅ Import mockups vào Figma
2. ✅ Tạo color palette
3. ✅ Setup typography
4. ✅ Create components
5. ✅ Build design system
6. ✅ Create responsive variants
7. ✅ Add interactions
8. ✅ Share with team
9. ✅ Handoff to developers

## Support

Nếu cần hỗ trợ:
- [Figma Help Center](https://help.figma.com/)
- [Figma Community Forum](https://forum.figma.com/)
- [Figma Twitter](https://twitter.com/figma)
