from langchain import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader, UnstructuredPowerPointLoader
import openai
import os

os.environ["OPENAI_API_KEY"] = "Open AI API KEYが入ります"

# 例：loader = UnstructuredPowerPointLoader("AI勉強会_8月.pptx")
loader = UnstructuredPowerPointLoader('パワポの資料が入ります')
documents = loader.load()

# print(data)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()

# embeddingができたか確認
# print(embeddings.embed_query(texts[0].page_content))

vectordb = Chroma.from_documents(texts, embeddings)
# print(vectordb)
retriever = vectordb.as_retriever()

qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name="gpt-3.5-turbo"), chain_type="stuff", retriever=retriever)




template = """
あなたは親切なアシスタントです。下記の質問に日本語で回答してください。
質問：{question}
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=template,
)

question = "要約をしてください。"

query = prompt.format(question=question)

docs = retriever.get_relevant_documents(question)

# print(docs[0].page_content)

result = qa.run(query)

print("---------", query, "---------")
print("The Answer is:", result)

# import gradio as gr

