try:
    import streamlit as st
    import requests
    import json
except ModuleNotFoundError as e:
    raise ImportError(
        "Required modules are not installed. Ensure Streamlit and Requests are installed."
    ) from e

st.set_page_config(
    page_title="RobotNav Query Interface",
    page_icon="docs/images/logo.png",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """<style>
    .main .block-container {
        background-color: #202124;
        color: white;
    }
    textarea {
        font-family: courier-new;
    }
    </style>""",
    unsafe_allow_html=True,
)

st.image("docs/images/logo.png", width=100)
st.title("RobotNav Query Interface")

st.sidebar.header("Query Configuration")

models = ["cohere", "local_default"]
prompt_formats = [
    "e7_v1_xrif_waypoints_keywords",
    "e7_v1_xrif_waypoints_list_simple",
]

selected_model = st.sidebar.selectbox("Select Model", models)
selected_format = st.sidebar.selectbox("Select Prompt Format", prompt_formats)

prompt = st.text_area(
    "Enter your prompt/query:",
    height=200,
    value='{\n      "query": "Grab a coffee and send it to the outreach classroom" \n}',
)

if st.button("Run Query"):
    if prompt.strip():
        with st.spinner("Querying the model..."):
            try:
                api_url = "http://localhost:8000/v1/text_prompt"
                payload = {
                    "model_name": selected_model,
                    "prompt_format_name": selected_format,
                    "prompt_args": json.loads(prompt),
                    "model_args": {"structured_output": {"type": "json_object"}},
                }
                response = requests.post(api_url, json=payload)
                result = response.json()

                st.subheader("Query Results")
                st.text_area(
                    "Output: ",
                    value=str(result.get("output", result)["response"]["Response"]),
                    height=400,
                    disabled=True,
                )

            except Exception as e:
                st.error(f"Error querying the model: {e}")
    else:
        st.warning("Please enter a prompt before running the query.")

st.sidebar.info("FYDP Team 7 - MSE 2025")
