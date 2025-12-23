# Navbar Styling Contract

## Overview
This document specifies the CSS styling contract for the Physical AI Book website navigation bar.

## Logo Requirements

### Logo Display
- **Property**: `navbar.logo.src`
- **Value**: Path to logo image file (e.g., `/img/logo.svg`)
- **Requirement**: Logo must be visible and properly sized in the navigation bar
- **Fallback**: If logo fails to load, alternative text must be displayed

### Logo Sizing
- **Width**: Maximum 40px for desktop, 32px for mobile
- **Height**: Auto-scaling to maintain aspect ratio
- **Responsive**: Must scale appropriately on different screen sizes

## Navbar Styling Properties

### Background
- **Property**: `background-color`
- **Value**: Modern color palette (to be defined)
- **Requirement**: Consistent with overall site design

### Typography
- **Property**: `font-family`
- **Value**: Site-appropriate font stack
- **Font Size**: 16px for desktop, 14px for mobile
- **Font Weight**: Medium (500) for active items, Normal (400) for others

### Spacing
- **Padding**: 0.75rem vertical, 1rem horizontal
- **Item Spacing**: 1.5rem between navigation items
- **Responsive**: Adjusted for mobile view

### Hover Effects
- **Transition**: Smooth 0.2s transition for all interactive elements
- **Color Change**: Subtle color shift on hover
- **Cursor**: Pointer cursor for clickable items

### Responsive Behavior
- **Breakpoint**: Switch to mobile layout at 996px screen width
- **Mobile Menu**: Hamburger icon for navigation items
- **Accessibility**: Proper ARIA labels and keyboard navigation support

## Implementation Notes
- All styling must be implemented in `src/css/custom.css`
- Use CSS variables for consistent color palette
- Ensure sufficient contrast ratios for accessibility
- Test across different browsers and devices
- Maintain all existing functionality while improving aesthetics