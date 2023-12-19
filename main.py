import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from io import BytesIO
from PIL import Image
import pytesseract
import pypdfium2 as pdfium
import time

# Set the Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def convert_pdf_to_images_and_ocr(pdf_docs, scale=300/72):
    text = ""   
    list_final_images = []

    for pdf_doc in pdf_docs:
        pdf_file = pdfium.PdfDocument(pdf_doc)
        page_indices = range(len(pdf_file))

        for i, page_number in enumerate(page_indices):
            pdf_page = pdf_file[page_number]
            pixmap = pdf_page.render(scale=scale)

            # Convert PdfBitmap to PIL image
            image = pixmap.to_pil()

            # Perform OCR using pytesseract
            extracted_text = pytesseract.image_to_string(image)

            # Append the extracted text
            text += extracted_text

            # Convert the image to bytes
            image_byte_array = BytesIO()
            image.save(image_byte_array, format='JPEG', quality=95)
            image_byte_array = image_byte_array.getvalue()
            list_final_images.append(dict({i: image_byte_array}))

    # Get text chunks
    chunks = get_text_chunks(text)

    return list_final_images, text, chunks


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks, openai_api_key):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore, openai_api_key):
    llm = ChatOpenAI(openai_api_key=openai_api_key)
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
                
def main():
        load_dotenv()
        st.set_page_config(page_title="S7 PDF Convo.AI", page_icon=":paper:", layout="wide")
        st.write(css, unsafe_allow_html=True)
        
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
          st.session_state.chat_history = None
          
        st.markdown("<h4 style='text-align: center; color: grey;'><i>A Place where you can Interact with your PDFs'</i> 🔮</h4>", unsafe_allow_html=True)
        st.markdown("<h1 style = 'text-align: center; color :black;'>S7 PDF Convo.AI 💬</h1>",unsafe_allow_html=True)
         # Smaller text below the title
        
        user_question = st.text_input("Ask a question about your documents:📢",value="", help="Type your question here", key="user_question", placeholder="Type here...")
        if user_question:
            handle_userinput(user_question)

        with st.sidebar:
            # Company logo image at the top of the sidebar
            company_logo = Image.open("C:\\VS Code\\PDF Chat Bot\\Spectrum 7 logo.png")
            st.image(company_logo, caption='Spectrum 7', use_column_width=True)

            st.markdown("---")  # Add a horizontal line for separation

            st.subheader("Your Folder 📂")
            pdf_docs = st.file_uploader("Upload your files here to chat with them ", accept_multiple_files=True)
            if st.button("**Upload 📤**"):
                st.markdown(
                    '<style>.stButton button { background-color: #007bff;  border-radius: 5px; padding: 0.5rem 1rem; margin-top: 1rem; }</style>',
                    unsafe_allow_html=True
                )
                with st.spinner("Uploading..."):
                    pdf_images, text, chunks = convert_pdf_to_images_and_ocr(pdf_docs)
                    vectorstore = get_vectorstore(chunks, openai_api_key="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")
                    st.session_state.conversation = get_conversation_chain(vectorstore, openai_api_key="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")

                # Display images
                for index, image_bytes in enumerate(pdf_images):
                    image = Image.open(BytesIO(list(image_bytes.values())[0]))
                    st.image(image, caption=f"Page Number {index+1}")

if __name__ == "__main__":
    main()
