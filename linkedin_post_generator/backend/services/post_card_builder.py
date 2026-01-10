"""
Post Card Builder
==================
Creates social media style post cards with:
- Dark/Light theme background
- Profile picture (rounded)
- Name and handle
- Post text with nice typography
- Clean, minimal design

No AI generation needed - pure code!
"""

import base64
import io
import os
import textwrap
from typing import Optional, Literal
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont


@dataclass
class PostCardStyle:
    """Visual style configuration for post cards."""
    # Dimensions (synced with carousel size for PDF consistency)
    width: int = 900  # Synced with carousel size
    height: int = 1200  # Synced with carousel size

    # Theme
    theme: Literal['dark', 'light'] = 'dark'

    # Custom background color (overrides theme bg if set)
    custom_bg_color: Optional[tuple] = None

    # Dark theme colors
    dark_bg: tuple = (0, 0, 0)
    dark_text: tuple = (255, 255, 255)
    dark_secondary: tuple = (113, 118, 123)
    dark_accent: tuple = (29, 155, 240)  # Twitter blue

    # Light theme colors
    light_bg: tuple = (255, 255, 255)
    light_text: tuple = (15, 20, 25)
    light_secondary: tuple = (83, 100, 113)
    light_accent: tuple = (29, 155, 240)

    # Typography (increased sizes)
    name_size: int = 44
    handle_size: int = 32
    text_size: int = 48

    # Layout
    padding: int = 60
    avatar_size: int = 80  # Increased from 64

    # Profile
    name: str = "Sachin Saurav"
    handle: str = "@ersachinsaurav"
    verified: bool = True

    @property
    def bg_color(self) -> tuple:
        """Return custom background color if set, otherwise theme-based color."""
        if self.custom_bg_color is not None:
            return self.custom_bg_color
        return self.dark_bg if self.theme == 'dark' else self.light_bg

    @property
    def text_color(self) -> tuple:
        """Return text color based on background brightness for contrast."""
        bg = self.bg_color
        # Calculate brightness (0-255)
        brightness = (bg[0] * 299 + bg[1] * 587 + bg[2] * 114) / 1000
        # Use white text for dark backgrounds, black for light backgrounds
        if brightness < 128:
            return self.dark_text  # White text
        else:
            return self.light_text  # Dark text

    @property
    def secondary_color(self) -> tuple:
        """Return secondary color based on background brightness."""
        bg = self.bg_color
        brightness = (bg[0] * 299 + bg[1] * 587 + bg[2] * 114) / 1000
        if brightness < 128:
            return self.dark_secondary  # Lighter gray for dark backgrounds
        else:
            return self.light_secondary  # Darker gray for light backgrounds

    @property
    def accent_color(self) -> tuple:
        return self.dark_accent if self.theme == 'dark' else self.light_accent


class PostCardBuilder:
    """
    Builds social media style post cards.

    Creates images that look like Twitter/X posts -
    perfect for sharing text-heavy content as images.
    """

    def __init__(self, style: Optional[PostCardStyle] = None):
        self.style = style or PostCardStyle()
        self._load_fonts()

    def _load_fonts(self):
        """Load fonts with fallbacks."""
        bold_paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/SFNSTextCondensed-Bold.otf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]

        regular_paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/SFNS.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]

        self.fonts = {}

        # Load bold fonts - name, text, and button sizes
        for size_name, size in [('name', self.style.name_size), ('text', self.style.text_size), ('button', 28)]:
            loaded = False
            for path in bold_paths:
                try:
                    self.fonts[f'bold_{size_name}'] = ImageFont.truetype(path, size)
                    loaded = True
                    break
                except (OSError, IOError):
                    continue
            if not loaded:
                self.fonts[f'bold_{size_name}'] = ImageFont.load_default()

        # Load regular fonts
        for size_name, size in [('handle', self.style.handle_size), ('text', self.style.text_size)]:
            loaded = False
            for path in regular_paths:
                try:
                    self.fonts[f'regular_{size_name}'] = ImageFont.truetype(path, size)
                    loaded = True
                    break
                except (OSError, IOError):
                    continue
            if not loaded:
                self.fonts[f'regular_{size_name}'] = ImageFont.load_default()

    def _load_font_for_size(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Load font for a specific size (used for carousel). Prefers Lato from assets."""
        # Get assets fonts directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        assets_fonts_dir = os.path.join(base_dir, "assets", "fonts")

        # Prioritize Lato fonts (modern, clean, highly readable)
        font_paths = []

        if bold:
            # Bold fonts - prefer Lato Bold, then Lato Black, then fallbacks
            font_paths = [
                os.path.join(assets_fonts_dir, "Lato-Bold.ttf"),
                os.path.join(assets_fonts_dir, "Lato-Black.ttf"),
                os.path.join(assets_fonts_dir, "Raleway-Bold.ttf"),
                os.path.join(assets_fonts_dir, "SourceSansPro-Bold.ttf"),
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/SFNSTextCondensed-Bold.otf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ]
        else:
            # Regular fonts - prefer Lato Medium, then fallbacks
            font_paths = [
                os.path.join(assets_fonts_dir, "Lato-Medium.ttf"),
                os.path.join(assets_fonts_dir, "Raleway-Medium.ttf"),
                os.path.join(assets_fonts_dir, "SourceSansPro-Semibold.ttf"),
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/SFNS.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]

        for path in font_paths:
            try:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue

        return ImageFont.load_default()

    def _draw_carousel_footer(self, draw: ImageDraw.Draw, y_start: int, height: int, style: PostCardStyle):
        """Draw a compact footer with icons for carousel postcards (consistent with cover)."""
        from ..utils.constants import SOCIAL_BRANDING

        # Get branding info
        branding = SOCIAL_BRANDING
        handle_text = style.handle or branding.get('handle', '@ersachinsaurav')
        website_text = branding.get('website', 'sachinsaurav.dev')

        # Font sizes - 16px to match icon size visually (consistent with carousel cover)
        font_size = 16
        footer_font = self._load_font_for_size(font_size, bold=True)

        # Icon and spacing configuration - icons balanced with 16px text
        icon_size = int(height * 0.38)  # Icons balanced with 16px text
        gap = 5  # Gap between elements

        # Colors based on theme
        if style.theme == 'dark':
            icon_color = (230, 230, 230)  # Bright for dark theme
            text_color = (220, 220, 220)
            sep_color = (160, 160, 160)
        else:
            icon_color = (50, 50, 50)  # Dark icons for light theme
            text_color = (70, 70, 70)
            sep_color = (110, 110, 110)

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
        start_x = (style.width - total_width) // 2
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
        draw.text((current_x, text_y), sep, font=footer_font, fill=sep_color, anchor="lm")
        current_x += sep_width

        # Draw globe icon
        self._draw_globe_icon(draw, current_x, icon_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw website text
        draw.text((current_x, text_y), website_text, font=footer_font, fill=text_color, anchor="lm")

    def _is_dark_color(self, color: tuple) -> bool:
        """Check if a color is dark based on perceived brightness."""
        brightness = (color[0] * 299 + color[1] * 587 + color[2] * 114) / 1000
        return brightness < 128

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
        font = self._load_font_for_size(font_size, bold=True)
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

    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> list[str]:
        """Wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            if bbox[2] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def _draw_avatar(
        self,
        image: Image.Image,
        avatar_base64: Optional[str],
        x: int,
        y: int,
        size: int,
    ) -> Image.Image:
        """Draw circular avatar."""
        if avatar_base64:
            try:
                avatar_data = base64.b64decode(avatar_base64)
                avatar = Image.open(io.BytesIO(avatar_data)).convert('RGBA')
                avatar = avatar.resize((size, size), Image.Resampling.LANCZOS)
            except Exception:
                # Create placeholder
                avatar = self._create_avatar_placeholder(size)
        else:
            avatar = self._create_avatar_placeholder(size)

        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([(0, 0), (size, size)], fill=255)

        # Apply mask
        avatar.putalpha(mask)

        # Convert base to RGBA for compositing
        if image.mode != 'RGBA':
            image = image.convert('RGBA')

        image.paste(avatar, (x, y), avatar)
        return image

    def _create_avatar_placeholder(self, size: int) -> Image.Image:
        """Create a placeholder avatar with initials."""
        s = self.style
        img = Image.new('RGBA', (size, size), s.accent_color)
        draw = ImageDraw.Draw(img)

        # Add initials
        initials = ''.join([n[0].upper() for n in s.name.split()[:2]])
        font = self.fonts.get('bold_name', ImageFont.load_default())

        draw.text(
            (size // 2, size // 2),
            initials,
            font=font,
            fill=(255, 255, 255),
            anchor='mm',
        )

        return img

    def _draw_verified_badge(self, draw: ImageDraw, x: int, y: int, size: int = 20):
        """Draw a verified checkmark badge."""
        # Blue circle
        draw.ellipse(
            [(x, y), (x + size, y + size)],
            fill=self.style.accent_color,
        )

        # White checkmark
        check_points = [
            (x + size * 0.25, y + size * 0.5),
            (x + size * 0.45, y + size * 0.7),
            (x + size * 0.75, y + size * 0.3),
        ]
        draw.line(check_points, fill=(255, 255, 255), width=max(2, size // 8))

    def build(
        self,
        post_text: str,
        avatar_base64: Optional[str] = None,
        short_post: Optional[str] = None,  # Use this if provided, else use post_text
        is_carousel: bool = False,  # Flag for carousel-specific styling
        is_section: bool = False,  # Flag to indicate section card (larger title)
        is_takeaway: bool = False,  # Flag to indicate takeaway/conclusion card
    ) -> tuple[str, int]:
        """
        Build a post card image with dynamic height based on content.

        Args:
            post_text: Full post text (fallback)
            avatar_base64: Optional base64 encoded avatar image
            short_post: Optional shortened version of the post (PLAIN TEXT ONLY)

        Returns:
            Base64 encoded PNG image
        """
        s = self.style

        # For postcards, prefer short_post (punchy summary) over full post_text
        # short_post is specifically crafted to be more impactful for visual content
        # Full post_text is still available if short_post is not provided
        if short_post:
            # Use short_post when available - it's the punchy summary meant for postcards
            display_text = short_post
        else:
            # Fallback to full post_text if short_post not provided
            display_text = post_text

        # For carousel, use fixed height
        if is_carousel:
            calculated_height = s.height  # Fixed 512x512 for carousel
        else:
            # Calculate dynamic height based on actual content (no truncation - show all text)
            text_font = self.fonts.get('regular_text', ImageFont.load_default())
            content_width = s.width - (s.padding * 2)

            # Get actual line height from font
            sample_bbox = text_font.getbbox("Ayg")  # Sample with ascenders and descenders
            actual_line_height = sample_bbox[3] - sample_bbox[1]
            line_height = int(actual_line_height * 1.5)  # 1.5x line spacing

            # Process paragraphs and count actual rendered lines
            paragraphs = display_text.split('\n')
            total_content_height = 0
            paragraph_gap = 25  # Gap between paragraphs (MUST match rendering)

            for i, para in enumerate(paragraphs):
                if para.strip():
                    wrapped = self._wrap_text(para.strip(), text_font, content_width)
                    total_content_height += len(wrapped) * line_height
                else:
                    # Empty line = half paragraph gap
                    total_content_height += paragraph_gap // 2

                # Add paragraph gap after each paragraph (except last)
                if i < len(paragraphs) - 1 and para.strip():
                    total_content_height += paragraph_gap

            # Calculate height: header + text content + bottom padding
            header_height = s.avatar_size + 30  # Avatar + spacing below
            bottom_padding = 30  # Reduced bottom padding for tighter fit

            # Calculate total height with minimal buffer for font rendering variations
            calculated_height = s.padding + header_height + total_content_height + bottom_padding

            # Add small safety buffer (5% extra) to prevent text clipping while minimizing empty space
            calculated_height = int(calculated_height * 1.05)

            # Ensure minimum height of 400px for very short posts
            calculated_height = max(calculated_height, 400)

        # Create image with calculated height
        image = Image.new('RGB', (s.width, calculated_height), s.bg_color)
        draw = ImageDraw.Draw(image)

        # Calculate layout
        y = s.padding

        # === HEADER: Avatar + Name + Handle + Follow Button ===
        # Skip header for carousel slides (they're content-only)
        if not is_carousel:
            avatar_x = s.padding
            avatar_y = y

            # Draw avatar
            image = self._draw_avatar(image, avatar_base64, avatar_x, avatar_y, s.avatar_size)
            draw = ImageDraw.Draw(image)  # Recreate draw object

            # Name and handle next to avatar
            text_x = avatar_x + s.avatar_size + 20

            # Get name dimensions for proper vertical alignment
            name_font = self.fonts.get('bold_name', ImageFont.load_default())
            name_bbox = name_font.getbbox(s.name)
            name_height = name_bbox[3] - name_bbox[1]

            # Handle dimensions
            handle_font = self.fonts.get('regular_handle', ImageFont.load_default())
            handle_bbox = handle_font.getbbox(s.handle)
            handle_height = handle_bbox[3] - handle_bbox[1]

            # Calculate vertical positions to center name+handle block within avatar height
            name_handle_gap = 10  # Gap between name and handle
            total_text_height = name_height + name_handle_gap + handle_height
            text_start_y = avatar_y + (s.avatar_size - total_text_height) // 2

            # Draw name
            name_y = text_start_y
            draw.text((text_x, name_y), s.name, font=name_font, fill=s.text_color)

            # Verified badge - vertically centered with name text baseline
            name_bbox_drawn = draw.textbbox((text_x, name_y), s.name, font=name_font)
            if s.verified:
                badge_size = 24
                badge_x = name_bbox_drawn[2] + 8
                # Use the actual drawn text bounds for better alignment
                drawn_name_height = name_bbox_drawn[3] - name_bbox_drawn[1]
                badge_y = name_bbox_drawn[1] + (drawn_name_height - badge_size) // 2
                self._draw_verified_badge(draw, badge_x, badge_y, badge_size)

            # Handle - with proper spacing from name
            handle_y = name_y + name_height + name_handle_gap
            draw.text((text_x, handle_y), s.handle, font=handle_font, fill=s.secondary_color)

            # Follow button (right side of header) - elegant pill shape
            follow_font = self.fonts.get('bold_button', ImageFont.load_default())
            follow_text = "+ Follow"

            # Calculate text dimensions first
            text_bbox = follow_font.getbbox(follow_text)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            # Button dimensions - slightly larger for better proportions
            button_padding_x = 20
            button_padding_y = 10
            follow_button_width = text_width + (button_padding_x * 2)
            follow_button_height_btn = text_height + (button_padding_y * 2)

            # Ensure minimum width for elegant look
            follow_button_width = max(follow_button_width, 110)

            follow_button_x = s.width - s.padding - follow_button_width
            follow_button_y = avatar_y + (s.avatar_size - follow_button_height_btn) // 2

            # Button styling - clean outline style
            if s.theme == 'dark':
                follow_bg_color = (0, 0, 0)  # Black background
                follow_text_color = (255, 255, 255)  # White text
                border_color = (255, 255, 255)  # White border for visibility
            else:
                follow_bg_color = (255, 255, 255)
                follow_text_color = (0, 0, 0)
                border_color = (0, 0, 0)

            # Draw perfect pill-shaped button
            pill_radius = follow_button_height_btn // 2

            # Method 1: Try PIL's rounded_rectangle (PIL 9.0.0+)
            try:
                draw.rounded_rectangle(
                    [(follow_button_x, follow_button_y),
                     (follow_button_x + follow_button_width, follow_button_y + follow_button_height_btn)],
                    radius=pill_radius,
                    fill=follow_bg_color,
                    outline=border_color,
                    width=2,
                )
            except (AttributeError, TypeError):
                # Method 2: Manual pill drawing for older PIL versions
                # Draw filled pill first
                # Left semicircle
                draw.ellipse(
                    [(follow_button_x, follow_button_y),
                     (follow_button_x + follow_button_height_btn, follow_button_y + follow_button_height_btn)],
                    fill=follow_bg_color,
                )
                # Right semicircle
                draw.ellipse(
                    [(follow_button_x + follow_button_width - follow_button_height_btn, follow_button_y),
                     (follow_button_x + follow_button_width, follow_button_y + follow_button_height_btn)],
                    fill=follow_bg_color,
                )
                # Center rectangle
                draw.rectangle(
                    [(follow_button_x + pill_radius, follow_button_y),
                     (follow_button_x + follow_button_width - pill_radius, follow_button_y + follow_button_height_btn)],
                    fill=follow_bg_color,
                )

                # Draw border outline
                # Left semicircle border
                draw.ellipse(
                    [(follow_button_x, follow_button_y),
                     (follow_button_x + follow_button_height_btn, follow_button_y + follow_button_height_btn)],
                    outline=border_color,
                    width=2,
                )
                # Right semicircle border
                draw.ellipse(
                    [(follow_button_x + follow_button_width - follow_button_height_btn, follow_button_y),
                     (follow_button_x + follow_button_width, follow_button_y + follow_button_height_btn)],
                    outline=border_color,
                    width=2,
                )
                # Top and bottom borders
                draw.line(
                    [(follow_button_x + pill_radius, follow_button_y),
                     (follow_button_x + follow_button_width - pill_radius, follow_button_y)],
                    fill=border_color,
                    width=2,
                )
                draw.line(
                    [(follow_button_x + pill_radius, follow_button_y + follow_button_height_btn),
                     (follow_button_x + follow_button_width - pill_radius, follow_button_y + follow_button_height_btn)],
                    fill=border_color,
                    width=2,
                )

            # Center text perfectly - calculate exact center position
            button_center_x = follow_button_x + follow_button_width // 2
            button_center_y = follow_button_y + follow_button_height_btn // 2

            # Use anchor='mm' if supported, otherwise manual centering
            try:
                draw.text(
                    (button_center_x, button_center_y),
                    follow_text,
                    font=follow_font,
                    fill=follow_text_color,
                    anchor='mm',  # Middle-middle anchor
                )
            except TypeError:
                # Fallback: manual centering
                text_x = button_center_x - text_width // 2
                text_y = button_center_y - text_height // 2
                draw.text(
                    (text_x, text_y),
                    follow_text,
                    font=follow_font,
                    fill=follow_text_color,
                )

            y = avatar_y + s.avatar_size + 30
        else:
            # For carousel, start content from top with padding
            y = s.padding

        # === POST TEXT ===
        paragraph_gap = 25  # Increased for better spacing

        # For carousel, parse text differently
        if is_carousel:
            # Carousel-specific settings for 512x768 dimensions
            carousel_padding = 40  # Good padding for readability
            content_width = s.width - (carousel_padding * 2)

            # Footer area - compact footer at bottom
            footer_height = 50  # Fixed footer height for carousel

            # Calculate available content area (leave space for footer)
            content_area_top = carousel_padding + 20  # Extra top padding
            content_area_bottom = s.height - footer_height - 20
            available_height = content_area_bottom - content_area_top

            paragraphs = display_text.split('\n')

            # Load fonts for carousel - LARGER for better readability on 512x768
            # Increased font sizes significantly
            carousel_title_size = 36  # Large section title
            carousel_text_size = 28   # Readable body text

            # Load carousel-specific fonts
            section_title_font = self._load_font_for_size(carousel_title_size, bold=True)
            text_font = self._load_font_for_size(carousel_text_size, bold=False)

            # Get line heights with comfortable spacing
            title_bbox = section_title_font.getbbox("Ayg")
            title_line_height = int((title_bbox[3] - title_bbox[1]) * 1.4)
            text_bbox_sample = text_font.getbbox("Ayg")
            text_line_height = int((text_bbox_sample[3] - text_bbox_sample[1]) * 1.5)

            # First pass: calculate total content height for vertical centering
            total_content_height = 0
            content_elements = []  # Store (type, lines) tuples

            for i, para in enumerate(paragraphs):
                if not para.strip():
                    content_elements.append(('gap', paragraph_gap // 2))
                    total_content_height += paragraph_gap // 2
                    continue

                # First paragraph is title (for sections or takeaway)
                if i == 0 and (is_section or is_takeaway):
                    lines = self._wrap_text(para.strip(), section_title_font, content_width)
                    height = len(lines) * title_line_height + paragraph_gap
                    content_elements.append(('title', lines))
                    total_content_height += height
                else:
                    lines = self._wrap_text(para.strip(), text_font, content_width)
                    height = len(lines) * text_line_height
                    content_elements.append(('text', lines))
                    total_content_height += height

                    # Add paragraph gap after each (except last non-empty)
                    if i < len(paragraphs) - 1:
                        content_elements.append(('gap', paragraph_gap))
                        total_content_height += paragraph_gap

            # Calculate starting Y to vertically center content
            y_offset = max(0, (available_height - total_content_height) // 2)
            y = content_area_top + y_offset

            # Second pass: draw content
            for element_type, element_data in content_elements:
                if y >= content_area_bottom:
                    break  # Stop if we exceed bounds

                if element_type == 'gap':
                    y += element_data
                elif element_type == 'title':
                    for line in element_data:
                        if y + title_line_height > content_area_bottom:
                            break
                        draw.text((carousel_padding, y), line, font=section_title_font, fill=s.text_color)
                        y += title_line_height
                    y += paragraph_gap  # Extra gap after title
                elif element_type == 'text':
                    for line in element_data:
                        if y + text_line_height > content_area_bottom:
                            break
                        draw.text((carousel_padding, y), line, font=text_font, fill=s.text_color)
                        y += text_line_height

            # Add footer overlay for better visibility
            # Convert image to RGBA temporarily for compositing
            image_rgba = image.convert('RGBA')
            footer_overlay = Image.new('RGBA', (s.width, footer_height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(footer_overlay)

            # Create gradient overlay from transparent to semi-transparent
            # This ensures footer is visible regardless of background color
            bg_brightness = (s.bg_color[0] * 299 + s.bg_color[1] * 587 + s.bg_color[2] * 114) / 1000
            if bg_brightness < 128:
                # Dark background - use light overlay
                overlay_base = (255, 255, 255)
            else:
                # Light background - use dark overlay
                overlay_base = (0, 0, 0)

            # Draw gradient overlay (fade from transparent at top to opaque at bottom)
            for i in range(footer_height):
                alpha = int(200 * (i / footer_height))  # Fade from 0 to 200 opacity
                overlay_color = overlay_base + (alpha,)
                overlay_draw.rectangle(
                    [(0, i), (s.width, i + 1)],
                    fill=overlay_color
                )

            # Composite overlay onto image
            footer_y = s.height - footer_height
            footer_overlay_positioned = Image.new('RGBA', image_rgba.size, (0, 0, 0, 0))
            footer_overlay_positioned.paste(footer_overlay, (0, footer_y))
            image_rgba = Image.alpha_composite(image_rgba, footer_overlay_positioned)

            # Convert back to RGB
            image = image_rgba.convert('RGB')
            draw = ImageDraw.Draw(image)  # Recreate draw after compositing

            # Draw compact footer for carousel postcards
            self._draw_carousel_footer(draw, s.height - footer_height, footer_height, s)
        else:
            # Non-carousel: use existing logic
            text_font = self.fonts.get('regular_text', ImageFont.load_default())
            text_bbox = text_font.getbbox("Ayg")
            line_height = int((text_bbox[3] - text_bbox[1]) * 1.5)
            paragraphs = display_text.split('\n')

            # Calculate content width for text wrapping
            content_width = s.width - (s.padding * 2)

            for i, para in enumerate(paragraphs):
                if not para.strip():
                    y += paragraph_gap // 2  # Empty line = half paragraph gap
                    continue

                lines = self._wrap_text(para.strip(), text_font, content_width)

                for line in lines:
                    draw.text((s.padding, y), line, font=text_font, fill=s.text_color)
                    y += line_height

                # Add paragraph gap after each paragraph (except last)
                if i < len(paragraphs) - 1:
                    y += paragraph_gap

        # Convert to bytes
        buffer = io.BytesIO()
        image.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode('utf-8'), calculated_height


# Convenience function
def create_post_card(
    post_text: str,
    short_post: Optional[str] = None,
    avatar_base64: Optional[str] = None,
    theme: Literal['dark', 'light'] = 'dark',
    name: str = "Sachin Saurav",
    handle: str = "@ersachinsaurav",
) -> tuple[str, int]:
    """
    Quick function to create a post card.

    Returns tuple of (base64 encoded PNG, height).
    """
    style = PostCardStyle(
        theme=theme,
        name=name,
        handle=handle,
    )
    builder = PostCardBuilder(style)
    return builder.build(post_text, avatar_base64, short_post)

