# ============================================================
#  file_handler.py  –  All file reading and writing
# ============================================================
# Functions here:
#   - read_text_file()  : load a .txt file
#   - read_pdf_file()   : load a .pdf file
#   - save_as_txt()     : export summary to .txt
#   - save_as_pdf()     : export summary to .pdf
# ============================================================

from pypdf import PdfReader
from fpdf import FPDF


# ── READING ─────────────────────────────────────────────────

def read_text_file(filepath):
    """
    Read a plain .txt file and return its content as a string.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"[OK] Loaded text file: {filepath}")
        return content
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        return None
    except Exception as e:
        print(f"[ERROR] Could not read file: {e}")
        return None


def read_pdf_file(filepath):
    """
    Read a PDF file and extract all text from every page.
    Uses the pypdf library.
    """
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:          # some pages may be blank
                text += page_text + "\n"
        print(f"[OK] Loaded PDF file: {filepath} ({len(reader.pages)} pages)")
        return text
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        return None
    except Exception as e:
        print(f"[ERROR] Could not read PDF: {e}")
        return None


# ── WRITING ─────────────────────────────────────────────────

def save_as_txt(summary, output_path="summary_output.txt"):
    """
    Save the generated summary to a plain .txt file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=== AI-GENERATED SUMMARY ===\n\n")
            f.write(summary)
            f.write("\n")
        print(f"[OK] Summary saved as TXT: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Could not save TXT: {e}")
        return False


def save_as_pdf(summary, output_path="summary_output.pdf"):
    """
    Save the generated summary to a formatted .pdf file.
    Uses the fpdf2 library.
    """
    try:
        pdf = FPDF()
        pdf.add_page()

        # Title
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(0, 12, "AI-Generated Summary", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(4)

        # Divider line
        pdf.set_draw_color(100, 100, 100)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(6)

        # Summary body
        pdf.set_font("Helvetica", size=12)
        # multi_cell wraps long lines automatically
        pdf.multi_cell(0, 8, summary)

        pdf.output(output_path)
        print(f"[OK] Summary saved as PDF: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Could not save PDF: {e}")
        return False
