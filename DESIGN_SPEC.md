# Design Specification - AI Medical Diagnosis System

## Tổng Quan

Tài liệu này mô tả chi tiết thiết kế UI/UX của hệ thống AI Medical Diagnosis, đảm bảo đồng bộ giữa Figma design và implementation.

## Color Palette

### Primary Colors

| Color Name | Hex Code | RGB | Usage |
|------------|----------|-----|-------|
| **Primary Purple** | `#667eea` | rgb(102, 126, 234) | Gradient start, primary actions |
| **Secondary Purple** | `#764ba2` | rgb(118, 75, 162) | Gradient end, accents |
| **Light Blue** | `#e3f2fd` | rgb(227, 242, 253) | User message background |
| **Light Purple** | `#f3e5f5` | rgb(243, 229, 245) | AI message background |
| **Warning Yellow** | `#fff3cd` | rgb(255, 243, 205) | Warning background |
| **Warning Border** | `#ff9800` | rgb(255, 152, 0) | Warning left border |
| **Background Gray** | `#f5f7fa` | rgb(245, 247, 250) | Page background |
| **Text Dark** | `#333333` | rgb(51, 51, 51) | Primary text |
| **Text Gray** | `#666666` | rgb(102, 102, 102) | Secondary text |

### Gradients

**Primary Gradient:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Sidebar Gradient:**
```css
background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
```

## Typography

### Font Family
- **Primary**: Inter, sans-serif
- **Fallback**: system-ui, -apple-system, sans-serif

### Font Sizes & Weights

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| **H1 (Header)** | 2.2rem (35.2px) | 700 (Bold) | 1.2 |
| **H2 (Section)** | 1.5rem (24px) | 600 (Semi-bold) | 1.3 |
| **Body** | 1rem (16px) | 400 (Regular) | 1.5 |
| **Small** | 0.85rem (13.6px) | 400 (Regular) | 1.4 |
| **Button** | 1rem (16px) | 600 (Semi-bold) | 1 |

## Layout Structure

### Desktop Layout (> 1024px)

```
┌─────────────────────────────────────────────────────────┐
│                      SIDEBAR (300px)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │                                                   │  │
│  │  🎯 AI Doctor                                     │  │
│  │  ─────────────────                                │  │
│  │                                                   │  │
│  │  💡 Khả năng của AI                               │  │
│  │  • Kiến thức toàn diện                            │  │
│  │  • Phân tích thông minh                           │  │
│  │  • Chẩn đoán chính xác                            │  │
│  │                                                   │  │
│  │  ─────────────────                                │  │
│  │                                                   │  │
│  │  🔧 Công nghệ                                     │  │
│  │  • AI Model: Gemini 2.0                           │  │
│  │  • Framework: Streamlit                           │  │
│  │                                                   │  │
│  │  ─────────────────                                │  │
│  │                                                   │  │
│  │  [🗑️ Xóa lịch sử chat]                           │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    MAIN CONTENT AREA                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │         🏥 AI Medical Diagnosis                   │  │
│  │  Hệ thống Chẩn đoán Y tế Thông minh               │  │
│  │         Powered by Google Gemini AI               │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ⚠️ LƯU Ý QUAN TRỌNG                              │  │
│  │  Hệ thống chỉ mang tính chất tham khảo...         │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  💬 Chat với AI Doctor                            │  │
│  │                                                   │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  🏥 AI Doctor              10:30            │  │  │
│  │  │  Xin chào! Tôi là AI Doctor...              │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │                                                   │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │  👤 Bạn                    10:31            │  │  │
│  │  │  Tôi bị sốt và đau đầu                      │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  💬 Mô tả triệu chứng của bạn...        [Send]   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Mobile Layout (< 768px)

- Sidebar collapses to hamburger menu
- Full-width content area
- Stacked layout

## Components

### 1. Header Component

**Dimensions:**
- Height: Auto (padding: 2rem)
- Border radius: 15px
- Margin bottom: 1.5rem

**Styling:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
padding: 2rem;
border-radius: 15px;
text-align: center;
color: white;
box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
```

**Content:**
- Title: "🏥 AI Medical Diagnosis" (2.2rem, bold)
- Subtitle: "Hệ thống Chẩn đoán Y tế Thông minh | Powered by Google Gemini AI" (1rem)

### 2. Warning Box Component

**Dimensions:**
- Padding: 1rem
- Border radius: 8px
- Border left: 4px solid #ff9800
- Margin: 1rem 0

**Styling:**
```css
background: #fff3cd;
border-left: 4px solid #ff9800;
padding: 1rem;
border-radius: 8px;
margin: 1rem 0;
```

**Content:**
- Icon: ⚠️
- Title: "LƯU Ý QUAN TRỌNG"
- Text: Warning message

### 3. Chat Message Components

#### User Message

**Dimensions:**
- Padding: 1rem
- Border radius: 10px
- Border left: 4px solid #2196f3
- Margin: 0.8rem 0

**Styling:**
```css
background: #e3f2fd;
padding: 1rem;
border-radius: 10px;
margin: 0.8rem 0;
border-left: 4px solid #2196f3;
```

**Structure:**
```
┌────────────────────────────────┐
│ 👤 Bạn          10:30          │
│ ────────────────────────────── │
│ Message content here...        │
└────────────────────────────────┘
```

#### AI Message

**Dimensions:**
- Padding: 1rem
- Border radius: 10px
- Border left: 4px solid #9c27b0
- Margin: 0.8rem 0

**Styling:**
```css
background: #f3e5f5;
padding: 1rem;
border-radius: 10px;
margin: 0.8rem 0;
border-left: 4px solid #9c27b0;
```

**Structure:**
```
┌────────────────────────────────┐
│ 🏥 AI Doctor    10:30          │
│ ────────────────────────────── │
│ AI response content here...    │
└────────────────────────────────┘
```

### 4. Button Component

**Dimensions:**
- Width: 100%
- Padding: 0.6rem 1.5rem
- Border radius: 8px

**Styling:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
color: white;
border: none;
padding: 0.6rem 1.5rem;
border-radius: 8px;
font-weight: 600;
transition: all 0.3s;
```

**Hover State:**
```css
transform: translateY(-2px);
box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
```

### 5. Chat Input Component

**Dimensions:**
- Height: 48px
- Border radius: 8px
- Padding: 0.8rem 1rem

**Styling:**
```css
border: 2px solid #e0e0e0;
border-radius: 8px;
padding: 0.8rem 1rem;
font-size: 1rem;
```

**Focus State:**
```css
border-color: #667eea;
box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
```

### 6. Sidebar Component

**Dimensions:**
- Width: 300px (desktop)
- Padding: 2rem 1.5rem

**Styling:**
```css
background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
color: white;
```

**Sections:**
1. Title: "🎯 AI Doctor"
2. Divider
3. Features list
4. Divider
5. Tech stack
6. Divider
7. Reset button

## Spacing System

### Padding & Margin Scale

| Size | Value | Usage |
|------|-------|-------|
| **xs** | 0.25rem (4px) | Tight spacing |
| **sm** | 0.5rem (8px) | Small spacing |
| **md** | 1rem (16px) | Default spacing |
| **lg** | 1.5rem (24px) | Large spacing |
| **xl** | 2rem (32px) | Extra large spacing |
| **2xl** | 3rem (48px) | Section spacing |

### Component Spacing

- **Between messages**: 0.8rem
- **Section margin**: 1.5rem
- **Content padding**: 1rem
- **Header padding**: 2rem
- **Sidebar padding**: 1.5rem

## Border Radius

| Element | Radius |
|---------|--------|
| **Header** | 15px |
| **Messages** | 10px |
| **Buttons** | 8px |
| **Warning box** | 8px |
| **Input fields** | 8px |

## Shadows

### Box Shadows

**Header Shadow:**
```css
box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
```

**Button Hover Shadow:**
```css
box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
```

**Card Shadow (optional):**
```css
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
```

## Icons

### Emoji Icons Used

- 🏥 - Medical/Hospital
- 👤 - User
- 💬 - Chat/Message
- ⚠️ - Warning
- 🔍 - Analysis/Search
- 💊 - Medicine/Treatment
- 💡 - Idea/Feature
- 🔧 - Technology/Tools
- 🗑️ - Delete/Trash
- 🎯 - Target/Goal

## Responsive Breakpoints

| Breakpoint | Width | Layout |
|------------|-------|--------|
| **Mobile** | < 768px | Stacked, no sidebar |
| **Tablet** | 768px - 1024px | Stacked, collapsible sidebar |
| **Desktop** | > 1024px | Side-by-side, fixed sidebar |

## Animation & Transitions

### Transitions

**Default Transition:**
```css
transition: all 0.3s ease;
```

**Button Hover:**
```css
transform: translateY(-2px);
transition: all 0.3s ease;
```

### Loading States

**Spinner:**
- Color: #667eea
- Size: 24px
- Animation: rotate 1s linear infinite

## Accessibility

### Color Contrast

- Text on white: #333333 (AAA compliant)
- White on purple gradient: White (AAA compliant)
- Warning text: #856404 on #fff3cd (AA compliant)

### Focus States

All interactive elements must have visible focus states:
```css
outline: 2px solid #667eea;
outline-offset: 2px;
```

## Figma Design Structure

### Pages

1. **Cover** - Design overview
2. **Design System** - Colors, typography, components
3. **Desktop** - Desktop layout (1440px)
4. **Tablet** - Tablet layout (768px)
5. **Mobile** - Mobile layout (375px)
6. **Components** - Reusable components library

### Frames

- Desktop: 1440 x 1024
- Tablet: 768 x 1024
- Mobile: 375 x 812

### Component Library

1. Header
2. Warning Box
3. User Message
4. AI Message
5. Button (Primary)
6. Chat Input
7. Sidebar
8. Divider

## Export Settings

### For Development

- **Format**: PNG, SVG
- **Scale**: 1x, 2x, 3x (for retina displays)
- **Naming**: component-name@2x.png

### For Documentation

- **Format**: PNG
- **Scale**: 2x
- **Quality**: High

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-03 | Initial design specification |

## Notes

- Thiết kế này dựa trên implementation hiện tại của Streamlit app
- Đảm bảo đồng bộ 100% giữa Figma và code
- Sử dụng Inter font (có sẵn trên Google Fonts)
- Gradient colors phải chính xác để đảm bảo brand consistency
