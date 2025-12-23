# CSS Contract: Navbar and Logo Styling

## Overview
This document specifies the CSS styling contract for the navigation bar and logo elements to ensure consistent appearance and behavior across the Physical AI Book website.

## Logo Styling Requirements

### Logo Container
- **Selector**: `.navbar__logo`
- **Properties**:
  - `display`: Must be `flex` or `inline-flex` for proper alignment
  - `align-items`: Must be `center` for vertical alignment
  - `margin-right`: Must be `1rem` for proper spacing from other elements
  - `transition`: Should include smooth transition for hover effects

### Logo Image
- **Selector**: `.navbar__logo img`
- **Properties**:
  - `width`: Maximum 40px for desktop, 32px for mobile
  - `height`: Auto-scaling to maintain aspect ratio
  - `max-height`: 40px to prevent oversized logos
  - `border-radius`: 4px for rounded corners (optional)
  - `transition`: 0.2s for smooth hover effects

### Error State Handling
- **Selector**: `.navbar__logo img[aria-busy="true"]` (loading state)
- **Properties**:
  - `opacity`: 0.6 during loading
  - `pointer-events`: `none` to prevent interaction during loading

- **Selector**: `.navbar__logo img.error` (failed to load)
- **Properties**:
  - `display`: `none` to hide broken image icon
  - `background`: Placeholder background with text alternative

## Navbar Styling Requirements

### Navigation Bar Container
- **Selector**: `.navbar`
- **Properties**:
  - `background-color`: Modern gradient or solid color (as defined in CSS variables)
  - `box-shadow`: Subtle shadow for depth (e.g., `0 2px 4px rgba(0,0,0,0.1)`)
  - `padding`: `0.75rem 1rem` for comfortable spacing
  - `position`: `sticky` or `fixed` for persistent navigation
  - `top`: `0` to position at top of viewport
  - `z-index`: High enough to appear above content

### Navigation Items
- **Selector**: `.navbar__item`
- **Properties**:
  - `color`: High contrast with background for readability
  - `font-weight`: Medium (500) for active items, Normal (400) for others
  - `padding`: `0.5rem 1rem` for comfortable click/tap targets
  - `margin`: `0 0.25rem` for spacing between items
  - `border-radius`: 6px for subtle rounded corners
  - `transition`: Smooth transition for hover effects (0.2s ease)

### Hover and Active States
- **Selector**: `.navbar__item:hover`
- **Properties**:
  - `background-color`: Slightly darker/lighter shade for visual feedback
  - `transform`: Subtle scale or position adjustment (optional)

- **Selector**: `.navbar__item.active`
- **Properties**:
  - `font-weight`: Bold or semibold for emphasis
  - `color`: Different color to indicate active state
  - `background-color`: Subtle highlight for active page

### Responsive Behavior
- **Media Query**: `@media (max-width: 996px)` for mobile
  - Navigation items should collapse into hamburger menu
  - Logo size should adjust to smaller dimensions
  - Padding and spacing should be reduced for smaller screens

## Animation Requirements

### Hover Effects
- **Transition Property**: `all`
- **Transition Duration**: 0.2s
- **Transition Timing**: `ease-in-out`
- **Transform Effects**: Subtle scale (1.02x) or position adjustments

### Loading States
- **Animation**: Fade-in or skeleton loading effect
- **Duration**: 0.3s for smooth appearance
- **Timing Function**: Ease for natural feel

## Accessibility Compliance

### Contrast Requirements
- **Normal Text**: Minimum 4.5:1 contrast ratio against background
- **Large Text**: Minimum 3:1 contrast ratio against background
- **Logotypes**: No minimum requirement but should be clearly visible

### Screen Reader Compatibility
- **Alt Text**: Logo images must have descriptive alt text
- **ARIA Labels**: Navigation items should have appropriate labels
- **Focus Indicators**: Visible focus rings for keyboard navigation

## Performance Considerations

### Loading Optimization
- **Logo Format**: Prefer SVG for scalability or WebP for raster images
- **File Size**: Keep under 100KB for fast loading
- **Lazy Loading**: Not applicable for logo in navigation bar
- **Critical CSS**: Navbar styles should be inlined in `<head>` for fastest rendering

### Rendering Performance
- **CSS Specificity**: Keep selectors simple to avoid performance issues
- **Avoid Expensive Properties**: Minimize use of `box-shadow`, `filter`, and `transform` on frequently updated elements
- **Hardware Acceleration**: Use `will-change` property for elements that animate frequently