from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextContainer
import os

#PDFから文字を取り出す。
def pdf_to_txt(filename):
  resourceManager = PDFResourceManager()
  device = PDFPageAggregator(resourceManager, laparams=LAParams())
  pdf_name = PDF_PATH + filename
  #path_pdf = pdf_name
  path_pdf = "../static/pdfs/" + filename
  count = 0
  ave_size = 0
  with open(path_pdf, 'rb') as fp:
      interpreter = PDFPageInterpreter(resourceManager, device)
      for page in PDFPage.get_pages(fp):
          interpreter.process_page(page)
          layout = device.get_result()
          for lt in layout:
              # LTTextContainerの場合だけ標準出力
              if isinstance(lt, LTTextContainer):
                  ave_size += lt.height
                  count += 1
  device.close()
  ave_size /= count
  #print("平均縦幅サイズ",ave_size)
  #どのサイズの文字をドロップアウトするか決める。
  dropout_parameter = 1.5
  drop_size = ave_size / dropout_parameter
  #print("ドロップアウトするサイズ",drop_size)
  textbox = ''
  with open(path_pdf, 'rb') as fp:
      interpreter = PDFPageInterpreter(resourceManager, device)
      for page in PDFPage.get_pages(fp):
          interpreter.process_page(page)
          layout = device.get_result()
          for lt in layout:
              # LTTextContainerの場合だけ標準出力
              if isinstance(lt, LTTextContainer):
                  if(lt.height > drop_size):
                      #print('{}, x0={:.2f}, x1={:.2f}, y0={:.2f}, y1={:.2f}, width={:.2f}, height={:.2f}'.format(lt.get_text().strip(), lt.x0, lt.x1, lt.y0, lt.y1, lt.width, lt.height))
                      textbox += lt.get_text()
                      #print( 'lt.get_textのタイプ',type(lt.get_text))
  device.close()
  textbox = textbox.replace('\n','')
  return textbox


