"""
Quote Card Builder
==================
Creates beautiful quote cards with textured backgrounds and clean typography.
Inspired by viral LinkedIn/Instagram quote posts.

Styles:
- Paper texture (like Wan-styled freelancing quotes)
- Solid dark (like Jean Lee posts)
- Grid paper (like society conditioning posts)
- Highlight style (like Sibel Terhaar quote)

All images are consistent regardless of which AI provider generates the background.
Text is applied programmatically for perfect control.
"""

import base64
import io
import os
import random
from typing import Optional, Literal, Tuple
from dataclasses import dataclass
from enum import Enum

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_FONTS_DIR = os.path.join(BASE_DIR, "assets", "fonts")


class QuoteStyle(str, Enum):
    """Visual styles for quote cards."""
    PAPER_TEXTURE = "paper_texture"  # White/cream paper with black text
    DARK_SOLID = "dark_solid"        # Dark background with white text (Jean Lee style)
    GRID_PAPER = "grid_paper"        # Graph paper with handwritten-style text
    HIGHLIGHT = "highlight"          # Grey background with yellow highlighted text
    WHITEBOARD = "whiteboard"        # Whiteboard with blue marker text
    MINIMAL = "minimal"              # Ultra clean, lots of whitespace


@dataclass
class QuoteCardConfig:
    """Configuration for quote card generation."""
    width: int = 900
    height: int = 1200
    style: QuoteStyle = QuoteStyle.PAPER_TEXTURE

    # Text settings
    main_text: str = ""
    subtitle: str = ""  # Optional attribution or subtitle

    # Profile settings (optional - for Jean Lee style)
    show_profile: bool = False
    profile_name: str = ""
    profile_handle: str = ""
    profile_image_base64: Optional[str] = None

    # Branding
    show_footer: bool = True
    footer_handle: str = "@ersachinsaurav"
    footer_website: str = "sachinsaurav.dev"


class QuoteCardBuilder:
    """
    Builds quote cards with various textured backgrounds.

    All text is applied programmatically for:
    - Perfect typography control
    - Consistency across all AI providers
    - No AI hallucinations in text
    """

    def __init__(self):
        self._load_fonts()

    def _load_fonts(self):
        """Load fonts with fallbacks, prioritizing assets fonts."""
        self.fonts = {}

        # Font configurations: (key, size, bold, preferred_fonts)
        font_configs = [
            ("title_large", 56, True, ["Raleway-Heavy.ttf", "Lato-Black.ttf"]),
            ("title", 44, True, ["Raleway-Bold.ttf", "Lato-Bold.ttf"]),
            ("body", 36, False, ["Lato-Medium.ttf", "SourceSansPro-Semibold.ttf"]),
            ("body_large", 42, False, ["Lato-Medium.ttf", "SourceSansPro-Semibold.ttf"]),
            ("subtitle", 28, False, ["Lato-Medium.ttf", "SourceSansPro-Semibold.ttf"]),
            ("footer", 18, True, ["Lato-Bold.ttf", "SourceSansPro-Bold.ttf"]),
            ("handle", 24, False, ["Lato-Medium.ttf"]),
        ]

        system_fallbacks = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]

        for key, size, bold, preferred in font_configs:
            font = None

            # Try preferred fonts from assets
            for font_name in preferred:
                path = os.path.join(ASSETS_FONTS_DIR, font_name)
                if os.path.exists(path):
                    try:
                        font = ImageFont.truetype(path, size)
                        break
                    except (OSError, IOError):
                        continue

            # Fallback to system fonts
            if font is None:
                for path in system_fallbacks:
                    try:
                        font = ImageFont.truetype(path, size)
                        break
                    except (OSError, IOError):
                        continue

            # Final fallback
            if font is None:
                font = ImageFont.load_default()

            self.fonts[key] = font

    def _get_font(self, key: str) -> ImageFont.FreeTypeFont:
        """Get font by key."""
        return self.fonts.get(key, ImageFont.load_default())

    def _load_font_for_size(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
        """Load font for a specific size."""
        font_files = (
            ["Lato-Bold.ttf", "Raleway-Bold.ttf"] if bold
            else ["Lato-Medium.ttf", "SourceSansPro-Semibold.ttf"]
        )

        for font_name in font_files:
            path = os.path.join(ASSETS_FONTS_DIR, font_name)
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except (OSError, IOError):
                    continue

        return ImageFont.load_default()

    def _create_paper_texture(self, width: int, height: int) -> Image.Image:
        """Create a subtle paper texture background."""
        # Base cream/off-white color
        base_color = (252, 250, 245)  # Warm off-white
        img = Image.new('RGB', (width, height), base_color)
        draw = ImageDraw.Draw(img)

        # Add subtle noise for paper texture
        for _ in range(width * height // 50):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            # Subtle grey dots
            grey = random.randint(240, 252)
            img.putpixel((x, y), (grey, grey, grey))

        # Apply slight blur for smoothness
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))

        return img

    def _create_dark_solid(self, width: int, height: int) -> Image.Image:
        """Create a dark solid background (Jean Lee style)."""
        # Deep dark blue-grey
        base_color = (30, 39, 46)  # #1e272e
        return Image.new('RGB', (width, height), base_color)

    def _create_grid_paper(self, width: int, height: int) -> Image.Image:
        """Create a grid paper background."""
        # White base
        img = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Grid settings
        grid_size = 30  # pixels between lines
        grid_color = (220, 225, 230)  # Light grey-blue

        # Draw vertical lines
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=1)

        # Draw horizontal lines
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill=grid_color, width=1)

        return img

    def _create_highlight_bg(self, width: int, height: int) -> Image.Image:
        """Create a grey textured background for highlight style."""
        base_color = (235, 235, 235)  # Light grey
        img = Image.new('RGB', (width, height), base_color)

        # Add subtle texture
        for _ in range(width * height // 30):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            grey = random.randint(230, 240)
            img.putpixel((x, y), (grey, grey, grey))

        img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
        return img

    def _create_whiteboard(self, width: int, height: int) -> Image.Image:
        """Create a whiteboard background."""
        # Slightly off-white with subtle gradient
        img = Image.new('RGB', (width, height), (250, 252, 255))
        draw = ImageDraw.Draw(img)

        # Add subtle shine gradient (lighter at top)
        for y in range(height // 4):
            alpha = 1 - (y / (height // 4))
            brightness = int(255 + (5 * alpha))  # Slightly brighter at top
            brightness = min(255, brightness)
            draw.line([(0, y), (width, y)], fill=(brightness, brightness, 255))

        # Add frame shadow on edges
        frame_width = 8
        shadow_color = (220, 225, 230)
        # Top
        draw.rectangle([(0, 0), (width, frame_width)], fill=shadow_color)
        # Bottom
        draw.rectangle([(0, height - frame_width), (width, height)], fill=shadow_color)
        # Left
        draw.rectangle([(0, 0), (frame_width, height)], fill=shadow_color)
        # Right
        draw.rectangle([(width - frame_width, 0), (width, height)], fill=shadow_color)

        return img

    def _create_minimal(self, width: int, height: int) -> Image.Image:
        """Create a minimal white background."""
        return Image.new('RGB', (width, height), (255, 255, 255))

    def _create_background(self, config: QuoteCardConfig) -> Image.Image:
        """Create background based on style."""
        creators = {
            QuoteStyle.PAPER_TEXTURE: self._create_paper_texture,
            QuoteStyle.DARK_SOLID: self._create_dark_solid,
            QuoteStyle.GRID_PAPER: self._create_grid_paper,
            QuoteStyle.HIGHLIGHT: self._create_highlight_bg,
            QuoteStyle.WHITEBOARD: self._create_whiteboard,
            QuoteStyle.MINIMAL: self._create_minimal,
        }

        creator = creators.get(config.style, self._create_paper_texture)
        return creator(config.width, config.height)

    def _get_text_color(self, style: QuoteStyle) -> Tuple[int, int, int]:
        """Get appropriate text color for background style."""
        if style == QuoteStyle.DARK_SOLID:
            return (255, 255, 255)  # White on dark
        elif style == QuoteStyle.WHITEBOARD:
            return (0, 100, 180)  # Blue marker color
        else:
            return (20, 20, 20)  # Near-black on light backgrounds

    def _get_subtitle_color(self, style: QuoteStyle) -> Tuple[int, int, int]:
        """Get subtitle/secondary text color."""
        if style == QuoteStyle.DARK_SOLID:
            return (180, 180, 180)  # Light grey on dark
        else:
            return (100, 100, 100)  # Dark grey on light

    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
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

    def _draw_highlighted_text(
        self,
        draw: ImageDraw.Draw,
        text: str,
        font: ImageFont.FreeTypeFont,
        x: int,
        y: int,
        max_width: int,
        text_color: Tuple[int, int, int],
        highlight_color: Tuple[int, int, int] = (255, 247, 140)  # Yellow highlight
    ) -> int:
        """Draw text with highlight effect (like Sibel Terhaar quote)."""
        lines = self._wrap_text(text, font, max_width)

        # Get line height
        sample_bbox = font.getbbox("Ayg")
        line_height = int((sample_bbox[3] - sample_bbox[1]) * 1.6)
        highlight_padding = 8

        current_y = y
        for line in lines:
            # Get line dimensions
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_text_height = bbox[3] - bbox[1]

            # Draw highlight rectangle
            highlight_y = current_y - highlight_padding // 2
            highlight_height = line_text_height + highlight_padding
            draw.rectangle(
                [(x - highlight_padding, highlight_y),
                 (x + line_width + highlight_padding, highlight_y + highlight_height)],
                fill=highlight_color
            )

            # Draw text
            draw.text((x, current_y), line, font=font, fill=text_color)
            current_y += line_height

        return current_y

    def _draw_footer(
        self,
        draw: ImageDraw.Draw,
        config: QuoteCardConfig,
        y_position: int
    ):
        """Draw footer with social handles."""
        if not config.show_footer:
            return

        footer_font = self._get_font("footer")
        footer_text = f"{config.footer_handle} • {config.footer_website}"

        # Calculate position (centered)
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        text_width = bbox[2] - bbox[0]
        x = (config.width - text_width) // 2

        # Get color based on style
        if config.style == QuoteStyle.DARK_SOLID:
            color = (150, 150, 150)
        else:
            color = (120, 120, 120)

        draw.text((x, y_position), footer_text, font=footer_font, fill=color)

    def _draw_profile_header(
        self,
        img: Image.Image,
        draw: ImageDraw.Draw,
        config: QuoteCardConfig,
        y_start: int
    ) -> int:
        """Draw profile header (Jean Lee style) and return new y position."""
        if not config.show_profile:
            return y_start

        padding = 60
        avatar_size = 64

        # Draw avatar circle (placeholder or image)
        avatar_x = padding
        avatar_y = y_start

        if config.profile_image_base64:
            try:
                avatar_data = base64.b64decode(config.profile_image_base64)
                avatar = Image.open(io.BytesIO(avatar_data)).convert('RGBA')
                avatar = avatar.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)

                # Create circular mask
                mask = Image.new('L', (avatar_size, avatar_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([(0, 0), (avatar_size, avatar_size)], fill=255)
                avatar.putalpha(mask)

                img.paste(avatar, (avatar_x, avatar_y), avatar)
            except Exception:
                # Draw placeholder circle
                draw.ellipse(
                    [(avatar_x, avatar_y), (avatar_x + avatar_size, avatar_y + avatar_size)],
                    fill=(255, 200, 50)  # Yellow circle placeholder
                )
        else:
            # Draw placeholder circle
            draw.ellipse(
                [(avatar_x, avatar_y), (avatar_x + avatar_size, avatar_y + avatar_size)],
                fill=(255, 200, 50)
            )

        # Name and handle
        text_x = avatar_x + avatar_size + 15
        name_font = self._get_font("subtitle")
        handle_font = self._get_font("handle")

        # Get colors
        if config.style == QuoteStyle.DARK_SOLID:
            name_color = (255, 255, 255)
            handle_color = (150, 150, 150)
            verified_color = (29, 155, 240)
        else:
            name_color = (30, 30, 30)
            handle_color = (100, 100, 100)
            verified_color = (29, 155, 240)

        # Draw name
        name_y = avatar_y + 8
        draw.text((text_x, name_y), config.profile_name, font=name_font, fill=name_color)

        # Verified badge (blue checkmark)
        name_bbox = draw.textbbox((text_x, name_y), config.profile_name, font=name_font)
        badge_x = name_bbox[2] + 8
        badge_y = name_y + 4
        badge_size = 18
        draw.ellipse(
            [(badge_x, badge_y), (badge_x + badge_size, badge_y + badge_size)],
            fill=verified_color
        )
        # Draw checkmark
        check_points = [
            (badge_x + badge_size * 0.25, badge_y + badge_size * 0.5),
            (badge_x + badge_size * 0.45, badge_y + badge_size * 0.7),
            (badge_x + badge_size * 0.75, badge_y + badge_size * 0.3),
        ]
        draw.line(check_points, fill=(255, 255, 255), width=2)

        # Draw handle
        handle_y = name_y + 28
        draw.text((text_x, handle_y), config.profile_handle, font=handle_font, fill=handle_color)

        return avatar_y + avatar_size + 40  # Return new y position

    def build(self, config: QuoteCardConfig) -> str:
        """
        Build a quote card image.

        Args:
            config: QuoteCardConfig with all settings

        Returns:
            Base64 encoded PNG image
        """
        # Create background
        img = self._create_background(config)
        draw = ImageDraw.Draw(img)

        # Layout settings
        padding = 60
        content_width = config.width - (padding * 2)

        # Get colors
        text_color = self._get_text_color(config.style)
        subtitle_color = self._get_subtitle_color(config.style)

        # Start y position (leave room for profile if shown)
        current_y = padding

        # Draw profile header if configured
        if config.show_profile:
            current_y = self._draw_profile_header(img, draw, config, current_y)
            # Need to recreate draw after paste
            draw = ImageDraw.Draw(img)

        # Choose font based on text length
        text_length = len(config.main_text)
        if text_length < 100:
            text_font = self._get_font("title_large")
        elif text_length < 200:
            text_font = self._get_font("body_large")
        else:
            text_font = self._get_font("body")

        # Calculate text height for vertical centering
        lines = self._wrap_text(config.main_text, text_font, content_width)
        sample_bbox = text_font.getbbox("Ayg")
        line_height = int((sample_bbox[3] - sample_bbox[1]) * 1.5)
        total_text_height = len(lines) * line_height

        # Add subtitle height if present
        if config.subtitle:
            subtitle_font = self._get_font("subtitle")
            subtitle_lines = self._wrap_text(config.subtitle, subtitle_font, content_width)
            sub_bbox = subtitle_font.getbbox("Ayg")
            sub_line_height = int((sub_bbox[3] - sub_bbox[1]) * 1.4)
            total_text_height += 30 + (len(subtitle_lines) * sub_line_height)

        # Calculate available space and center vertically
        footer_space = 80 if config.show_footer else 20
        available_height = config.height - current_y - footer_space
        text_start_y = current_y + max(0, (available_height - total_text_height) // 2)

        # Draw main text
        if config.style == QuoteStyle.HIGHLIGHT:
            # Use highlight effect
            text_y = self._draw_highlighted_text(
                draw, config.main_text, text_font,
                padding, text_start_y, content_width,
                text_color
            )
        else:
            # Regular text drawing
            text_y = text_start_y
            for line in lines:
                draw.text((padding, text_y), line, font=text_font, fill=text_color)
                text_y += line_height

        # Draw subtitle/attribution
        if config.subtitle:
            text_y += 30  # Gap before subtitle
            subtitle_font = self._get_font("subtitle")
            subtitle_lines = self._wrap_text(config.subtitle, subtitle_font, content_width)
            sub_bbox = subtitle_font.getbbox("Ayg")
            sub_line_height = int((sub_bbox[3] - sub_bbox[1]) * 1.4)

            for line in subtitle_lines:
                draw.text((padding, text_y), line, font=subtitle_font, fill=subtitle_color)
                text_y += sub_line_height

        # Draw footer
        if config.show_footer:
            footer_y = config.height - 50
            self._draw_footer(draw, config, footer_y)

        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode('utf-8')

    def build_from_ai_background(
        self,
        ai_image_base64: str,
        config: QuoteCardConfig
    ) -> str:
        """
        Apply text overlay to an AI-generated background image.

        This allows ANY AI provider (Nova, Titan, SDXL) to generate
        simple textured backgrounds, and we add clean text on top.

        Args:
            ai_image_base64: Base64 AI-generated background image
            config: QuoteCardConfig with text and styling

        Returns:
            Base64 encoded PNG with text overlay
        """
        # Decode AI image
        img_data = base64.b64decode(ai_image_base64)
        img_buffer = io.BytesIO(img_data)
        img = Image.open(img_buffer).convert('RGBA')

        # Resize if needed
        if img.size != (config.width, config.height):
            img = img.resize((config.width, config.height), Image.Resampling.LANCZOS)

        # Convert to RGB for drawing
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)

        # Analyze image brightness to choose text color
        # Sample pixels from center area
        sample_region = img.crop((
            config.width // 4,
            config.height // 4,
            3 * config.width // 4,
            3 * config.height // 4
        ))
        avg_color = sample_region.resize((1, 1)).getpixel((0, 0))
        brightness = (avg_color[0] * 299 + avg_color[1] * 587 + avg_color[2] * 114) / 1000

        # Choose text color based on brightness
        if brightness < 128:
            text_color = (255, 255, 255)  # White text on dark bg
            subtitle_color = (200, 200, 200)
        else:
            text_color = (30, 30, 30)  # Dark text on light bg
            subtitle_color = (80, 80, 80)

        # Layout settings
        padding = 60
        content_width = config.width - (padding * 2)

        # Choose font based on text length
        text_length = len(config.main_text)
        if text_length < 100:
            text_font = self._get_font("title_large")
        elif text_length < 200:
            text_font = self._get_font("body_large")
        else:
            text_font = self._get_font("body")

        # Calculate text layout
        lines = self._wrap_text(config.main_text, text_font, content_width)
        sample_bbox = text_font.getbbox("Ayg")
        line_height = int((sample_bbox[3] - sample_bbox[1]) * 1.5)
        total_text_height = len(lines) * line_height

        # Add subtitle height
        if config.subtitle:
            total_text_height += 50  # Gap + subtitle

        # Vertical centering
        footer_space = 80 if config.show_footer else 20
        available_height = config.height - padding - footer_space
        text_start_y = padding + max(0, (available_height - total_text_height) // 2)

        # Draw text with slight shadow for readability on any background
        shadow_offset = 2
        shadow_color = (0, 0, 0, 80) if brightness > 128 else (255, 255, 255, 40)

        text_y = text_start_y
        for line in lines:
            # Shadow (for readability)
            draw.text((padding + shadow_offset, text_y + shadow_offset), line,
                     font=text_font, fill=shadow_color[:3])
            # Main text
            draw.text((padding, text_y), line, font=text_font, fill=text_color)
            text_y += line_height

        # Draw subtitle
        if config.subtitle:
            text_y += 30
            subtitle_font = self._get_font("subtitle")
            subtitle_lines = self._wrap_text(config.subtitle, subtitle_font, content_width)
            sub_bbox = subtitle_font.getbbox("Ayg")
            sub_line_height = int((sub_bbox[3] - sub_bbox[1]) * 1.4)

            for line in subtitle_lines:
                draw.text((padding, text_y), line, font=subtitle_font, fill=subtitle_color)
                text_y += sub_line_height

        # Draw footer
        if config.show_footer:
            footer_y = config.height - 50
            footer_color = (180, 180, 180) if brightness < 128 else (120, 120, 120)
            footer_font = self._get_font("footer")
            footer_text = f"{config.footer_handle} • {config.footer_website}"
            bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
            text_width = bbox[2] - bbox[0]
            x = (config.width - text_width) // 2
            draw.text((x, footer_y), footer_text, font=footer_font, fill=footer_color)

        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode('utf-8')


# Convenience functions
def create_quote_card(
    text: str,
    subtitle: str = "",
    style: QuoteStyle = QuoteStyle.PAPER_TEXTURE,
    show_footer: bool = True,
) -> str:
    """
    Quick function to create a quote card.

    Returns base64 encoded PNG.
    """
    config = QuoteCardConfig(
        main_text=text,
        subtitle=subtitle,
        style=style,
        show_footer=show_footer,
    )
    builder = QuoteCardBuilder()
    return builder.build(config)


def create_jean_lee_style(
    quote_text: str,
    profile_name: str = "Sachin Saurav",
    profile_handle: str = "@ersachinsaurav",
    profile_image_base64: Optional[str] = None,
) -> str:
    """
    Create a Jean Lee style quote card (dark bg + profile + bold text).

    Returns base64 encoded PNG.
    """
    config = QuoteCardConfig(
        main_text=quote_text,
        style=QuoteStyle.DARK_SOLID,
        show_profile=True,
        profile_name=profile_name,
        profile_handle=profile_handle,
        profile_image_base64=profile_image_base64,
        show_footer=False,  # Jean Lee style doesn't have footer
    )
    builder = QuoteCardBuilder()
    return builder.build(config)


def apply_text_to_ai_background(
    ai_image_base64: str,
    text: str,
    subtitle: str = "",
    show_footer: bool = True,
) -> str:
    """
    Apply text overlay to an AI-generated background.
    Works with ANY AI provider (Nova, Titan, SDXL).

    Returns base64 encoded PNG.
    """
    config = QuoteCardConfig(
        main_text=text,
        subtitle=subtitle,
        show_footer=show_footer,
    )
    builder = QuoteCardBuilder()
    return builder.build_from_ai_background(ai_image_base64, config)

