import streamlit as st

from text_diff_visualize import TextLineVisualize


def on_clear_clicked():
    st.session_state.text1 = ""
    st.session_state.text2 = ""


def on_rm_whitespace_clicked():
    # split by newline
    text1 = st.session_state.text1.split('\n')
    text2 = st.session_state.text2.split('\n')

    # remove whitespace
    text1 = [line.strip() for line in text1]
    text2 = [line.strip() for line in text2]

    # join by newline
    st.session_state.text1 = '\n'.join(text1)
    st.session_state.text2 = '\n'.join(text2)


def on_uppercase_clicked():
    st.session_state.text1 = st.session_state.text1.upper()
    st.session_state.text2 = st.session_state.text2.upper()


def on_lowercase_clicked():
    st.session_state.text1 = st.session_state.text1.lower()
    st.session_state.text2 = st.session_state.text2.lower()


def main():
    # create 2 text input boxes
    st.set_page_config(layout="wide")

    st.title("Text Diff Visualize")
    st.markdown("<hr />", unsafe_allow_html=True)

    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns([1, 1, 1, 1])
    with btn_col1:
        btn_clear = st.button("Clear", on_click=on_clear_clicked)
    with btn_col2:
        btn_rm_whitespace = st.button(
            "Remove Whitespace", on_click=on_rm_whitespace_clicked
        )
    with btn_col3:
        btn_uppercase = st.button("Uppercase", on_click=on_uppercase_clicked)

    with btn_col4:
        btn_lowercase = st.button("Lowercase", on_click=on_lowercase_clicked)

    btn_run = st.button("Visualize")

    col1, col2 = st.columns(2)
    with col1:
        text1 = st.text_area(
            label="Text 1",
            key="text1",
        )
    with col2:
        text2 = st.text_area(
            label="Text 2",
            key="text2",
        )

    if btn_run:
        visual_line = TextLineVisualize(
            highlight_color_left='rgba(255, 0, 0, 0.6)',
            highlight_color_right='rgba(0, 255, 0, 0.6)',
            split_char='\n',
            empty_char='&nbsp;',
        )

        ### Visualize with streamlit
        # Convert dataframe to markdown table and render on streamlit
        rs_df = visual_line.run_single(text1, text2)

        markdown_table = rs_df.to_markdown(index=False)

        # NOTE: the text must have no tab character
        css = """
<style>

table {
    width: 100%;
    border-collapse: collapse;
}

table th:first-of-type {
    width: 10%;
}
table th:nth-of-type(2) {
    width: 40%;
}
table th:nth-of-type(3) {
    width: 10%;
}
table th:nth-of-type(4) {
    width: 40%;
}
</style>
"""
        css_table = f'''
{css}

{markdown_table}
        '''
        st.markdown(css_table, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
