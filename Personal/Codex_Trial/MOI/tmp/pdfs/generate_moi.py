from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def draw_wrapped_text(c, text, x, y, max_width, font_name="Times-Roman", font_size=12, leading=18):
    c.setFont(font_name, font_size)
    words = text.split()
    lines = []
    current = []

    for word in words:
        candidate = " ".join(current + [word])
        if c.stringWidth(candidate, font_name, font_size) <= max_width:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]

    if current:
        lines.append(" ".join(current))

    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def generate_moi(output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    left = 25 * mm
    right = width - 25 * mm
    y = height - 28 * mm

    c.setTitle("Medium of Instruction Certificate - Subin S")

    c.setFont("Times-Bold", 13)
    c.drawCentredString(width / 2, y, "VIDYA ACADEMY OF SCIENCE & TECHNOLOGY TECHNICAL CAMPUS")
    y -= 6 * mm
    c.setFont("Times-Roman", 11)
    c.drawCentredString(width / 2, y, "Kilimanoor, Thiruvananthapuram, Kerala - 695602")
    y -= 12 * mm

    c.setLineWidth(0.8)
    c.line(left, y, right, y)
    y -= 12 * mm

    c.setFont("Times-Bold", 14)
    c.drawCentredString(width / 2, y, "TO WHOMSOEVER IT MAY CONCERN")
    y -= 12 * mm

    c.setFont("Times-Bold", 13)
    c.drawCentredString(width / 2, y, "MEDIUM OF INSTRUCTION CERTIFICATE")
    y -= 14 * mm

    para_1 = (
        "This is to certify that Mr. Subin S (Registration Number: VAK17EC021) was a bona fide student "
        "of this institution in the B.Tech program in Electronics and Communication Engineering."
    )
    para_2 = (
        "The medium of instruction and examination for the entire four-year course of study was ENGLISH."
    )
    para_3 = (
        "This certificate is being issued on request for higher education and official purposes."
    )

    max_width = right - left
    y = draw_wrapped_text(c, para_1, left, y, max_width)
    y -= 6
    y = draw_wrapped_text(c, para_2, left, y, max_width)
    y -= 6
    y = draw_wrapped_text(c, para_3, left, y, max_width)

    y -= 24
    c.setFont("Times-Roman", 12)
    c.drawString(left, y, "Date: 08 March 2026")

    y -= 18
    c.drawString(left, y, "Place: Kilimanoor")

    sig_y = 42 * mm
    c.setFont("Times-Bold", 12)
    c.drawString(right - 72 * mm, sig_y + 10 * mm, "Authorized Signatory")
    c.setFont("Times-Roman", 11)
    c.drawString(right - 72 * mm, sig_y + 4 * mm, "Vidya Academy of Science & Technology")
    c.drawString(right - 72 * mm, sig_y - 2 * mm, "Technical Campus - Kilimanoor")
    c.line(right - 75 * mm, sig_y + 14 * mm, right, sig_y + 14 * mm)

    c.showPage()
    c.save()


if __name__ == "__main__":
    generate_moi(Path("output/pdf/subin_MOI_certificate.pdf"))
