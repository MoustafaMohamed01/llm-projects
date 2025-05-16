import streamlit as st
import requests
import json

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2"

def generate_content(prompt):
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API, headers=HEADERS, data=json.dumps(data))
        response.raise_for_status()
        response_json = response.json()
        if 'choices' in response_json and len(response_json['choices']) > 0 and 'message' in response_json['choices'][0] and 'content' in response_json['choices'][0]['message']:
            return response_json['choices'][0]['message']['content']
        elif 'message' in response_json and 'content' in response_json['message']:
            return response_json['message']['content']
        else:
            return f"Error: Unexpected Ollama response format - {response_json}"
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {e}"
    except json.JSONDecodeError as e:
        return f"Error decoding JSON response from Ollama: {e}"

def main():
    st.set_page_config(page_title='SQL Query Generator')
    st.markdown(
        """
        <div style='text-align: center;'>
            <h1>SQL Query Generator</h1>
            <h3>I can generate SQL queries for you!</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    text_input = st.text_area('Enter your Query description here...')
    database_context = st.text_area('Optional: Provide database schema or context (e.g., table names, columns)...')
    dialect = st.selectbox('Optional: Specify SQL dialect', ['Generic SQL', 'PostgreSQL', 'MySQL', 'SQLite'])

    submit = st.button('Generate SQL Query')

    if submit:
        if not text_input:
            st.warning("Please enter a query description.")
            return

        with st.spinner('Generating SQL Query...'):
            try:
                template = f"""
                    Create a SQL query snippet based on the following description:
                    ```
                    {text_input}
                    ```
                    {'considering the following database context: ' + database_context if database_context else ''}
                    {'Ensure the query is compatible with ' + dialect + '.' if dialect != 'Generic SQL' else ''}
                    I just want the SQL query.
                    """
                formatted_template = template.format(text_input=text_input)
                sql_query = generate_content(formatted_template)
                if sql_query.startswith("Error"):
                    raise Exception(sql_query)
                sql_query = sql_query.strip().lstrip('```sql').rstrip('```')

                expected_output_prompt = f"""
                    What would be the expected response of this SQL Query snippet:
                    ```sql
                    {sql_query}
                    ```
                    Provide a sample tabular response formatted as a Markdown table, with no additional explanation.
                    """
                output = generate_content(expected_output_prompt)
                if output.startswith("Error"):
                    raise Exception(output)

                explanation_prompt = f"""
                    Explain this SQL Query:
                    ```sql
                    {sql_query}
                    ```
                    Please provide a concise explanation.
                    """
                explanation = generate_content(explanation_prompt)
                if explanation.startswith("Error"):
                    raise Exception(explanation)

                with st.container():
                    st.success('SQL Query Generated Successfully! Here is your Query Below:')
                    st.code(sql_query, language='sql')

                    st.success('Expected Output of this SQL Query will be:')
                    st.markdown(f"```\n{output}\n```")

                    st.success('Explanation of this SQL Query:')
                    st.markdown(explanation)

            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

