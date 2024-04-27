import streamlit as st
from .constants import Constants


def get_image_code_ui(path_to_image: str, code: str, language: str = "python") -> None:
    with st.container(border=True):
        st.image(path_to_image, use_column_width=True)
        st.expander(label="💻 See source code").code(
            body=Constants.CODE_HEADER + code if language == "python" else code,
            language=language,
            line_numbers=True,
        )
