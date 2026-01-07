# ARC Protocol - Design System

## Color Palette

```
Primary Navy:    #383F5B
White:           #FFFFFF
Light Blue:      #A7BCC4
Teal:            #115361
```

## Design Philosophy

**Apple-inspired**: Sophisticated, minimal, attention to detail
- Clean typography with Inter font family
- Smooth animations (cubic-bezier easing)
- Generous white space
- Subtle shadows and depth
- Refined hover states

## Key Design Elements

### Typography
- **Font**: Inter (weights 300-700)
- **Letter spacing**: -0.022em for headings, -0.011em for body
- **Line height**: 1.2 for headings, 1.7-1.8 for body
- **Antialiasing**: Enabled for crisp text rendering

### Features Section
**Enhanced from basic cards to sophisticated showcases:**

- Large padding (4rem vertical, 3rem horizontal)
- Gradient backgrounds (145deg, white to off-white)
- Top accent line (4px gradient, animates on hover)
- Elevated hover state (8px lift + scale 1.02)
- Refined shadows (4px normal, 20px on hover)
- Icon scaling animation
- Better visual hierarchy

### Animations
- **Transitions**: 150ms (fast), 300ms (normal), 400ms (slow)
- **Easing**: cubic-bezier(0.4, 0, 0.2, 1) - Apple's signature
- **Transform**: translateY + scale for depth
- **Hover effects**: Smooth, purposeful

### Cards & Components
- **Border radius**: 12px (global), 24px (features)
- **Shadows**: Multi-layer, rgba opacity
- **Borders**: 1px solid with low opacity
- **Backdrop blur**: 20px on navbar

### Buttons
- Smooth corners (8px radius)
- Gradient backgrounds for primary
- Subtle lift on hover (1px up)
- Larger shadows on interaction
- Font weight 500-600

### Code Blocks
- Navy background (#383F5B)
- Light blue text (#A7BCC4)
- Rounded corners (16px)
- Deep shadows for depth
- SF Mono font family

## Spacing System

- **Section padding**: 6rem - 8rem vertical
- **Component padding**: 2rem - 4rem
- **Gaps**: 1rem - 4rem based on context
- **Hero padding**: 8rem top, 6rem bottom

## Responsive Breakpoints

- **Desktop**: > 996px (3 columns)
- **Tablet**: 600px - 996px (1 column)
- **Mobile**: < 600px (stacked, full width)

## Dark Mode

Automatically adapts with sophisticated dark theme:
- Background: #1a1d2e → #232738
- Text: #E8EDF2, #A7BCC4
- Gradients inverted
- Increased contrast
- Deeper shadows

## Accessibility

- High contrast ratios
- Keyboard navigation support
- Semantic HTML
- ARIA labels where needed
- Focus states

## Performance

- Font loading optimized
- Smooth scrollbar styling
- Hardware-accelerated transforms
- Efficient animations (GPU)

## Browser Support

- Modern browsers (last 2 versions)
- Safari (webkit prefixes included)
- Chrome/Edge (chromium)
- Firefox

---

**Result**: Professional, sophisticated documentation site matching enterprise design standards with Apple-level polish.

