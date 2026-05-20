import html
import json

import streamlit as st
import streamlit.components.v1 as components

from translator import (
    LANGUAGES,
    create_history_item,
    get_source_languages,
    get_target_languages,
    limit_history,
    translate_text,
)


def apply_page_styles():
    """Style the page using Streamlit theme colors for light and dark mode."""
    st.markdown(
        """
        <style>
            .stApp {
                background: var(--background-color);
                color: var(--text-color);
            }

            .block-container {
                max-width: 1040px;
                padding-top: 2rem;
                padding-bottom: 2rem;
            }

            [data-testid="stVerticalBlockBorderWrapper"] {
                background: var(--secondary-background-color);
                border: 1px solid rgba(128, 128, 128, 0.28);
                border-radius: 14px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
                padding: 0.2rem;
            }

            h1, h2, h3, p, label, span {
                color: var(--text-color);
            }

            textarea,
            input,
            [data-baseweb="select"] > div,
            [data-baseweb="textarea"] textarea {
                background-color: var(--background-color);
                color: var(--text-color);
                border-color: rgba(128, 128, 128, 0.35);
            }

            textarea::placeholder,
            input::placeholder {
                color: rgba(128, 128, 128, 0.85);
            }

            .translated-box {
                background: var(--background-color);
                color: var(--text-color);
                border: 1px solid rgba(128, 128, 128, 0.32);
                border-radius: 10px;
                min-height: 120px;
                padding: 1rem;
                line-height: 1.6;
                white-space: pre-wrap;
                overflow-wrap: anywhere;
            }

            .stButton > button,
            button[kind="primary"],
            button[kind="secondary"],
            [data-testid="baseButton-primary"],
            [data-testid="baseButton-secondary"] {
                background-color: #2563EB;
                color: #ffffff;
                border: 1px solid #2563EB;
                border-radius: 10px;
                font-weight: 600;
            }

            .stButton > button:hover,
            button[kind="primary"]:hover,
            button[kind="secondary"]:hover,
            [data-testid="baseButton-primary"]:hover,
            [data-testid="baseButton-secondary"]:hover {
                background-color: #1D4ED8;
                border-color: #1D4ED8;
                color: #ffffff;
            }

            .stButton > button:focus,
            button[kind="primary"]:focus,
            button[kind="secondary"]:focus,
            [data-testid="baseButton-primary"]:focus,
            [data-testid="baseButton-secondary"]:focus {
                box-shadow: 0 0 0 0.2rem rgba(37, 99, 235, 0.25);
                color: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Create session values used for output and history."""
    if "translation_history" not in st.session_state:
        st.session_state.translation_history = []

    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""

    if "output_message" not in st.session_state:
        st.session_state.output_message = "Your translated text will appear here."

    if "output_status" not in st.session_state:
        st.session_state.output_status = "info"

    if "target_language_name" not in st.session_state:
        st.session_state.target_language_name = ""


def add_to_history(source_name, target_name, original_text, translated_text):
    """Save the latest translation to the current browser session."""
    history_item = create_history_item(
        source_name,
        target_name,
        original_text,
        translated_text,
    )

    st.session_state.translation_history.insert(0, history_item)
    st.session_state.translation_history = limit_history(
        st.session_state.translation_history
    )


def show_status_message():
    """Display the current output message with the correct Streamlit style."""
    if st.session_state.output_status == "success":
        st.success(st.session_state.output_message)
    elif st.session_state.output_status == "warning":
        st.warning(st.session_state.output_message)
    elif st.session_state.output_status == "error":
        st.error(st.session_state.output_message)
    else:
        st.info(st.session_state.output_message)


def render_copy_button(translated_text):
    """Render a browser-side copy button for the translated text."""
    safe_text = json.dumps(translated_text)

    components.html(
        f"""
        <style>
            body {{
                background: transparent;
                margin: 0;
            }}

            #copyMessage {{
                font-family: sans-serif;
                color: #64748b;
            }}

            @media (prefers-color-scheme: dark) {{
                #copyMessage {{
                    color: #cbd5e1;
                }}
            }}

            #copyButton {{
                background: #2563EB;
                color: #ffffff;
                border: 1px solid #2563EB;
                border-radius: 8px;
                padding: 0.65rem 0.9rem;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
            }}

            #copyButton:hover {{
                background: #1D4ED8;
                border-color: #1D4ED8;
            }}
        </style>
        <button id="copyButton">
            Copy Translated Text
        </button>
        <p id="copyMessage"></p>

        <script>
            const textToCopy = {safe_text};
            const button = document.getElementById("copyButton");
            const message = document.getElementById("copyMessage");

            button.addEventListener("click", async () => {{
                try {{
                    await navigator.clipboard.writeText(textToCopy);
                    message.innerText = "Translated text copied.";
                }} catch (error) {{
                    message.innerText = "Copy failed. Please select the text and copy manually.";
                }}
            }});
        </script>
        """,
        height=95,
    )


def handle_translation(input_text, source_language_name, target_language_name):
    """Validate user input, translate text, and update the output area."""
    clean_text = input_text.strip()

    if not clean_text:
        st.session_state.translated_text = ""
        st.session_state.target_language_name = ""
        st.session_state.output_status = "warning"
        st.session_state.output_message = "Please enter some text before translating."
        return

    if LANGUAGES[source_language_name] == LANGUAGES[target_language_name]:
        st.session_state.translated_text = ""
        st.session_state.target_language_name = ""
        st.session_state.output_status = "warning"
        st.session_state.output_message = (
            "Please choose different source and target languages."
        )
        return

    try:
        with st.spinner("Translating your text..."):
            translated_text = translate_text(
                clean_text,
                source_language_name,
                target_language_name,
            )

        st.session_state.translated_text = translated_text
        st.session_state.target_language_name = target_language_name
        st.session_state.output_status = "success"
        st.session_state.output_message = "Translation completed successfully."

        add_to_history(
            source_language_name,
            target_language_name,
            clean_text,
            translated_text,
        )
    except Exception:
        st.session_state.translated_text = ""
        st.session_state.target_language_name = ""
        st.session_state.output_status = "error"
        st.session_state.output_message = (
            "Translation could not be completed. Please check your internet "
            "connection and try again."
        )


def render_translated_text_box(translated_text, target_language_name):
    """Show one clean output box, using RTL alignment for Arabic text."""
    direction = "rtl" if target_language_name == "Arabic" else "ltr"
    text_align = "right" if target_language_name == "Arabic" else "left"
    safe_text = html.escape(translated_text)

    st.markdown(
        f"""
        <div class="translated-box" dir="{direction}" style="text-align: {text_align};">
            {safe_text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Show the app title and short project description."""
    with st.container(border=True):
        st.title("CodeAlpha Language Translation Tool")
        st.caption("Artificial Intelligence Internship - Task 1")
        st.write(
            "Translate text between common languages using a simple "
            "AI-powered translation tool."
        )


def render_input_section():
    """Show the text input, language dropdowns, and translate button."""
    with st.container(border=True):
        st.header("Input")

        input_text = st.text_area(
            "Enter text",
            height=170,
            placeholder="Type or paste the text you want to translate.",
        )

        col1, col2 = st.columns(2)

        with col1:
            source_language_name = st.selectbox(
                "Source language",
                get_source_languages(),
                index=0,
            )

        with col2:
            target_language_name = st.selectbox(
                "Target language",
                get_target_languages(),
                index=0,
            )

        if st.button("Translate", type="primary", use_container_width=True):
            handle_translation(input_text, source_language_name, target_language_name)


def render_output_section():
    """Show messages, translated text, and the copy button."""
    with st.container(border=True):
        st.header("Output")
        show_status_message()

        if st.session_state.translated_text:
            render_translated_text_box(
                st.session_state.translated_text,
                st.session_state.target_language_name,
            )
            render_copy_button(st.session_state.translated_text)


def render_history_section():
    """Show current-session translation history."""
    with st.container(border=True):
        st.header("Translation History")

        if st.session_state.translation_history:
            if st.button("Clear Translation History", use_container_width=True):
                st.session_state.translation_history = []
                st.rerun()

            for index, item in enumerate(st.session_state.translation_history, start=1):
                with st.expander(
                    f"{index}. {item['source']} -> {item['target']}",
                    expanded=index == 1,
                ):
                    st.markdown("**Original text**")
                    st.write(item["original"])
                    st.markdown("**Translated text**")
                    st.write(item["translated"])
        else:
            st.info("No translations have been saved in this session yet.")


def run_app():
    """Run the Streamlit front end."""
    st.set_page_config(
        page_title="CodeAlpha Language Translation Tool",
        layout="centered",
    )

    apply_page_styles()
    initialize_session_state()
    render_header()
    render_input_section()
    render_output_section()
    render_history_section()
