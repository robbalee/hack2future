#!/usr/bin/env python3
"""
Convert text files in sample_documents directory to PDF format
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def text_to_pdf(text_file_path, pdf_file_path):
    """Convert a text file to PDF"""
    
    # Create PDF document
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    # Create a custom style for monospace text
    mono_style = ParagraphStyle(
        'MonoStyle',
        parent=normal_style,
        fontName='Courier',
        fontSize=10,
        leftIndent=0,
        rightIndent=0,
        spaceAfter=6,
    )
    
    # Read the text file
    with open(text_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into lines and create paragraphs
    story = []
    lines = content.split('\n')
    
    # Add title (first line)
    if lines:
        title = lines[0].strip()
        if title:
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 12))
            lines = lines[1:]  # Remove title from content
    
    # Add content
    for line in lines:
        # Handle empty lines
        if not line.strip():
            story.append(Spacer(1, 6))
        else:
            # Use monospace for structured data, normal for regular text
            if any(char in line for char in [':', '|', 'Policy', 'Case', 'Claim']):
                story.append(Paragraph(line, mono_style))
            else:
                story.append(Paragraph(line, normal_style))
    
    # Build PDF
    doc.build(story)
    print(f"✓ Converted {text_file_path} to {pdf_file_path}")

def main():
    """Convert all text files in sample_documents to PDF"""
    
    sample_docs_dir = "/workspaces/hack2future/sample_documents"
    
    # Check if directory exists
    if not os.path.exists(sample_docs_dir):
        print(f"Directory {sample_docs_dir} does not exist!")
        return
    
    # Get all .txt files
    txt_files = [f for f in os.listdir(sample_docs_dir) if f.endswith('.txt')]
    
    if not txt_files:
        print("No .txt files found in sample_documents directory!")
        return
    
    print(f"Found {len(txt_files)} text files to convert:")
    
    # Convert each file
    for txt_file in txt_files:
        txt_path = os.path.join(sample_docs_dir, txt_file)
        pdf_file = txt_file.replace('.txt', '.pdf')
        pdf_path = os.path.join(sample_docs_dir, pdf_file)
        
        try:
            text_to_pdf(txt_path, pdf_path)
        except Exception as e:
            print(f"✗ Error converting {txt_file}: {e}")
    
    print("\nConversion complete!")
    print(f"PDF files created in: {sample_docs_dir}")

if __name__ == "__main__":
    main()
