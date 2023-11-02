# from llama_index.readers.file.slides_reader import PptxReader
# from pptx import Presentation 
from llama_index import download_loader
import openai
import os

openai.api_key = "Open AI API KEYが入ります"

# parser = PptxReader()
# result = parser.load_data(file="AI勉強会_8月.pptx")

# result = Presentation("AI勉強会_8月.pptx")

# parser = PptxReader()
# parser.init_parser()
# result = parser.parse_file("AI勉強会_8月.pptx")

PptxReader = download_loader("PptxReader")
loader = PptxReader()
result = loader.load_data(file="パワポの資料が入ります")

content = """
あなたは親切なアシスタントです。質問に日本語で回答してください。 
質問：下記のパワポ資料から発表原稿を作成してください。 

# パワポ資料
"""

completion = openai.ChatCompletion.create(
  model="gpt-4", 
  messages=[
    {"role": "user", "content": content + result[0].text}
  ]
)

print("The Question Is:", content + result[0].text)
print("The Answer Is:", completion.choices[0].message.content.encode("unicode-escape").decode("unicode-escape"))
