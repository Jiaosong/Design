#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import subprocess

TEXT='OLEANDER PDF FONT EMBEDDING TEST 2026-08-28'

# A: deliberately unembedded standard font via PostScript + Ghostscript.
ps='''%!PS-Adobe-3.0\n%%Pages: 1\n%%BoundingBox: 0 0 595 842\n/Helvetica findfont 24 scalefont setfont\n72 760 moveto\n(%s) show\nshowpage\n%%EOF\n''' % TEXT
open('fixture.ps','w',encoding='ascii').write(ps)
subprocess.run(['gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=pdfwrite','-dEmbedAllFonts=false','-dSubsetFonts=false','-sOutputFile=A_unembedded.pdf','fixture.ps'],check=True)

# B: explicitly embedded TrueType subset. The Lato path is a TRAINING runtime fixture dependency, not a project font authority.
font_path='/usr/share/fonts/truetype/lato/Lato-Medium.ttf'
pdfmetrics.registerFont(TTFont('LatoMedium',font_path))
c=canvas.Canvas('B_embedded.pdf', pagesize=(595,842), initialFontName='LatoMedium')
c.drawString(72,760,TEXT)
c.save()
