"""
Infographic Text Renderer
==========================
Renders clean typography overlays on SDXL-generated infographic illustrations.

This service handles:
- Multi-panel infographic layouts
- Text wrapping and positioning
- Brand-safe margins
- Consistent typography system
"""

import base64
import io
import logging
import os
from typing import Optional, List, Literal
from PIL import Image, ImageDraw, ImageFont

from ..utils.constants import get_social_branding
from .text_extractor import _simple_extract as _text_extractor_simple_extract

logger = logging.getLogger(__name__)

# Canvas dimensions (LinkedIn-friendly vertical infographic)
CANVAS_WIDTH = 768
CANVAS_HEIGHT = 1344

# Safe margins
MARGIN_X = 64
MARGIN_Y = 64
CONTENT_WIDTH = 640

# Design tokens
# NOTE: Alpha values - 255 is fully opaque, 0 is fully transparent
# We use semi-transparent overlays to let background show through
COLORS = {
    "title": (0, 0, 0),  # Pure black for maximum visibility (hero section title)
    "subtitle": (20, 15, 10),  # Dark brown shade for headers
    "body": (0, 0, 0),  # Pure black for body text - maximum visibility
    "bullet": (0, 0, 0),  # Black bullets for consistency
    "accent": (0, 123, 255),  # Blue for section titles (NOT hero, NOT takeaway)
    "footer": (255, 255, 255),  # White footer text with shadow for contrast
    "footer_shadow": (0, 0, 0, 120),  # Footer text shadow
    "card_bg": (255, 255, 255, 200),  # Slightly more opaque for readability
    "section_bg": (255, 255, 255, 185),  # Slightly more opaque for sections
}

# Section gap constant - space between section cards (increased for better separation)
SECTION_GAP = 32

# Layout constants
FOOTER_HEIGHT = 100  # Reserve bottom 100px for footer
MAX_CONTENT_Y = CANVAS_HEIGHT - FOOTER_HEIGHT - 20  # Stop content before footer

# Font paths (with fallbacks)
# Priority: assets/fonts > system fonts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")

def _get_font_paths():
    """Get font paths with assets/fonts priority."""
    return {
        "bold": [
            # Custom fonts (priority)
            os.path.join(ASSETS_FONTS_DIR, "SourceSansPro-Bold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Raleway-Bold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Raleway-Heavy.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "OpenSans-Bold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Lato-Bold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Lato-Black.ttf"),
            # System fonts (fallback)
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",  # Linux
        ],
        "regular": [
            # Custom fonts (priority)
            os.path.join(ASSETS_FONTS_DIR, "SourceSansPro-Semibold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Raleway-Medium.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Raleway-SemiBold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "OpenSans-Semibold.ttf"),
            os.path.join(ASSETS_FONTS_DIR, "Lato-Medium.ttf"),
            # System fonts (fallback)
            "/System/Library/Fonts/Supplemental/Arial.ttf",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",  # Linux
        ],
    }

FONT_PATHS = _get_font_paths()


class InfographicRenderer:
    """Renders text overlays on infographic-style images."""

    def __init__(self, branding: Optional[dict] = None):
        """Initialize renderer with branding."""
        self.branding = branding or get_social_branding()
        self._fonts = {}

    def _load_font(self, style: str, size: int) -> ImageFont.FreeTypeFont:
        """Load font with fallbacks - checks assets/fonts first."""
        cache_key = f"{style}_{size}"
        if cache_key in self._fonts:
            return self._fonts[cache_key]

        font_paths = FONT_PATHS.get(style, FONT_PATHS["regular"])

        for path in font_paths:
            try:
                # Check if path exists
                if os.path.exists(path):
                    font = ImageFont.truetype(path, size)
                    self._fonts[cache_key] = font
                    logger.debug(f"Loaded font: {path}")
                    return font
            except (OSError, IOError) as e:
                logger.debug(f"Failed to load font {path}: {e}")
                continue

        # Fallback to default
        logger.warning(f"Using default font for {style} {size}pt - no custom fonts found")
        font = ImageFont.load_default()
        self._fonts[cache_key] = font
        return font

    def _wrap_text(
        self, draw: ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int
    ) -> List[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        line = ""

        for word in words:
            test_line = f"{line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                line = test_line
            else:
                if line:
                    lines.append(line)
                line = word

        if line:
            lines.append(line)

        return lines

    def _draw_linkedin_icon(self, draw: ImageDraw, x: int, y: int, size: int, color: tuple):
        """Draw LinkedIn icon - outline style rounded rectangle with 'in' text."""
        line_width = max(2, size // 10)

        # Draw rounded rectangle outline (not filled)
        draw.rounded_rectangle(
            [(x, y), (x + size, y + size)],
            radius=size // 4,
            outline=color,
            width=line_width,
        )

        # Draw 'in' text inside - increased font size for better visibility
        font_size = int(size * 0.65)  # Increased from 0.55 to 0.65
        icon_font = self._load_font("bold", font_size)
        draw.text(
            (x + size // 2, y + size // 2),
            "in",
            font=icon_font,
            fill=color,
            anchor="mm",
        )

    def _draw_instagram_icon(self, draw: ImageDraw, x: int, y: int, size: int, color: tuple):
        """Draw Instagram icon - camera outline style."""
        line_width = max(2, size // 10)

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
        dot_r = size // 10
        draw.ellipse(
            [(dot_x - dot_r, dot_y - dot_r), (dot_x + dot_r, dot_y + dot_r)],
            fill=color,
        )

    def _draw_globe_icon(self, draw: ImageDraw, x: int, y: int, size: int, color: tuple):
        """Draw globe icon - outline style with meridians."""
        line_width = max(2, size // 10)
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

    def _draw_footer(self, draw: ImageDraw, footer_font: ImageFont.FreeTypeFont) -> None:
        """Draw branded footer with drawn icons - NO overlay background."""
        handle = self.branding.get("handle", "@yourusername")
        website = self.branding.get("website", "yourwebsite.com")

        # Skip footer if both handle and website are empty
        if not handle.strip() and not website.strip():
            return

        footer_y = CANVAS_HEIGHT - FOOTER_HEIGHT
        footer_text_y = footer_y + 50  # Text baseline position

        # Icon configuration
        icon_size = 22  # Slightly larger icons for better visibility
        icon_color = COLORS["footer"]  # White icons
        gap = 10  # Gap between icon and text, and between elements

        # Calculate text widths and heights for proper vertical alignment
        handle_width = 0
        handle_top = footer_text_y
        handle_bottom = footer_text_y
        handle_center_y = footer_text_y

        if handle.strip():
            handle_bbox = draw.textbbox((0, footer_text_y), handle, font=footer_font)
            handle_width = handle_bbox[2] - handle_bbox[0]
            handle_top = handle_bbox[1]  # Top of text bounding box
            handle_bottom = handle_bbox[3]  # Bottom of text bounding box
            handle_center_y = (handle_top + handle_bottom) // 2  # Center of text

        separator = "  •  "
        sep_width = 0
        if handle.strip() and website.strip():
            sep_bbox = draw.textbbox((0, footer_text_y), separator, font=footer_font)
            sep_width = sep_bbox[2] - sep_bbox[0]

        website_width = 0
        if website.strip():
            website_bbox = draw.textbbox((0, footer_text_y), website, font=footer_font)
            website_width = website_bbox[2] - website_bbox[0]

        # Calculate icon Y position - center icons vertically with text centerline
        icon_y = handle_center_y - icon_size // 2 if handle.strip() else footer_text_y - icon_size // 2

        # Calculate total width based on what's actually present
        # LinkedIn icon + gap + Instagram icon + gap + handle (if present) + separator (if both present) + Globe icon + gap + website (if present)
        total_width = icon_size + gap + icon_size + gap  # LinkedIn + Instagram icons
        if handle.strip():
            total_width += handle_width + gap
        if handle.strip() and website.strip():
            total_width += sep_width + gap
        if website.strip():
            total_width += icon_size + gap + website_width
        else:
            total_width += icon_size  # Globe icon even if no website

        # Ensure footer doesn't exceed canvas width
        total_width = min(total_width, CANVAS_WIDTH - MARGIN_X * 2)

        # Start position (centered, but ensure it fits within canvas)
        start_x = max(MARGIN_X, (CANVAS_WIDTH - total_width) // 2)
        current_x = start_x

        # Draw LinkedIn icon
        self._draw_linkedin_icon(draw, current_x, icon_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw Instagram icon
        self._draw_instagram_icon(draw, current_x, icon_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw handle text with shadow (only if present)
        if handle.strip():
            shadow_offset = 2
            draw.text(
                (current_x + shadow_offset, footer_text_y + shadow_offset),
                handle,
                fill=COLORS["footer_shadow"],
                font=footer_font,
            )
            draw.text(
                (current_x, footer_text_y),
                handle,
                fill=COLORS["footer"],
                font=footer_font,
            )
            current_x += handle_width + gap

        # Draw separator (only if both handle and website are present)
        if handle.strip() and website.strip():
            shadow_offset = 2
            draw.text(
                (current_x + shadow_offset, footer_text_y + shadow_offset),
                separator,
                fill=COLORS["footer_shadow"],
                font=footer_font,
            )
            draw.text(
                (current_x, footer_text_y),
                separator,
                fill=COLORS["footer"],
                font=footer_font,
            )
            current_x += sep_width + gap

        # Draw Globe icon
        self._draw_globe_icon(draw, current_x, icon_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw website text with shadow (only if present)
        if website.strip():
            shadow_offset = 2
            draw.text(
                (current_x + shadow_offset, footer_text_y + shadow_offset),
                website,
                fill=COLORS["footer_shadow"],
                font=footer_font,
            )
            draw.text(
                (current_x, footer_text_y),
                website,
                fill=COLORS["footer"],
                font=footer_font,
            )

    def _draw_card(
        self, draw: ImageDraw, y: int, height: int, padding: int = 20,
        is_header: bool = False
    ) -> None:
        """Draw rounded card background with semi-transparent fill.

        Args:
            draw: ImageDraw object
            y: Y position of the card content (card starts at y - padding)
            height: Height of the content inside the card
            padding: Padding around the content
            is_header: If True, uses slightly more opaque background for title
        """
        # Use more opaque bg for header, more transparent for sections
        bg_color = COLORS["card_bg"] if is_header else COLORS["section_bg"]

        draw.rounded_rectangle(
            [
                (MARGIN_X - padding, y - padding),
                (MARGIN_X + CONTENT_WIDTH + padding, y + height),
            ],
            radius=24,
            fill=bg_color,
        )

    def render_infographic(
        self,
        base_image_base64: str,
        title: str,
        subtitle: Optional[str] = None,
        sections: Optional[List[dict]] = None,
        takeaway: Optional[str] = None,
        add_footer: bool = True,
        layout: Literal["infographic", "checklist", "quote", "comparison"] = "infographic",
    ) -> str:
        """
        Render infographic with text overlay (Step 3 - Multiple Layouts).

        Args:
            base_image_base64: Base64 encoded SDXL-generated image
            title: Main headline
            subtitle: Optional subtitle/context
            sections: List of section dicts with 'title' and 'bullets' keys
            takeaway: Optional takeaway message
            add_footer: Whether to add branding footer
            layout: Layout template to use

        Returns:
            Base64 encoded final image
        """
        # Route to appropriate layout renderer
        if layout == "checklist":
            return self._render_checklist_layout(
                base_image_base64, title, subtitle, sections, takeaway, add_footer
            )
        elif layout == "quote":
            return self._render_quote_layout(
                base_image_base64, title, subtitle, takeaway, add_footer
            )
        elif layout == "comparison":
            return self._render_comparison_layout(
                base_image_base64, title, subtitle, sections, takeaway, add_footer
            )
        else:
            # Default infographic layout
            return self._render_infographic_layout(
                base_image_base64, title, subtitle, sections, takeaway, add_footer
            )

    def _render_infographic_layout(
        self,
        base_image_base64: str,
        title: str,
        subtitle: Optional[str] = None,
        sections: Optional[List[dict]] = None,
        takeaway: Optional[str] = None,
        add_footer: bool = True,
    ) -> str:
        """Render standard infographic layout (multi-panel with sections)."""
        # Decode base image
        image_data = base64.b64decode(base_image_base64)
        img = Image.open(io.BytesIO(image_data)).convert("RGBA")

        # Resize if needed (SDXL should generate 768x1344, but handle variations)
        if img.size != (CANVAS_WIDTH, CANVAS_HEIGHT):
            img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)

        # Create overlay for text
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Adaptive font sizing to ensure ALL sections always render
        # Start with base sizes and reduce if needed
        font_scale = 1.0
        title_size = 52
        subtitle_size = 32
        section_size = 36
        body_size = 28

        # Try to fit everything with adaptive sizing (max 5 attempts)
        for attempt in range(5):
            # Load fonts with current scale
            title_font = self._load_font("bold", int(title_size * font_scale))
            subtitle_font = self._load_font("regular", int(subtitle_size * font_scale))
            section_font = self._load_font("bold", int(section_size * font_scale))
            body_font = self._load_font("regular", int(body_size * font_scale))
            footer_font = self._load_font("regular", 24)  # Footer size stays constant

            # Calculate heights with current font sizes
            title_lines = self._wrap_text(draw, title, title_font, CONTENT_WIDTH - 40)
            subtitle_lines = []
            if subtitle:
                subtitle_lines = self._wrap_text(draw, subtitle, subtitle_font, CONTENT_WIDTH - 40)

            # Calculate line heights based on font size (proportional)
            title_line_height = int(60 * font_scale)
            subtitle_line_height = int(40 * font_scale)
            section_title_height = int(50 * font_scale)
            bullet_line_height = int(34 * font_scale)
            bullet_spacing = int(8 * font_scale)
            takeaway_line_height = int(44 * font_scale)

            header_height = len(title_lines) * title_line_height + len(subtitle_lines) * subtitle_line_height + int(40 * font_scale)
            header_card_bottom = MARGIN_Y + header_height

            # Pre-calculate section heights
            section_heights = []
            if sections:
                for section in sections:
                    section_title = section.get("title", "")
                    bullets = section.get("bullets", [])
                    section_height = section_title_height if section_title else int(10 * font_scale)
                    for bullet in bullets:
                        bullet_lines = self._wrap_text(draw, bullet, body_font, CONTENT_WIDTH - 80)
                        section_height += len(bullet_lines) * bullet_line_height + bullet_spacing
                    section_height += int(20 * font_scale)  # Bottom padding
                    section_heights.append(section_height)

            # Calculate takeaway height
            takeaway_height_est = 0
            if takeaway:
                takeaway_lines_est = self._wrap_text(draw, takeaway, section_font, CONTENT_WIDTH - 60)
                takeaway_height_est = len(takeaway_lines_est) * takeaway_line_height + int(40 * font_scale)

            # Calculate total space needed
            total_content_height = header_height + sum(section_heights) + takeaway_height_est

            # Calculate gaps needed (use minimum gaps to fit everything)
            num_overlays = 1 + len(sections) + (1 if takeaway else 0)
            num_gaps = num_overlays - 1 if num_overlays > 1 else 0

            # Use minimum gaps (scaled down) to ensure everything fits
            min_gap = max(12, int(SECTION_GAP * font_scale * 0.4))  # Minimum 12px, scaled
            total_gaps_height = num_gaps * min_gap

            # Check if everything fits
            total_needed = header_card_bottom - MARGIN_Y + sum(section_heights) + takeaway_height_est + total_gaps_height

            if total_needed <= MAX_CONTENT_Y - MARGIN_Y - 20:
                # Everything fits! Break and use these font sizes
                logger.debug(f"Content fits with font_scale={font_scale:.2f}, total_needed={total_needed}px")
                break
            else:
                # Reduce font scale for next attempt
                font_scale *= 0.88  # Reduce by 12% each time
                logger.debug(f"Attempt {attempt + 1}: Content doesn't fit ({total_needed}px > {MAX_CONTENT_Y - MARGIN_Y}px), reducing font scale to {font_scale:.2f}")

        # Final font sizes (may be reduced)
        title_font = self._load_font("bold", int(title_size * font_scale))
        subtitle_font = self._load_font("regular", int(subtitle_size * font_scale))
        section_font = self._load_font("bold", int(section_size * font_scale))
        body_font = self._load_font("regular", int(body_size * font_scale))
        footer_font = self._load_font("regular", 24)

        # Recalculate with final font sizes
        title_lines = self._wrap_text(draw, title, title_font, CONTENT_WIDTH - 40)
        subtitle_lines = []
        if subtitle:
            subtitle_lines = self._wrap_text(draw, subtitle, subtitle_font, CONTENT_WIDTH - 40)

        # Calculate line heights with final scale
        title_line_height = int(60 * font_scale)
        subtitle_line_height = int(40 * font_scale)
        section_title_height = int(50 * font_scale)
        bullet_line_height = int(34 * font_scale)
        bullet_spacing = int(8 * font_scale)
        takeaway_line_height = int(44 * font_scale)

        header_height = len(title_lines) * title_line_height + len(subtitle_lines) * subtitle_line_height + int(40 * font_scale)

        y = MARGIN_Y

        # Draw header card background (more opaque for title visibility)
        self._draw_card(draw, y, header_height, padding=int(24 * font_scale), is_header=True)

        # Title
        for line in title_lines:
            draw.text(
                (MARGIN_X, y),
                line,
                fill=COLORS["title"],
                font=title_font,
            )
            y += title_line_height

        # Subtitle (if provided)
        if subtitle_lines:
            y += int(10 * font_scale)  # Small gap between title and subtitle
            for line in subtitle_lines:
                draw.text(
                    (MARGIN_X, y),
                    line,
                    fill=COLORS["subtitle"],
                    font=subtitle_font,
                )
                y += subtitle_line_height

        # Store header end position for gap calculation
        # Use card bottom position (not text end) for consistent gap calculation
        # Card is drawn from MARGIN_Y - padding to MARGIN_Y + header_height
        header_padding = 24  # Same as padding used in _draw_card for header
        header_card_bottom = MARGIN_Y + header_height  # Card bottom position
        header_end_y = header_card_bottom  # Use card bottom for consistent spacing

        # Actual header content height (from start to end of text)
        header_content_height = y - MARGIN_Y

        # Pre-calculate all section heights for dynamic gap distribution (using final font sizes)
        section_heights = []
        if sections:
            for section in sections:
                section_title = section.get("title", "")
                bullets = section.get("bullets", [])
                section_height = section_title_height if section_title else int(10 * font_scale)
                for bullet in bullets:
                    bullet_lines = self._wrap_text(
                        draw, bullet, body_font, CONTENT_WIDTH - 80
                    )
                    section_height += len(bullet_lines) * bullet_line_height + bullet_spacing
                section_height += int(20 * font_scale)  # Bottom padding
                section_heights.append(section_height)

        # Calculate takeaway height if present
        takeaway_height_est = 0
        if takeaway:
            takeaway_lines_est = self._wrap_text(draw, takeaway, section_font, CONTENT_WIDTH - 60)
            takeaway_height_est = len(takeaway_lines_est) * takeaway_line_height + int(40 * font_scale)

        # Count total overlays: header (1) + sections (N) + takeaway (0 or 1)
        num_overlays = 1  # Header overlay (title + subtitle)
        if sections:
            num_overlays += len(sections)
        if takeaway:
            num_overlays += 1

        # Total gaps needed = overlays - 1
        # Gaps: after header, between sections, before takeaway
        num_gaps = num_overlays - 1 if num_overlays > 1 else 0

        # Calculate total content height (all overlays)
        # Use actual content heights, not card heights (cards include padding)
        total_content_height = header_content_height
        total_content_height += sum(section_heights)
        total_content_height += takeaway_height_est

        # Calculate available space for gaps
        # Start from header card bottom, need space for all remaining content + gaps
        remaining_content_height = sum(section_heights) + takeaway_height_est
        available_space = MAX_CONTENT_Y - header_end_y - remaining_content_height

        # Dynamic gap: distribute available space evenly across ALL gaps
        # Use minimum gaps to ensure everything fits, then distribute extra space
        min_gap = max(12, int(SECTION_GAP * font_scale * 0.4))  # Minimum gap, scaled
        if num_gaps > 0 and available_space > 0:
            # Calculate minimum gaps needed
            min_gaps_total = num_gaps * min_gap
            extra_space = max(0, available_space - min_gaps_total)
            # Distribute extra space evenly, but ensure minimum gap
            dynamic_gap = min_gap + (extra_space // num_gaps if num_gaps > 0 else 0)
            # Cap at reasonable maximum
            dynamic_gap = min(dynamic_gap, int(SECTION_GAP * 2.5))
        else:
            dynamic_gap = min_gap

        # Add dynamic gap after hero section card (consistent with section gaps)
        # Sections start at: previous_section_start_y + section_height + dynamic_gap
        # Hero section card ends at: header_end_y (card bottom)
        # First section should start at: header_end_y + dynamic_gap
        y = header_end_y + dynamic_gap

        # SECTIONS - with overflow protection and proper spacing
        if sections:
            for idx, section in enumerate(sections):
                section_title = section.get("title", "")
                bullets = section.get("bullets", [])

                # Store section start position
                section_start_y = y

                # Use pre-calculated height
                section_height = section_heights[idx] if idx < len(section_heights) else 100

                # CHECK: Would this section overflow into footer area?
                # Check if section fits, accounting for gap after it (except last section before takeaway)
                gap_after = dynamic_gap if (idx < len(sections) - 1 or not takeaway) else dynamic_gap // 2
                if section_start_y + section_height + gap_after > MAX_CONTENT_Y:
                    logger.debug(f"Skipping section '{section_title}' - would overflow")
                    break  # Stop adding sections

                # Draw section card (more transparent than header)
                # Card is drawn from section_start_y with calculated height
                self._draw_card(draw, section_start_y, section_height, padding=int(16 * font_scale), is_header=False)

                # Reset y to section start for content drawing
                y = section_start_y

                # Section title with accent color
                if section_title:
                    draw.text(
                        (MARGIN_X + int(8 * font_scale), y + int(8 * font_scale)),  # Small top padding
                        section_title,
                        fill=COLORS["accent"],
                        font=section_font,
                    )
                    y += section_title_height

                # Bullets with bullet symbols
                for bullet in bullets:
                    # Draw bullet symbol "•" in accent color
                    draw.text(
                        (MARGIN_X + int(16 * font_scale), y),
                        "•",
                        fill=COLORS["bullet"],
                        font=body_font,
                    )

                    # Wrap and draw bullet text
                    bullet_lines = self._wrap_text(
                        draw, bullet, body_font, CONTENT_WIDTH - 80
                    )
                    for line_idx, line in enumerate(bullet_lines):
                        # First line starts after bullet, subsequent lines align
                        x_offset = MARGIN_X + int(40 * font_scale) if line_idx == 0 else MARGIN_X + int(40 * font_scale)
                        draw.text(
                            (x_offset, y),
                            line,
                            fill=COLORS["body"],
                            font=body_font,
                        )
                        y += bullet_line_height
                    y += bullet_spacing  # Space after each bullet point

                # Move to next section position: end of current card + dynamic gap
                # Use full gap for all sections (gap before takeaway handled separately)
                y = section_start_y + section_height + dynamic_gap

        # TAKEAWAY SECTION - ALWAYS render if present (we've already adjusted fonts/gaps to fit)
        if takeaway:
            # Pre-calculate takeaway height
            takeaway_lines = self._wrap_text(draw, takeaway, section_font, CONTENT_WIDTH - 60)
            takeaway_height = len(takeaway_lines) * takeaway_line_height + int(40 * font_scale)

            # Add gap before takeaway (reduce if needed to fit)
            takeaway_start_y = y
            if sections:
                # Use dynamic gap, but reduce it if takeaway won't fit
                gap_before_takeaway = dynamic_gap
                min_gap = max(8, int(SECTION_GAP * font_scale * 0.25))  # Minimum gap, scaled
                # Check if takeaway fits with full gap
                if y + gap_before_takeaway + takeaway_height > MAX_CONTENT_Y - 20:
                    # Reduce gap to minimum needed to fit takeaway
                    gap_before_takeaway = max(min_gap, MAX_CONTENT_Y - 20 - y - takeaway_height)
                    if gap_before_takeaway < min_gap:
                        gap_before_takeaway = min_gap
                takeaway_start_y += gap_before_takeaway

            # Always render takeaway (we've already adjusted to fit)
            y = takeaway_start_y
            self._draw_card(draw, y, takeaway_height, padding=int(16 * font_scale), is_header=True)  # Use header style for emphasis
            for line in takeaway_lines:
                draw.text(
                    (MARGIN_X + int(8 * font_scale), y + int(10 * font_scale)),
                    line,
                    fill=COLORS["title"],
                    font=section_font,
                )
                y += takeaway_line_height
            logger.debug(f"Rendered takeaway at y={takeaway_start_y}, height={takeaway_height}, font_scale={font_scale:.2f}")

        # FOOTER (if enabled)
        if add_footer:
            self._draw_footer(draw, footer_font)

        # Composite overlay onto base image
        result = Image.alpha_composite(img, overlay)

        # Convert to RGB for PNG
        result = result.convert("RGB")

        # Encode to base64
        buffer = io.BytesIO()
        result.save(buffer, format="PNG", optimize=True)
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode("utf-8")

    async def extract_text_from_post_llm(
        self,
        post_text: str,
        short_post: Optional[str] = None,
        use_llm: bool = True,
    ) -> dict:
        """
        Extract structured text from post using LLM (Step 2).

        Args:
            post_text: Full post text
            short_post: Optional short version
            use_llm: Whether to use LLM extraction (default: True)

        Returns:
            Dict with title, subtitle, sections, takeaway
        """
        if use_llm:
            try:
                from .text_extractor import extract_text_structure_llm
                return await extract_text_structure_llm(post_text, short_post)
            except Exception as e:
                logger.warning(f"LLM extraction failed: {e}. Using simple extraction.")

        # Fallback to simple extraction
        return self._simple_extract_text(post_text, short_post)

    def _simple_extract_text(
        self, post_text: str, short_post: Optional[str] = None
    ) -> dict:
        """Simple text extraction fallback. Delegates to text_extractor module."""
        return _text_extractor_simple_extract(post_text, short_post)

    # Legacy method for backward compatibility
    def extract_text_from_post(
        self, post_text: str, short_post: Optional[str] = None
    ) -> dict:
        """Legacy method - use extract_text_from_post_llm for LLM extraction."""
        return self._simple_extract_text(post_text, short_post)

    def _render_checklist_layout(
        self,
        base_image_base64: str,
        title: str,
        subtitle: Optional[str] = None,
        sections: Optional[List[dict]] = None,
        takeaway: Optional[str] = None,
        add_footer: bool = True,
    ) -> str:
        """Render checklist-style layout."""
        image_data = base64.b64decode(base_image_base64)
        img = Image.open(io.BytesIO(image_data)).convert("RGBA")
        if img.size != (CANVAS_WIDTH, CANVAS_HEIGHT):
            img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        title_font = self._load_font("bold", 52)
        subtitle_font = self._load_font("regular", 32)
        body_font = self._load_font("regular", 28)
        footer_font = self._load_font("regular", 24)

        y = MARGIN_Y

        # Header
        title_lines = self._wrap_text(draw, title, title_font, CONTENT_WIDTH - 40)
        header_height = len(title_lines) * 60 + 40
        self._draw_card(draw, y, header_height, padding=24, is_header=True)

        for line in title_lines:
            draw.text((MARGIN_X, y), line, fill=COLORS["title"], font=title_font)
            y += 60

        if subtitle:
            y += 10
            subtitle_lines = self._wrap_text(draw, subtitle, subtitle_font, CONTENT_WIDTH - 40)
            for line in subtitle_lines:
                draw.text((MARGIN_X, y), line, fill=COLORS["subtitle"], font=subtitle_font)
                y += 40

        y += 30

        # Checklist items - each item gets its own subtle background
        all_items = []
        if sections:
            for section in sections:
                all_items.extend(section.get("bullets", []))

        for item in all_items[:8]:
            if y + 50 > MAX_CONTENT_Y:
                break
            item_lines = self._wrap_text(draw, f"✓ {item}", body_font, CONTENT_WIDTH - 60)
            for line in item_lines:
                draw.text((MARGIN_X + 24, y), line, fill=COLORS["body"], font=body_font)
                y += 36
            y += 10

        # Footer
        if add_footer:
            self._draw_footer(draw, footer_font)

        result = Image.alpha_composite(img, overlay).convert("RGB")
        buffer = io.BytesIO()
        result.save(buffer, format="PNG", optimize=True)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def _render_quote_layout(
        self,
        base_image_base64: str,
        title: str,
        subtitle: Optional[str] = None,
        takeaway: Optional[str] = None,
        add_footer: bool = True,
    ) -> str:
        """Render quote-style layout."""
        image_data = base64.b64decode(base_image_base64)
        img = Image.open(io.BytesIO(image_data)).convert("RGBA")
        if img.size != (CANVAS_WIDTH, CANVAS_HEIGHT):
            img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        quote_font = self._load_font("bold", 48)
        author_font = self._load_font("regular", 32)
        footer_font = self._load_font("regular", 24)

        quote_text = takeaway or title
        quote_lines = self._wrap_text(draw, f'"{quote_text}"', quote_font, CONTENT_WIDTH - 80)

        # Center vertically
        total_height = len(quote_lines) * 60
        y = (CANVAS_HEIGHT - FOOTER_HEIGHT - total_height) // 2

        # Draw quote card (header-like for emphasis)
        self._draw_card(draw, y - 20, total_height + 80, padding=30, is_header=True)

        for line in quote_lines:
            draw.text((MARGIN_X + 20, y), line, fill=COLORS["title"], font=quote_font)
            y += 60

        if subtitle:
            draw.text((MARGIN_X + 20, y + 10), f"— {subtitle}", fill=COLORS["subtitle"], font=author_font)

        # Footer
        if add_footer:
            self._draw_footer(draw, footer_font)

        result = Image.alpha_composite(img, overlay).convert("RGB")
        buffer = io.BytesIO()
        result.save(buffer, format="PNG", optimize=True)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

    def _render_comparison_layout(
        self,
        base_image_base64: str,
        title: str,
        subtitle: Optional[str] = None,
        sections: Optional[List[dict]] = None,
        takeaway: Optional[str] = None,
        add_footer: bool = True,
    ) -> str:
        """Render comparison-style layout - side-by-side comparison."""
        image_data = base64.b64decode(base_image_base64)
        img = Image.open(io.BytesIO(image_data)).convert("RGBA")
        if img.size != (CANVAS_WIDTH, CANVAS_HEIGHT):
            img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.Resampling.LANCZOS)

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        title_font = self._load_font("bold", 48)
        section_font = self._load_font("bold", 32)
        body_font = self._load_font("regular", 26)
        footer_font = self._load_font("regular", 24)

        y = MARGIN_Y

        # Title
        title_lines = self._wrap_text(draw, title, title_font, CONTENT_WIDTH - 40)
        header_height = len(title_lines) * 56 + 30
        self._draw_card(draw, y, header_height, padding=24, is_header=True)

        for line in title_lines:
            draw.text((MARGIN_X, y), line, fill=COLORS["title"], font=title_font)
            y += 56

        y += 40

        # Two-column comparison
        if sections and len(sections) >= 2:
            left_section = sections[0]
            right_section = sections[1]
            col_width = (CONTENT_WIDTH - 40) // 2

            # Estimate max height needed
            max_items = min(4, max(len(left_section.get("bullets", [])), len(right_section.get("bullets", []))))
            comparison_height = 50 + max_items * 80

            if y + comparison_height < MAX_CONTENT_Y:
                self._draw_card(draw, y, comparison_height, padding=20, is_header=False)

                # Left column
                left_y = y
                draw.text((MARGIN_X, left_y), left_section.get("title", ""), fill=COLORS["accent"], font=section_font)
                left_y += 40
                for bullet in left_section.get("bullets", [])[:4]:
                    bullet_lines = self._wrap_text(draw, bullet, body_font, col_width - 20)
                    for line in bullet_lines:
                        if left_y + 32 > MAX_CONTENT_Y:
                            break
                        draw.text((MARGIN_X, left_y), line, fill=COLORS["body"], font=body_font)
                        left_y += 32

                # Right column
                right_y = y
                draw.text((MARGIN_X + col_width + 30, right_y), right_section.get("title", ""), fill=COLORS["accent"], font=section_font)
                right_y += 40
                for bullet in right_section.get("bullets", [])[:4]:
                    bullet_lines = self._wrap_text(draw, bullet, body_font, col_width - 20)
                    for line in bullet_lines:
                        if right_y + 32 > MAX_CONTENT_Y:
                            break
                        draw.text((MARGIN_X + col_width + 30, right_y), line, fill=COLORS["body"], font=body_font)
                        right_y += 32

        # Footer
        if add_footer:
            self._draw_footer(draw, footer_font)

        result = Image.alpha_composite(img, overlay).convert("RGB")
        buffer = io.BytesIO()
        result.save(buffer, format="PNG", optimize=True)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

