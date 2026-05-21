import streamlit as st
from utils import summerizer

st.set_page_config(page_title='PDF & Word Document Summarizer')
st.title('PDF & Word Document Summarizer App')
st.write('Summarize your PDF or Word files in just a few seconds...')
st.divider()

doc_file = st.file_uploader('Upload your PDF or Word Document...', type=['pdf', 'docx'])
submit = st.button('Generate Summary')

if submit:
    if doc_file is not None:
        with st.spinner("Generating summary... This might take a moment."):
            response = summerizer(doc_file)

        st.subheader('Summary of file:')
        st.write(response)
    else:
        st.warning("Please upload a PDF or Word document first.")
