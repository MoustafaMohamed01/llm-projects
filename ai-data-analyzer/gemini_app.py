import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
import os
from utils import get_model_response

def main():
    st.title('📊 Chat with AI Data Analyzer')

    uploaded_file = st.file_uploader('Choose a CSV file:', type='csv')

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        try:
            loader = CSVLoader(file_path=tmp_file_path, encoding='utf-8', csv_args={'delimiter': ','})
            data = loader.load()

            user_input = st.text_input('Ask a question about the data:')

            if user_input:
                st.info("Generating response...")
                try:
                    response = get_model_response(data, user_input)
                    st.success("Response:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Model error: {e}")

        except Exception as e:
            st.error(f"CSV loading error: {e}")
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

if __name__ == '__main__':
    main()
