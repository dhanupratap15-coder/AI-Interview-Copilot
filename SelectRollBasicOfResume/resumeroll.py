
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import TextLoader


while True:
        input_file = input("Enter the Resumme file  : ").strip()
        input_type = input_file.split(".")[-1].lower().strip()
        if input_type == "pdf":
             loader = PyPDFLoader(input_file)
             documents = loader.load()
             resume = "\n".join(doc.page_content for doc in documents)
             break
        elif input_type == "docx":
            loader = Docx2txtLoader(input_file)
            documents = loader.load()
            resume = "\n".join(doc.page_content for doc in documents)
            break
        else:
            print("Unsupported file format")
            print("Please enter a valid file format (pdf, txt, docx).")
       