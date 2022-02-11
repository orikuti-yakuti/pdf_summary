import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextContainer
from app import pdf
from app import pdf_write
#from app.t5 import inference


from reportlab.platypus import BaseDocTemplate, PageTemplate
from reportlab.platypus import Paragraph, PageBreak, FrameBreak
from reportlab.platypus.flowables import Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import cidfonts
from reportlab.platypus.frames import Frame

#UPLOAD_FOLDER = '/tmp'
UPLOAD_FOLDER = './app/static/pdfs'
#ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'randomstringyoulike'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#pdfの保存先
PDF_DIR = "/static/"
BASE_DIR = os.path.dirname(__file__)
PDF_PATH = BASE_DIR + PDF_DIR

#保存先のパスがなければ作成
if not os.path.isdir(PDF_PATH):
    os.mkdir(PDF_PATH)

#@app.route('/uploads/<filename>')
@app.route('/summary/<filename>')
def uploaded_file(filename):
    #if request.methods == 'POST':
    #    if request.form.get('filename'):
            
    pdf_name = filename
    filename = pdf.pdf_to_txt(filename)
    summary = pdf.summary(filename)
    #print(summary)
    summary = pdf.new_line(summary)
    #print(summary)
    #要約した文書をPDFに書き込む
    pdfmetrics.registerFont(cidfonts.UnicodeCIDFont("HeiseiMin-W3"))
    buf = "./app/static/write/summary.pdf"
    
    doc = BaseDocTemplate(buf, title="要約結果",pagesize=(210*mm, 297*mm),)
    
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
    bundle_list = summary.splitlines()
    
    for sentence in bundle_list:
        para = Paragraph(sentence, style)
        flowables.append(para)
    doc.multiBuild(flowables)
    pdf_write = doc.multiBuild(flowables)
    return render_template('pdf.html', pdf_name=pdf_name ,filename=filename, summary = summary, pdf_write = pdf_write)
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

""" @app.route('/abstract/<filename>')
def abstract_file(filename):
    pdf_name = filename
    filename = pdf.pdf_to_txt(filename)
    summary = inference.abstract(filename)
    return render_template('abstract.html', summary=summary) """



@app.route('/', methods=['POST'])
def upload_file():
    # file パートがない場合はアップロード画面にリダイレクト
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # ファイルが選択されていない場合はアップロード画面にリダイレクト
    if not file.filename:
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename))
"""     if file and allowed_file(file.filename) and request.form.get('abstract'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
        return redirect(url_for('abstract_file', filename=filename))"""
"""     if file and allowed_file(file.filename):
        # マルチバイトなど XSS の可能性のある文字列を変換
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file', filename=filename)) """

@app.route('/', methods=['GET'])
def upload_file_view():
    return render_template('index.html')