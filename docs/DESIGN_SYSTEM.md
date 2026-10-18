# Design system

## Direction

Luxury minimalism combines warm ivory, tactile beige, charcoal, and small metallic-gold accents. Editorial serif headings contrast with a clear sans-serif for reading. Broad margins and fine rules give the content room.

## Tokens and layout

The root variables at the top of css/styles.css define paper, deeper paper, ink, muted text, gold, typography, and page width. Gold stays an accent rather than long-form text. The font stack falls back to Georgia and Arial if Google Fonts is unavailable. Content width is capped; gutters and grids adapt at tablet and phone breakpoints.

## Interaction and access

Buttons and text links have short hover feedback. The CSS hero uses a restrained mouse response. FAQ disclosures use native browser controls. Focus remains visible, and a skip link provides a direct route to main content.

Motion is brief and optional. The hero response is disabled for touch-oriented devices and when reduced motion is requested. Keep information available without color, hover, animation, or JavaScript. Check text contrast when changing colors, and give meaningful images useful alternative text.
