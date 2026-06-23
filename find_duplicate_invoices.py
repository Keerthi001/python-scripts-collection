import os
import shutil
from collections import defaultdict
import re
from pathlib import Path

# ================== CONFIGURE THESE ==================
input_folder = r"C:\Users\KEERTHI K\Desktop\All Amazon Gift Card Invoices - 2025\All_90_Invoices"   # Change this
output_unique = r"C:\Users\KEERTHI K\Desktop\All Amazon Gift Card Invoices - 2025\Unique"
output_duplicates = r"C:\Users\KEERTHI K\Desktop\All Amazon Gift Card Invoices - 2025\Duplicates"
# ====================================================

os.makedirs(output_unique, exist_ok=True)
os.makedirs(output_duplicates, exist_ok=True)

def extract_order_number(pdf_path):
    """Extract Order Number from Amazon invoice PDF"""
    try:
        import fitz  # PyMuPDF - best for this
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        # Look for order number pattern: XXX-XXXXXXX-XXXXXXX
        match = re.search(r'(\d{3}-\d{7}-\d{7})', text)
        if match:
            return match.group(1)
        
        # Alternative patterns
        match = re.search(r'Order number[:\s]*(\d{3}-\d{7}-\d{7})', text, re.IGNORECASE)
        if match:
            return match.group(1)
            
    except:
        pass
    
    # Fallback: Try with pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    match = re.search(r'(\d{3}-\d{7}-\d{7})', text)
                    if match:
                        return match.group(1)
    except:
        pass

    return None

# Process all PDFs
order_to_files = defaultdict(list)

print("Scanning PDFs and extracting Order Numbers...\n")

for filename in os.listdir(input_folder):
    if filename.lower().endswith('.pdf'):
        filepath = os.path.join(input_folder, filename)
        order_num = extract_order_number(filepath)
        
        if order_num:
            order_to_files[order_num].append((filename, filepath))
            print(f"✅ {filename:<35} → Order: {order_num}")
        else:
            print(f"⚠️  {filename:<35} → Could not extract order number")

print(f"\nFound {len(order_to_files)} unique order numbers.\n")

# Separate files
duplicate_count = 0

for order_num, files in order_to_files.items():
    if len(files) == 1:
        # Unique
        filename, filepath = files[0]
        shutil.copy2(filepath, os.path.join(output_unique, filename))
    else:
        # Duplicates
        duplicate_count += 1
        for i, (filename, filepath) in enumerate(files):
            new_name = f"{order_num}_{i+1}.pdf" if i > 0 else filename
            shutil.copy2(filepath, os.path.join(output_duplicates, new_name))

print(f"✅ Process completed!")
print(f"   • Unique invoices     : {len([f for f in order_to_files.values() if len(f)==1])}")
print(f"   • Orders with duplicates : {duplicate_count}")
print(f"\nFiles saved in:")
print(f"   → Unique folder: {output_unique}")
print(f"   → Duplicates folder: {output_duplicates}")