from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.platypus import Paragraph, PageBreak, FrameBreak
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import cidfonts
from reportlab.platypus.frames import Frame

def write(bundle_into_one):
    pdfmetrics.registerFont(cidfonts.UnicodeCIDFont("HeiseiMin-W3"))
    buf = "./app/static/write/summary.pdf"
    
    doc = BaseDocTemplate(buf, title="要約結果",pagesize=(210*mm, 297*mm),)
    
    # 左下右上。左上が０になる?
    frames = [ Frame(10*mm, 10*mm, 190*mm, 277*mm, showBoundary=1),]
    page_template = PageTemplate("frames", frames=frames)
    doc.addPageTemplates(page_template)
    
    style_dict ={
        "name":"nomarl",
        "fontName":"HeiseiMin-W3",
        "fontSize":10,
        "leading":20,
        "firstLineIndent":10,
        }
    style = ParagraphStyle(**style_dict)
    flowables = []
    space = Spacer(10*mm, 10*mm)
    bundle_list = bundle_into_one.splitlines()
    
    #flowables.append(space)
    for sentence in bundle_list:
        para = Paragraph(sentence, style)
        flowables.append(para)
    summary = doc.multiBuild(flowables)
    return summary
