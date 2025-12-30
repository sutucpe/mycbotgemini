import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

# --- LANGCHAIN ---
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

# --- ML ---
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline

# ==============================================================================
# CONFIG
# ==============================================================================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CONFIDENCE_THRESHOLD = 0.70

st.set_page_config(page_title="Accutane AI Assistant", layout="wide")
st.title("Accutane (Isotretinoin) Expert Assistant")

if GOOGLE_API_KEY == "AIzaSyD_BURAYA_KENDI_ANAHTARINI_YAZ":
    st.error("Please provide your own Google API key in the GOOGLE_API_KEY variable.")
    st.stop()

# ==============================================================================
# 1. INTENT CLASSIFIER
# ==============================================================================
@st.cache_resource
def train_intent_classifier():
    file_path = "training.csv"

    if not os.path.exists(file_path):
        st.error("training.csv file not found.")
        return None

    df = pd.read_csv(file_path)

    if not {"text", "label"}.issubset(df.columns):
        st.error("The CSV file must contain 'text' and 'label' columns.")
        return None

    model = make_pipeline(
        TfidfVectorizer(),
        SVC(kernel="linear", probability=True)
    )

    model.fit(df["text"].astype(str), df["label"])
    return model

# ==============================================================================
# 2. VECTORSTORE (RAG)
# ==============================================================================
@st.cache_resource
def initialize_vectorstore():
    file_path = "accutane.pdf"

    if not os.path.exists(file_path):
        st.error("accutane.pdf file not found.")
        return None

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(pages)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GOOGLE_API_KEY
    )

    return Chroma.from_documents(docs, embeddings)

# ==============================================================================
# 3. INITIALIZATION
# ==============================================================================
with st.spinner("Initializing system..."):
    intent_model = train_intent_classifier()
    vectorstore = initialize_vectorstore()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY
)

# ==============================================================================
# 4. SESSION STATE
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================================================================
# 5. MAIN LOOP
# ==============================================================================
if query := st.chat_input("Type your question here..."):

    # --- USER MESSAGE ---
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):

            final_answer = ""
            predicted_intent = "unknown"
            confidence = 0.0

            # ==============================================================
            # A) INTENT PREDICTION + CONFIDENCE
            # ==============================================================
            if intent_model:
                try:
                    probs = intent_model.predict_proba([query])[0]
                    classes = intent_model.classes_

                    idx = probs.argmax()
                    confidence = float(probs[idx])
                    predicted_intent = classes[idx]

                except Exception:
                    predicted_intent = "unknown"
                    confidence = 0.0

            # Debug (optional)
            st.caption(
                f"Detected intent: `{predicted_intent}` | Confidence: `{confidence:.2f}`"
            )

            # Low confidence → force RAG fallback
            if confidence < CONFIDENCE_THRESHOLD:
                predicted_intent = "unknown"

            # ==============================================================
            # B) ROUTING LOGIC
            # ==============================================================
            if predicted_intent == "bot_identity_and_disclaimer":
                final_answer = (
                    "I am an AI assistant specialized in the Accutane (Isotretinoin) patient information leaflet. "
                    "I am not a medical professional. All information is for educational purposes only."
                )

            elif predicted_intent == "unrelated":
                final_answer = (
                    "This question does not appear to be related to Accutane. "
                    "I can only assist with questions about this medication and its official leaflet."
                )

            elif predicted_intent in ["greeting", "goodbye"]:
                if predicted_intent == "greeting":
                    final_answer = (
                        "Hello! Feel free to ask any questions about Accutane treatment."
                    )
                else:
                    final_answer = (
                        "Alright. Take care! You may continue asking questions if you like."
                    )

            # ==============================================================
            # C) RAG (DEFAULT PATH)
            # ==============================================================
            else:
                if vectorstore is None:
                    final_answer = "The document could not be processed, so I cannot answer this question."
                else:
                    retriever = vectorstore.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 10}
                    )

                    system_prompt = (
                        "You are an AI assistant specialized in Accutane.\n"
                        "You must ONLY use the retrieved context to answer.\n"
                        "If the answer is not found in the context, explicitly say so.\n"
                        "Keep the answer concise (maximum 4 sentences).\n\n"
                        "{context}"
                    )

                    prompt = ChatPromptTemplate.from_messages([
                        ("system", system_prompt),
                        ("human", "{input}")
                    ])

                    try:
                        chain = create_stuff_documents_chain(llm, prompt)
                        rag_chain = create_retrieval_chain(retriever, chain)
                        response = rag_chain.invoke({"input": query})
                        final_answer = response.get(
                            "answer",
                            "I could not find a relevant answer in the document."
                        )
                    except Exception as e:
                        final_answer = f"An error occurred during retrieval: {e}"

            # ==============================================================
            # OUTPUT
            # ==============================================================
            st.markdown(final_answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": final_answer}
            )

