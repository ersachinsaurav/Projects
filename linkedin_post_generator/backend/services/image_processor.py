"""
Image Processor
================
Post-processing for generated images:
- Branded footer overlay with social icons
- PDF merge for multiple images
"""

import base64
import io
from typing import Optional

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Spacer, PageBreak

from ..utils.constants import SOCIAL_BRANDING

# More subtle footer - lower opacity for better blend
DEFAULT_FOOTER_OPACITY = 0.55


class ImageProcessor:
    """Process generated images with branded footer and PDF merge."""

    def __init__(
        self,
        footer_opacity: float = DEFAULT_FOOTER_OPACITY,
    ):
        """Initialize with footer configuration."""
        self.footer_opacity = footer_opacity
        self.branding = SOCIAL_BRANDING

    def _get_font(self, size: int, bold: bool = False):
        """Get appropriate font, with macOS/Linux fallbacks."""
        font_paths = [
            # macOS fonts
            "/System/Library/Fonts/SFNSText.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            # Linux fonts
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]

        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue

        # Fallback to default
        return ImageFont.load_default()

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

        # Draw 'in' text inside
        font_size = int(size * 0.55)
        font = self._get_font(font_size, bold=True)
        draw.text(
            (x + size // 2, y + size // 2),
            "in",
            font=font,
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


    def add_footer(
        self,
        image_base64: str,
        custom_branding: Optional[dict] = None,
    ) -> str:
        """
        Add branded footer overlay to image.

        Footer format:
        [LinkedIn] [Instagram]  @ersachinsaurav
        [Globe] sachinsaurav.dev

        Args:
            image_base64: Base64 encoded image
            custom_branding: Optional custom branding dict

        Returns:
            Base64 encoded image with branded footer
        """
        branding = custom_branding or self.branding

        # Decode image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))

        # Convert to RGBA if needed
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        width, height = image.size

        # Footer dimensions - 8% of image height
        footer_height = int(height * 0.08)
        footer_y = height - footer_height

        # Create overlay
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Calculate max alpha (more subtle)
        max_alpha = int(255 * self.footer_opacity)

        # Create smooth gradient from transparent to semi-transparent
        # Gradient zone starts above the footer area for seamless blend
        gradient_zone = int(height * 0.06)  # 6% gradient above footer

        # Draw gradient zone (transparent to semi-transparent)
        for i in range(gradient_zone):
            y_pos = footer_y - gradient_zone + i
            if y_pos >= 0:
                # Ease-in curve for smoother transition
                progress = i / gradient_zone
                alpha = int(max_alpha * 0.4 * (progress ** 2))
                draw.rectangle(
                    [(0, y_pos), (width, y_pos + 1)],
                    fill=(0, 0, 0, alpha),
                )

        # Footer area with gradient (semi-transparent, not solid)
        for i in range(footer_height):
            y_pos = footer_y + i
            # Start at 40% opacity and go to 70% at bottom
            progress = i / footer_height
            alpha = int(max_alpha * (0.4 + 0.3 * progress))
            draw.rectangle(
                [(0, y_pos), (width, y_pos + 1)],
                fill=(0, 0, 0, alpha),
            )

        # Icon and text configuration
        icon_size = int(footer_height * 0.45)
        font_size = int(footer_height * 0.36)
        small_font_size = int(footer_height * 0.32)

        # Consistent white color for all elements (slightly transparent for elegance)
        icon_color = (255, 255, 255, 220)
        text_color = (255, 255, 255, 220)

        # Use bolder font for better visibility
        bold_font = self._get_font(font_size, bold=True)
        small_bold_font = self._get_font(small_font_size, bold=True)

        # Single line layout for compact footer
        line_y = footer_y + (footer_height - icon_size) // 2

        # Get branding info
        handle_text = branding.get("handle", "@ersachinsaurav")
        website_text = branding.get("website", "sachinsaurav.dev")

        # Single-line compact layout with drawn icons:
        # [LinkedIn] [Instagram]  @ersachinsaurav  •  [Globe] sachinsaurav.dev

        # Calculate text widths for centering
        handle_bbox = draw.textbbox((0, 0), handle_text, font=bold_font)
        handle_width = handle_bbox[2] - handle_bbox[0]

        website_bbox = draw.textbbox((0, 0), website_text, font=small_bold_font)
        website_width = website_bbox[2] - website_bbox[0]

        separator = "  •  "
        sep_bbox = draw.textbbox((0, 0), separator, font=small_bold_font)
        sep_width = sep_bbox[2] - sep_bbox[0]

        # Total width: icons + gaps + handle + separator + globe + website
        gap = int(icon_size * 0.3)
        total_width = (
            icon_size + gap +          # LinkedIn icon + gap
            icon_size + gap * 2 +      # Instagram icon + larger gap
            handle_width +             # Handle text
            sep_width +                # Separator
            icon_size + gap +          # Globe icon + gap
            website_width              # Website text
        )

        start_x = (width - total_width) // 2
        current_x = start_x
        text_y = footer_y + footer_height // 2

        # Draw LinkedIn icon (outline style)
        self._draw_linkedin_icon(draw, current_x, line_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw Instagram icon (outline style)
        self._draw_instagram_icon(draw, current_x, line_y, icon_size, icon_color)
        current_x += icon_size + gap * 2

        # Draw handle text (bold)
        draw.text(
            (current_x, text_y),
            handle_text,
            font=bold_font,
            fill=text_color,
            anchor="lm",
        )
        current_x += handle_width

        # Draw separator (dimmer)
        draw.text(
            (current_x, text_y),
            separator,
            font=small_bold_font,
            fill=(255, 255, 255, 150),
            anchor="lm",
        )
        current_x += sep_width

        # Draw globe icon (outline style)
        self._draw_globe_icon(draw, current_x, line_y, icon_size, icon_color)
        current_x += icon_size + gap

        # Draw website text (bold)
        draw.text(
            (current_x, text_y),
            website_text,
            font=small_bold_font,
            fill=text_color,
            anchor="lm",
        )

        # Composite images
        result = Image.alpha_composite(image, overlay)

        # Convert back to RGB for PNG
        result = result.convert("RGB")

        # Encode back to base64
        buffer = io.BytesIO()
        result.save(buffer, format="PNG", optimize=True)
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode("utf-8")

    def merge_to_pdf(
        self,
        images_base64: list[str],
        title: Optional[str] = None,
    ) -> str:
        """
        Merge multiple images into a single PDF.

        Args:
            images_base64: List of base64 encoded images
            title: Optional title for the PDF

        Returns:
            Base64 encoded PDF
        """
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )

        story = []

        # Calculate image dimensions
        page_width = letter[0] - inch  # Account for margins
        page_height = letter[1] - inch

        for idx, img_b64 in enumerate(images_base64):
            # Decode image
            img_data = base64.b64decode(img_b64)
            img_buffer = io.BytesIO(img_data)

            # Open with PIL to get dimensions
            pil_img = Image.open(img_buffer)
            img_width, img_height = pil_img.size

            # Calculate scaled dimensions to fit page
            aspect = img_width / img_height

            if aspect > (page_width / (page_height * 0.9)):
                # Width constrained
                display_width = page_width
                display_height = display_width / aspect
            else:
                # Height constrained
                display_height = page_height * 0.85
                display_width = display_height * aspect

            # Reset buffer for ReportLab
            img_buffer.seek(0)

            # Add image to story
            rl_image = RLImage(img_buffer, width=display_width, height=display_height)
            story.append(rl_image)
            story.append(Spacer(1, 0.25 * inch))

            # Page break between images (except last)
            if idx < len(images_base64) - 1:
                story.append(PageBreak())

        # Build PDF
        doc.build(story)
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode("utf-8")

    def process_images(
        self,
        images: list[dict],
        add_footer: bool = True,
        create_pdf: bool = True,
    ) -> dict:
        """
        Process a batch of generated images.

        Args:
            images: List of image dicts with 'base64_data' key
            add_footer: Whether to add branded footer to images
            create_pdf: Whether to create PDF if multiple images

        Returns:
            Dict with processed images and optional PDF
        """
        processed_images = []

        for img in images:
            img_data = img.get("base64_data", "")

            if add_footer and img_data:
                img_data = self.add_footer(img_data)

            processed_images.append({
                **img,
                "base64_data": img_data,
            })

        result = {"images": processed_images}

        # Create PDF if multiple images
        if create_pdf and len(processed_images) > 1:
            pdf_images = [img["base64_data"] for img in processed_images if img["base64_data"]]
            if pdf_images:
                result["pdf_base64"] = self.merge_to_pdf(pdf_images)

        return result
