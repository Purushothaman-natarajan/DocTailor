"""
PDF Processor for DocTailor
Handles conversion of documents to PDF format.
"""

from typing import Optional
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class PDFProcessor:
    """Processes documents into PDF format."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Register a default font if needed
        # pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    
    def process(self, content: str, output_path: str, options: Optional[dict] = None) -> bool:
        """
        Convert markdown-like content to PDF.
        
        Args:
            content: The document content (simple markdown-like format)
            output_path: Path where the PDF should be saved
            options: Optional dictionary of processing options
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create the PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build the story (content)
            story = []
            
            # Process content line by line (simple markdown-like parsing)
            lines = content.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Skip empty lines
                if not line:
                    i += 1
                    continue
                
                # Handle headers
                if line.startswith('# '):
                    story.append(Paragraph(line[2:], self.styles['Title']))
                    story.append(Spacer(1, 12))
                elif line.startswith('## '):
                    story.append(Paragraph(line[3:], self.styles['Heading1']))
                    story.append(Spacer(1, 12))
                elif line.startswith('### '):
                    story.append(Paragraph(line[4:], self.styles['Heading2']))
                    story.append(Spacer(1, 12))
                # Handle bullet points
                elif line.startswith('- '):
                    story.append(Paragraph('• ' + line[2:], self.styles['Normal']))
                    story.append(Spacer(1, 6))
                # Handle numbered lists
                elif line[0].isdigit() and '. ' in line:
                    story.append(Paragraph(line, self.styles['Normal']))
                    story.append(Spacer(1, 6))
                # Handle horizontal rules
                elif line.startswith('---') or line.startswith('***'):
                    story.append(Spacer(1, 12))
                    story.append(Paragraph('_' * 50, self.styles['Normal']))
                    story.append(Spacer(1, 12))
                # Regular paragraph
                else:
                    story.append(Paragraph(line, self.styles['Normal']))
                    story.append(Spacer(1, 6))
                
                i += 1
            
            # Build the PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def can_process(self, format_name: str) -> bool:
        """Check if this processor can handle the given format."""
        return format_name.lower() in ['pdf']
