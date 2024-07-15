from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

import os

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate

from langchain_community.llms import CTransformers
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

import tempfile
import wget

app = FastAPI()

model_file = 'vinallama-2.7b-chat_q5_0.gguf'
if not os.path.isfile(model_file):
    url = 'https://huggingface.co/vilm/vinallama-2.7b-chat-GGUF/resolve/main/vinallama-2.7b-chat_q5_0.gguf?download=true'
    wget.download(url, 'vinallama-2.7b-chat_q5_0.gguf')


def load_llm(model_file):
    return CTransformers(
        model=model_file,
        model_type="llama",
        max_new_tokens=1024,
        temperature=0.01
    )

def create_prompt(template):
    return PromptTemplate(template=template, input_variables=["context", "question"])

def create_qa_chain(prompt, llm, db):
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}, max_tokens_limit=1024),
        return_source_documents=False,
        chain_type_kwargs={'prompt': prompt}
    )

template = """<|im_start|>system\nSử dụng thông tin sau đây để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói không biết, đừng cố tạo ra câu trả lời\n
    {context}<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant"""

llm = load_llm(model_file)
prompt = create_prompt(template)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(content={"error": "Invalid file type. Please upload a PDF file."}, status_code=400)

    with tempfile.TemporaryDirectory() as tmpdir:
        file_location = os.path.join(tmpdir, file.filename)
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        loader = PyPDFLoader(file_location)
        document = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
        document_split = text_splitter.split_documents(document)

        embeddings = GPT4AllEmbeddings(
            model_name="nomic-embed-text-v1.f16.gguf",
            gpt4all_kwargs={'allow_download': 'True'}
        )

        docsearch = FAISS.from_documents(document_split, embeddings)
        llm_chain = create_qa_chain(prompt, llm, docsearch)

        # Store the QA chain in the session
        app.state.llm_chain = llm_chain

    return {"message": f"Processing `{file.filename}` done. You can now ask questions!"}

@app.post("/ask")
async def ask_question(question: str):
    llm_chain = app.state.llm_chain
    if not llm_chain:
        return JSONResponse(content={"error": "No document has been processed yet. Please upload a document first."}, status_code=400)

    res = llm_chain.invoke({"query": question})
    answer = str(res['result']).split('<|')[0]
    return {"answer": answer}
