from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextContainer
import os
import re
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import os.path
import spacy

#pdfの保存先
PDF_DIR = "/static/"
BASE_DIR = os.path.dirname(__file__)
PDF_PATH = BASE_DIR + PDF_DIR
print(PDF_PATH)

#PDFから文字を取り出す。
def pdf_to_txt(filename):
  resourceManager = PDFResourceManager()
  device = PDFPageAggregator(resourceManager, laparams=LAParams())
  pdf_name = PDF_PATH + filename
  #path_pdf = pdf_name
  path_pdf = "./app/static/pdfs/" + filename
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
  # ginzaを使用して、文に自然な区切りをつける。
  nlp = spacy.load('ja_ginza_electra')
  doc = nlp(textbox)
  temp = ''
  for sent in doc.sents:
      temp += sent.text + '\n'
  textbox = temp
  """   doc = nlp(textbox)
  textbox = ''
  for sent in doc.sents:
      textbox += sent.text + '\n'
  textbox = textbox.split('\n') """
  return textbox


def summary(filename):
    document = filename
    
    #print(u'[原文書]')
    #print(document)
    
    # Object of automatic summarization.
    auto_abstractor = AutoAbstractor()
    # Set tokenizer for Japanese.
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # Set delimiter for making a list of sentence.
    auto_abstractor.delimiter_list = ["。", "\n"]
    # Object of abstracting and filtering document.
    abstractable_doc = TopNRankAbstractor()
    # Summarize document.
    result_dict = auto_abstractor.summarize(document, abstractable_doc)

    #print(u'[文書要約結果]')
    # Output result.
    #print(result_dict["summarize_result"])
    result = ''
    for sentence in result_dict["summarize_result"]:
        #print(sentence)
        result += sentence
    return result

def new_line(sentence):
    sentence = sentence.replace('。','。\n　')
    return sentence



""" from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextContainer
import os
import re
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import os.path

#pdfの保存先
PDF_DIR = "/static/"
BASE_DIR = os.path.dirname(__file__)
PDF_PATH = BASE_DIR + PDF_DIR
print(PDF_PATH)

#PDFから文字を取り出し、GINZAで直す。
def pdf_to_txt(filename):
  resourceManager = PDFResourceManager()
  device = PDFPageAggregator(resourceManager, laparams=LAParams())
  pdf_name = PDF_PATH + filename
  #path_pdf = pdf_name
  path_pdf = "./app/static/pdfs/" + filename
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
  # ginzaを使用して、文に自然な区切りをつける。
  import spacy
  nlp = spacy.load('ja_ginza_electra')
  #doc = nlp('''私は「あなたの思いに答えられない。他を当たってほしい。」と言われました！呆然として\nその場にたたずむしかありませんでしたそれでも私は信じたい！''')
  doc = nlp(textbox)
  textbox = ''
  for sent in doc.sents:
      textbox += sent.text + '\n'
  textbox = textbox.split('\n')
  return textbox


def summary(filename):
    document = filename
    
    #print(u'[原文書]')
    #print(document)
    
    # Object of automatic summarization.
    auto_abstractor = AutoAbstractor()
    # Set tokenizer for Japanese.
    auto_abstractor.tokenizable_doc = MeCabTokenizer()
    # Set delimiter for making a list of sentence.
    auto_abstractor.delimiter_list = ["。", "\n"]
    # Object of abstracting and filtering document.
    abstractable_doc = TopNRankAbstractor()
    # Summarize document.
    result_dict = auto_abstractor.summarize(document, abstractable_doc)

    #print(u'[文書要約結果]')
    # Output result.
    #print(result_dict["summarize_result"])
    result = ''
    for sentence in result_dict["summarize_result"]:
        #print(sentence)
        result += sentence
    return result

def new_line(sentence):
    sentence = sentence.replace('。','。\n　')
    return sentence

 """