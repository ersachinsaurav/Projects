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
import textwrap
from typing import Optional, Literal
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont


@dataclass
class PostCardStyle:
    """Visual style configuration for post cards."""
    # Dimensions (1:1 or 4:5 ratio)
    width: int = 1080
    height: int = 1080

    # Theme
    theme: Literal['dark', 'light'] = 'dark'

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
        return self.dark_bg if self.theme == 'dark' else self.light_bg

    @property
    def text_color(self) -> tuple:
        return self.dark_text if self.theme == 'dark' else self.light_text

    @property
    def secondary_color(self) -> tuple:
        return self.dark_secondary if self.theme == 'dark' else self.light_secondary

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
    ) -> str:
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

        # Use short post if available
        display_text = short_post or post_text

        # Limit text length for readability
        if len(display_text) > 500:
            display_text = display_text[:497] + "..."

        # Calculate dynamic height based on actual content
        text_font = self.fonts.get('regular_text', ImageFont.load_default())
        content_width = s.width - (s.padding * 2)

        # Get actual line height from font
        sample_bbox = text_font.getbbox("Ayg")  # Sample with ascenders and descenders
        actual_line_height = sample_bbox[3] - sample_bbox[1]
        line_height = int(actual_line_height * 1.5)  # 1.5x line spacing

        # Process paragraphs and count actual rendered lines
        paragraphs = display_text.split('\n')
        total_content_height = 0
        paragraph_gap = 20  # Gap between paragraphs

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
        bottom_padding = 40  # Smaller bottom padding

        # Calculate total height
        calculated_height = s.padding + header_height + total_content_height + bottom_padding

        # Ensure minimum height of 350px for very short posts
        calculated_height = max(calculated_height, 350)

        # Create image with calculated height
        image = Image.new('RGB', (s.width, calculated_height), s.bg_color)
        draw = ImageDraw.Draw(image)

        # Calculate layout
        y = s.padding

        # === HEADER: Avatar + Name + Handle + Follow Button ===
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

        # === POST TEXT ===
        # text_font and line_height already defined above
        paragraph_gap = 20  # Same as in height calculation

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

