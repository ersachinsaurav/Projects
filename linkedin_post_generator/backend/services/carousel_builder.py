"""
Carousel Builder
================
Creates LinkedIn carousel from AI cover image + post card sections.

Hybrid approach:
- First image: AI-generated cover with character + overlay at bottom 30%
- Rest: Post cards (one per section: title, sections, takeaways)
- All images synced to same size (768x512) for elegant PDF
- Arrow indicators added to show next page with soft edges
"""

import base64
import io
import os
import logging
from typing import Optional, List, Dict
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from .post_card_builder import PostCardBuilder, PostCardStyle
from ..utils.constants import get_social_branding

logger = logging.getLogger(__name__)

# Font paths for carousel cover
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

# Carousel dimensions - 768 height x 512 width for better content layout
# AI generates image with bottom 30% free for title/footer overlay
CAROUSEL_WIDTH = 512
CAROUSEL_HEIGHT = 768

# Content area percentages
AI_IMAGE_CONTENT_PERCENT = 0.70  # Top 70% for AI image content (characters)
OVERLAY_AREA_PERCENT = 0.30      # Bottom 30% for title + footer

# Arrow size and position - centered in FULL image height
ARROW_SIZE = 32
# Arrow positioned at vertical center of the COMPLETE image (768 / 2 = 384px)
ARROW_Y_POSITION = CAROUSEL_HEIGHT // 2  # 384px - exact center of full image

# Overlay styling (consistent with image_processor.py)
OVERLAY_OPACITY = 0.80  # Strong opacity for readability

# Footer dimensions for carousel (scaled for 512 width)
CAROUSEL_FOOTER_HEIGHT = 50  # Fixed footer height for carousel


class CarouselBuilder:
    """Builds carousel from AI cover + post card sections."""

    def __init__(self, branding: Optional[dict] = None):
        """Initialize carousel builder."""
        self.branding = branding or get_social_branding()
        # Extract name from handle or use default
        handle = self.branding.get('handle', '@yourusername')
        name = self.branding.get('name', 'Your Name')
        # Post cards use same dimensions as carousel (768x512)
        # Background color will be set from cover image in build_carousel
        self.post_card_builder = PostCardBuilder(PostCardStyle(
            width=CAROUSEL_WIDTH,
            height=CAROUSEL_HEIGHT,
            theme='dark',
            name=name,
            handle=handle
        ))

    def _extract_dominant_colors(self, image_base64: str, num_colors: int = 5) -> tuple:
        """
        Extract dominant colors from the cover image.
        Returns a tuple (R, G, B) representing the best background color.

        Args:
            image_base64: Base64 encoded image
            num_colors: Number of dominant colors to extract

        Returns:
            Tuple (R, G, B) suitable for background
        """
        try:
            img_data = base64.b64decode(image_base64)
            img_buffer = io.BytesIO(img_data)
            img = Image.open(img_buffer).convert('RGB')

            # Resize for faster processing (keep aspect ratio)
            max_size = 200
            if img.width > max_size or img.height > max_size:
                aspect = img.width / img.height
                if img.width > img.height:
                    new_size = (max_size, int(max_size / aspect))
                else:
                    new_size = (int(max_size * aspect), max_size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Quantize to reduce color space and get dominant colors
            quantized = img.quantize(colors=num_colors)

            # Get color frequencies
            colors = quantized.getcolors(maxcolors=num_colors * 2)
            if not colors:
                return (0, 0, 0)  # Fallback to black

            # Sort by frequency (most common first)
            colors.sort(reverse=True, key=lambda x: x[0])

            # Use the most common color (first in sorted list)
            if colors:
                palette = quantized.getpalette()
                if palette:
                    color_index = colors[0][1]  # Most common color
                    r = palette[color_index * 3]
                    g = palette[color_index * 3 + 1]
                    b = palette[color_index * 3 + 2]

                    # Calculate brightness (0-255)
                    brightness = (r * 299 + g * 587 + b * 114) / 1000

                    # Always lighten the color (make it brighter)
                    # Target brightness: 180-220 (light enough for dark text, not too bright)
                    target_brightness = 200

                    if brightness < target_brightness:
                        # Lighten: move towards white
                        # Calculate how much to lighten
                        lighten_factor = (target_brightness - brightness) / brightness if brightness > 0 else 1
                        # Blend with white (255, 255, 255)
                        blend_factor = min(0.6, lighten_factor * 0.5)  # Cap at 60% blend
                        r = int(r + (255 - r) * blend_factor)
                        g = int(g + (255 - g) * blend_factor)
                        b = int(b + (255 - b) * blend_factor)

                    # Ensure we don't go too bright (max 240)
                    final_brightness = (r * 299 + g * 587 + b * 114) / 1000
                    if final_brightness > 240:
                        # Slightly darken if too bright
                        factor = 240 / final_brightness
                        r = int(r * factor)
                        g = int(g * factor)
                        b = int(b * factor)

                    return (r, g, b)

            return (0, 0, 0)  # Final fallback to black
        except Exception as e:
            logger.warning(f"Failed to extract colors from cover image: {e}")
            return (0, 0, 0)  # Fallback to black

    def _load_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Load font with fallbacks."""
        font_paths = [
            # Bold fonts
            os.path.join(ASSETS_FONTS_DIR, "SourceSansPro-Bold.ttf") if bold else os.path.join(ASSETS_FONTS_DIR, "SourceSansPro-Semibold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Raleway-Bold.ttf") if bold else os.path.join(ASSETS_FONTS_DIR, "Raleway-Medium.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "OpenSans-Bold.ttf") if bold else os.path.join(ASSETS_FONTS_DIR, "OpenSans-Semibold.ttf"),
            # System fonts
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

        for path in font_paths:
            try:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue

        return ImageFont.load_default()

    def _render_carousel_cover(self, ai_image_base64: str, title: str, subtitle: Optional[str] = None) -> str:
        """
        Render carousel cover with title/subtitle in the bottom 30% overlay area.
        AI image should have interactive cartoon character in top 70%.

        Design:
        - Top 70%: AI-generated illustration with characters
        - Bottom 30%: Full-width gradient overlay with title, subtitle, and footer
        - Smooth gradient fade at top edge of overlay

        Args:
            ai_image_base64: AI-generated image with cartoon character (512x768, content in top 70%)
            title: Main title
            subtitle: Optional subtitle

        Returns:
            Base64 encoded image with title/subtitle overlay and footer
        """
        # Decode AI image
        img_data = base64.b64decode(ai_image_base64)
        img_buffer = io.BytesIO(img_data)
        img = Image.open(img_buffer).convert('RGBA')

        # Resize/fit AI image to carousel dimensions
        if img.size != (CAROUSEL_WIDTH, CAROUSEL_HEIGHT):
            logger.warning(f"AI generated {img.size} instead of {CAROUSEL_WIDTH}x{CAROUSEL_HEIGHT}. Fitting to canvas...")

            # Calculate scaling to fill the canvas (cover mode)
            img_aspect = img.width / img.height
            canvas_aspect = CAROUSEL_WIDTH / CAROUSEL_HEIGHT

            if img_aspect > canvas_aspect:
                # Image is wider - fit to height, crop width
                new_height = CAROUSEL_HEIGHT
                new_width = int(CAROUSEL_HEIGHT * img_aspect)
            else:
                # Image is taller - fit to width, crop height
                new_width = CAROUSEL_WIDTH
                new_height = int(CAROUSEL_WIDTH / img_aspect)

            # Resize with high-quality resampling
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create canvas and center-crop the resized image
            canvas = Image.new('RGBA', (CAROUSEL_WIDTH, CAROUSEL_HEIGHT), (20, 20, 20, 255))
            paste_x = (CAROUSEL_WIDTH - new_width) // 2
            paste_y = (CAROUSEL_HEIGHT - new_height) // 2
            canvas.paste(img_resized, (paste_x, paste_y))
            img = canvas
        else:
            logger.debug(f"AI correctly generated {CAROUSEL_WIDTH}x{CAROUSEL_HEIGHT} image")

        # Create overlay for gradient and text - FULL WIDTH, no side gaps
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Calculate overlay area (bottom 30%)
        overlay_start_y = int(CAROUSEL_HEIGHT * AI_IMAGE_CONTENT_PERCENT)
        overlay_height = CAROUSEL_HEIGHT - overlay_start_y

        # Create full-width gradient overlay
        max_alpha = int(255 * OVERLAY_OPACITY)

        # Gradient zone above overlay (smooth fade from transparent to overlay)
        gradient_zone = int(CAROUSEL_HEIGHT * 0.08)  # 8% gradient fade zone

        # Draw top gradient fade - FULL WIDTH from edge to edge
        for i in range(gradient_zone):
            y_pos = overlay_start_y - gradient_zone + i
            if y_pos >= 0:
                progress = i / gradient_zone
                alpha = int(max_alpha * (progress ** 2))  # Ease-in curve
                # Full width - 0 to CAROUSEL_WIDTH
                draw.rectangle(
                    [(0, y_pos), (CAROUSEL_WIDTH, y_pos + 1)],
                    fill=(0, 0, 0, alpha),
                )

        # Draw main overlay area - FULL WIDTH, solid
        for i in range(overlay_height):
            y_pos = overlay_start_y + i
            progress = i / overlay_height
            alpha = int(max_alpha * (0.90 + 0.10 * progress))  # 90% to 100%
            # Full width overlay
            draw.rectangle(
                [(0, y_pos), (CAROUSEL_WIDTH, y_pos + 1)],
                fill=(0, 0, 0, alpha),
            )

        # Load fonts - larger for better readability
        title_font = self._load_font(30, bold=True)  # Title font
        subtitle_font = self._load_font(18, bold=False)  # Subtitle font

        # Calculate layout areas
        padding = 25  # Horizontal padding
        content_width = CAROUSEL_WIDTH - (padding * 2)

        # Reserve space for compact footer at bottom
        footer_height = CAROUSEL_FOOTER_HEIGHT
        text_area_start_y = overlay_start_y + 20
        text_area_end_y = CAROUSEL_HEIGHT - footer_height - 10

        # Wrap title
        title_lines = self._wrap_text(title, title_font, content_width, draw)

        # Calculate title height
        title_bbox = draw.textbbox((0, 0), "Ayg", font=title_font)
        title_line_height = int((title_bbox[3] - title_bbox[1]) * 1.25)
        title_height = len(title_lines) * title_line_height

        # Wrap subtitle if exists
        subtitle_lines = []
        subtitle_height = 0
        subtitle_line_height = 0
        if subtitle:
            subtitle_lines = self._wrap_text(subtitle, subtitle_font, content_width, draw)
            subtitle_bbox = draw.textbbox((0, 0), "Ayg", font=subtitle_font)
            subtitle_line_height = int((subtitle_bbox[3] - subtitle_bbox[1]) * 1.2)
            subtitle_height = len(subtitle_lines) * subtitle_line_height

        # Calculate total text height
        gap = 8 if subtitle else 0
        total_text_height = title_height + gap + subtitle_height

        # Center text vertically in the text area
        available_space = text_area_end_y - text_area_start_y
        start_y = text_area_start_y + max(0, (available_space - total_text_height) // 2)

        # Draw title (white with shadow)
        y = start_y
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (CAROUSEL_WIDTH - text_width) // 2
            # Shadow
            draw.text((x + 1, y + 1), line, font=title_font, fill=(0, 0, 0, 120))
            # Main text
            draw.text((x, y), line, font=title_font, fill=(255, 255, 255, 255))
            y += title_line_height

        # Draw subtitle
        if subtitle_lines:
            y += gap
            for line in subtitle_lines:
                bbox = draw.textbbox((0, 0), line, font=subtitle_font)
                text_width = bbox[2] - bbox[0]
                x = (CAROUSEL_WIDTH - text_width) // 2
                draw.text((x, y), line, font=subtitle_font, fill=(255, 255, 255, 200))
                y += subtitle_line_height

        # Draw compact footer - centered, smaller text for 512 width
        self._draw_compact_footer(draw, CAROUSEL_HEIGHT - footer_height, footer_height)

        # Composite overlay onto image
        result = Image.alpha_composite(img, overlay)
        result = result.convert('RGB')

        # Convert to base64
        output_buffer = io.BytesIO()
        result.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        return base64.b64encode(output_buffer.read()).decode('utf-8')

    def _draw_compact_footer(self, draw: ImageDraw.Draw, y_start: int, height: int):
        """Draw a compact footer with icons for carousel images (optimized for 512 width)."""
        # Get branding info
        handle_text = self.branding.get('handle', '@yourusername')
        website_text = self.branding.get('website', 'yourwebsite.com')

        # Font sizes - 16px to match icon size visually
        font_size = 16
        footer_font = self._load_font(font_size, bold=True)

        # Icon and spacing configuration - icons sized to match 16px text
        icon_size = int(height * 0.38)  # Icons balanced with 16px text
        gap = 5  # Gap between elements
        icon_color = (255, 255, 255, 230)  # Bright icons
        text_color = (255, 255, 255, 220)  # Bright text to match

        # Calculate text widths
        handle_bbox = draw.textbbox((0, 0), handle_text, font=footer_font)
        handle_width = handle_bbox[2] - handle_bbox[0]

        sep = " • "
        sep_bbox = draw.textbbox((0, 0), sep, font=footer_font)
        sep_width = sep_bbox[2] - sep_bbox[0]

        website_bbox = draw.textbbox((0, 0), website_text, font=footer_font)
        website_width = website_bbox[2] - website_bbox[0]

        # Total width: [LinkedIn][Instagram] @handle • [Globe] website
        total_width = (
            icon_size + gap +           # LinkedIn + gap
            icon_size + gap * 2 +       # Instagram + larger gap
            handle_width +              # @handle
            sep_width +                 # " • "
            icon_size + gap +           # Globe + gap
            website_width               # website
        )

        # Center the footer content
        start_x = (CAROUSEL_WIDTH - total_width) // 2
        current_x = start_x
        icon_y = y_start + (height - icon_size) // 2
        text_y = y_start + height // 2

        # Draw LinkedIn icon
        self._draw_linkedin_icon(draw, current_x, icon_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw Instagram icon
        self._draw_instagram_icon(draw, current_x, icon_y, icon_size, icon_color)
        current_x += icon_size + gap * 2

        # Draw handle text
        draw.text((current_x, text_y), handle_text, font=footer_font, fill=text_color, anchor="lm")
        current_x += handle_width

        # Draw separator
        draw.text((current_x, text_y), sep, font=footer_font, fill=(255, 255, 255, 120), anchor="lm")
        current_x += sep_width

        # Draw globe icon
        self._draw_globe_icon(draw, current_x, icon_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw website text
        draw.text((current_x, text_y), website_text, font=footer_font, fill=text_color, anchor="lm")

    def _draw_linkedin_icon(self, draw: ImageDraw.Draw, x: int, y: int, size: int, color: tuple):
        """Draw LinkedIn icon - outline style rounded rectangle with 'in' text."""
        line_width = max(1, size // 12)

        # Draw rounded rectangle outline
        draw.rounded_rectangle(
            [(x, y), (x + size, y + size)],
            radius=size // 4,
            outline=color,
            width=line_width,
        )

        # Draw 'in' text inside - LARGER for better visibility
        font_size = int(size * 0.70)  # Increased from 0.50 to 0.70
        font = self._load_font(font_size, bold=True)
        draw.text(
            (x + size // 2, y + size // 2),
            "in",
            font=font,
            fill=color,
            anchor="mm",
        )

    def _draw_instagram_icon(self, draw: ImageDraw.Draw, x: int, y: int, size: int, color: tuple):
        """Draw Instagram icon - camera outline style."""
        line_width = max(1, size // 12)

        # Outer rounded rectangle
        draw.rounded_rectangle(
            [(x, y), (x + size, y + size)],
            radius=size // 4,
            outline=color,
            width=line_width,
        )

        # Inner circle (lens)
        center = (x + size // 2, y + size // 2)
        lens_radius = size // 4
        draw.ellipse(
            [
                (center[0] - lens_radius, center[1] - lens_radius),
                (center[0] + lens_radius, center[1] + lens_radius),
            ],
            outline=color,
            width=line_width,
        )

        # Small dot (flash) in top-right
        dot_x = x + size - size // 4
        dot_y = y + size // 4
        dot_r = max(1, size // 10)
        draw.ellipse(
            [(dot_x - dot_r, dot_y - dot_r), (dot_x + dot_r, dot_y + dot_r)],
            fill=color,
        )

    def _draw_globe_icon(self, draw: ImageDraw.Draw, x: int, y: int, size: int, color: tuple):
        """Draw globe icon - outline style with meridians."""
        line_width = max(1, size // 12)
        center = (x + size // 2, y + size // 2)
        radius = size // 2 - 1

        # Outer circle
        draw.ellipse(
            [(center[0] - radius, center[1] - radius),
             (center[0] + radius, center[1] + radius)],
            outline=color,
            width=line_width,
        )

        # Horizontal line (equator)
        draw.line(
            [(x + 2, center[1]), (x + size - 2, center[1])],
            fill=color,
            width=line_width,
        )

        # Vertical ellipse (meridian)
        inner_rx = radius // 2
        draw.ellipse(
            [(center[0] - inner_rx, center[1] - radius),
             (center[0] + inner_rx, center[1] + radius)],
            outline=color,
            width=line_width,
        )

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.Draw) -> List[str]:
        """Wrap text to fit within max_width."""
        lines = []
        words = text.split()
        line = ""
        for word in words:
            test_line = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        return lines

    def _resize_image(self, image_base64: str, target_width: int, target_height: int) -> str:
        """Resize image to target dimensions while maintaining aspect ratio."""
        img_data = base64.b64decode(image_base64)
        img_buffer = io.BytesIO(img_data)
        img = Image.open(img_buffer)

        # Calculate scaling to fit within target dimensions
        aspect = img.width / img.height
        target_aspect = target_width / target_height

        if aspect > target_aspect:
            # Image is wider - fit to width
            new_width = target_width
            new_height = int(target_width / aspect)
        else:
            # Image is taller - fit to height
            new_height = target_height
            new_width = int(target_height * aspect)

        # Resize image
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create canvas with target size and paste centered
        canvas = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        canvas.paste(img_resized, (paste_x, paste_y))

        # Convert back to base64
        output_buffer = io.BytesIO()
        canvas.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        return base64.b64encode(output_buffer.read()).decode('utf-8')

    def _add_arrow_indicator(self, image_base64: str, is_last: bool = False) -> str:
        """Add elegant single > arrow indicator with soft/blurred edges to right-middle of image."""
        img_data = base64.b64decode(image_base64)
        img_buffer = io.BytesIO(img_data)
        img = Image.open(img_buffer).convert('RGBA')

        if not is_last:
            # Create a larger overlay for the chevron (for blur effect)
            # We'll draw on a separate image, blur it slightly, then composite
            chevron_overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
            chevron_draw = ImageDraw.Draw(chevron_overlay)

            # Single chevron outline parameters - slightly larger for better visibility
            chevron_height = 28  # Height of chevron
            chevron_width = 16   # Width (how far right the point goes)
            stroke_width = 3     # Outline thickness

            # Position on right side, vertically centered in the content area (above overlay)
            start_x = img.width - 40  # Distance from right edge
            center_y = ARROW_Y_POSITION

            # Draw shadow layer first (larger blur for soft drop shadow)
            shadow_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
            shadow_draw = ImageDraw.Draw(shadow_layer)
            shadow_color = (0, 0, 0, 180)
            shadow_offset = 2

            # Shadow chevron
            shadow_draw.line([
                (start_x + shadow_offset, center_y - chevron_height // 2 + shadow_offset),
                (start_x + chevron_width + shadow_offset, center_y + shadow_offset),
            ], fill=shadow_color, width=stroke_width + 1)
            shadow_draw.line([
                (start_x + chevron_width + shadow_offset, center_y + shadow_offset),
                (start_x + shadow_offset, center_y + chevron_height // 2 + shadow_offset),
            ], fill=shadow_color, width=stroke_width + 1)

            # Apply Gaussian blur to shadow for soft edges
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=3))

            # Draw main white chevron with anti-aliasing
            white_color = (255, 255, 255, 240)

            # Use polygon for smoother anti-aliased look instead of lines
            # Create chevron points
            top_point = (start_x, center_y - chevron_height // 2)
            middle_point = (start_x + chevron_width, center_y)
            bottom_point = (start_x, center_y + chevron_height // 2)

            # Draw thicker outline for better visibility
            chevron_draw.line([top_point, middle_point], fill=white_color, width=stroke_width)
            chevron_draw.line([middle_point, bottom_point], fill=white_color, width=stroke_width)

            # Add rounded joints by drawing small circles at connection points
            joint_radius = stroke_width // 2 + 1
            chevron_draw.ellipse([
                (middle_point[0] - joint_radius, middle_point[1] - joint_radius),
                (middle_point[0] + joint_radius, middle_point[1] + joint_radius)
            ], fill=white_color)

            # Apply slight blur to chevron for soft edges
            chevron_overlay = chevron_overlay.filter(ImageFilter.GaussianBlur(radius=0.5))

            # Composite layers: base image -> shadow -> chevron
            img = Image.alpha_composite(img, shadow_layer)
            img = Image.alpha_composite(img, chevron_overlay)

        # Convert back to RGB for base64 encoding
        img_rgb = Image.new('RGB', img.size, (0, 0, 0))
        img_rgb.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)

        # Convert back to base64
        output_buffer = io.BytesIO()
        img_rgb.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        return base64.b64encode(output_buffer.read()).decode('utf-8')

    def build_carousel(
        self,
        ai_cover_image_base64: str,
        infographic_text: Dict,
        post_text: str,
        short_post: Optional[str] = None,
    ) -> List[str]:
        """
        Build carousel from AI cover + post card sections.

        Args:
            ai_cover_image_base64: AI-generated cover image (first slide)
            infographic_text: Dict with title, subtitle, sections, takeaway
            post_text: Full post text
            short_post: Short post text for title card

        Returns:
            List of base64 encoded images (cover + post cards)
        """
        carousel_images = []

        # 1. Extract dominant color from cover image for post card backgrounds
        extracted_bg_color = self._extract_dominant_colors(ai_cover_image_base64)
        logger.info(f"Extracted background color from cover: RGB{extracted_bg_color}")

        # Update post card builder style with extracted color
        handle = self.branding.get('handle', '@yourusername')
        name = self.branding.get('name', 'Your Name')
        self.post_card_builder.style = PostCardStyle(
            width=CAROUSEL_WIDTH,
            height=CAROUSEL_HEIGHT,
            theme='dark',
            name=name,
            handle=handle,
            custom_bg_color=extracted_bg_color
        )

        # 2. Create carousel cover with title/subtitle overlay on AI image
        title = infographic_text.get('title', '')
        subtitle = infographic_text.get('subtitle', '')
        cover_with_overlay = self._render_carousel_cover(
            ai_image_base64=ai_cover_image_base64,
            title=title or 'Key Insight',
            subtitle=subtitle
        )
        carousel_images.append(cover_with_overlay)

        # 3. Create section cards (one per section) - with larger section titles
        sections = infographic_text.get('sections', [])
        for idx, section in enumerate(sections):
            section_title = section.get('title', '')
            bullets = section.get('bullets', [])

            if section_title or bullets:
                # Format section text with larger title
                section_text = section_title if section_title else ''
                if bullets:
                    bullet_text = '\n'.join([f"• {bullet}" for bullet in bullets])
                    if section_text:
                        section_text = f"{section_text}\n\n{bullet_text}"
                    else:
                        section_text = bullet_text

                section_card_base64, _ = self.post_card_builder.build(
                    post_text=section_text,
                    avatar_base64=None,
                    short_post=None,
                    is_carousel=True,  # Flag for carousel-specific styling
                    is_section=True,  # Flag to indicate this is a section (larger title)
                )
                carousel_images.append(section_card_base64)

        # 4. Create takeaway/conclusion card (if exists) - with title prefix and follow CTA
        takeaway = infographic_text.get('takeaway', '')
        if takeaway:
            # Add "Takeaway" or "Conclusion" title prefix
            takeaway_title = "Takeaway"
            takeaway_text = f"{takeaway_title}\n\n{takeaway}"

            takeaway_card_base64, _ = self.post_card_builder.build(
                post_text=takeaway_text,
                avatar_base64=None,
                short_post=None,
                is_carousel=True,  # Flag for carousel-specific styling
                is_takeaway=True,  # Flag to indicate this is the final slide
            )

            # Add "Follow for more" CTA to the last slide
            takeaway_with_cta = self._add_follow_cta(takeaway_card_base64)
            carousel_images.append(takeaway_with_cta)

        return carousel_images

    def _add_follow_cta(self, image_base64: str) -> str:
        """
        Add [Follow button] + "for more" CTA to the bottom-right of the image.
        Tilted diagonally between takeaway content and footer.
        """
        # Decode image
        img_data = base64.b64decode(image_base64)
        img_buffer = io.BytesIO(img_data)
        img = Image.open(img_buffer).convert('RGBA')

        # Create a separate layer for the CTA that we'll rotate
        cta_layer = Image.new('RGBA', (300, 80), (0, 0, 0, 0))  # Larger canvas for rotation
        cta_draw = ImageDraw.Draw(cta_layer)

        # Font size - increased for larger button
        button_font = self._load_awesome_font(24)  # Increased from 18 to 24
        text_font = self._load_awesome_font(22)    # "for more" text at 22px

        # Text elements
        button_text = "+ Follow"
        cta_text = "for more"

        # Calculate dimensions
        button_bbox = cta_draw.textbbox((0, 0), button_text, font=button_font)
        button_text_width = button_bbox[2] - button_bbox[0]
        button_text_height = button_bbox[3] - button_bbox[1]

        cta_bbox = cta_draw.textbbox((0, 0), cta_text, font=text_font)
        cta_text_width = cta_bbox[2] - cta_bbox[0]
        cta_text_height = cta_bbox[3] - cta_bbox[1]

        # Button dimensions with padding - increased for larger button
        button_padding_x = 20  # Increased from 14 to 20
        button_padding_y = 12  # Increased from 8 to 12
        button_total_width = button_text_width + button_padding_x * 2
        button_total_height = button_text_height + button_padding_y * 2

        # Layout: [Follow button] "for more"
        gap = 10  # Gap between button and text
        total_width = button_total_width + gap + cta_text_width

        # Center in the CTA layer
        start_x = (300 - total_width) // 2
        button_y = (80 - button_total_height) // 2

        # Draw follow button - rounded pill with LinkedIn blue
        linkedin_blue = (0, 119, 181)  # LinkedIn brand blue
        button_radius = button_total_height // 2

        cta_draw.rounded_rectangle(
            [(start_x, button_y),
             (start_x + button_total_width, button_y + button_total_height)],
            radius=button_radius,
            fill=linkedin_blue,
        )

        # Draw button text (white on blue) - centered in button
        button_text_x = start_x + button_padding_x
        button_text_y = button_y + (button_total_height - button_text_height) // 2
        cta_draw.text((button_text_x, button_text_y), button_text, font=button_font, fill=(255, 255, 255))

        # Draw "for more" text after button - use Follow button background color
        text_x = start_x + button_total_width + gap
        text_y = button_y + (button_total_height - cta_text_height) // 2
        cta_color = linkedin_blue  # Use same color as Follow button background
        cta_draw.text((text_x, text_y), cta_text, font=text_font, fill=cta_color)

        # Rotate the CTA layer diagonally (-15 degrees for upward tilt)
        rotated_cta = cta_layer.rotate(15, expand=True, resample=Image.BICUBIC)

        # Position: bottom-right, above footer
        footer_height = CAROUSEL_FOOTER_HEIGHT
        paste_x = CAROUSEL_WIDTH - rotated_cta.width - 10  # 10px from right edge
        paste_y = CAROUSEL_HEIGHT - footer_height - rotated_cta.height - 5  # Above footer

        # Composite the rotated CTA onto the image
        img.paste(rotated_cta, (paste_x, paste_y), rotated_cta)

        # Convert to RGB
        result = img.convert('RGB')

        # Convert to base64
        output_buffer = io.BytesIO()
        result.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        return base64.b64encode(output_buffer.read()).decode('utf-8')

    def _load_awesome_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Load the Awesome font specifically."""
        awesome_path = os.path.join(ASSETS_FONTS_DIR, "Awesome.ttf")
        try:
            if os.path.exists(awesome_path):
                return ImageFont.truetype(awesome_path, size)
        except (OSError, IOError):
            pass

        # Fallback to regular font loading
        return self._load_font(size, bold=True)

