import streamlit as st

from text_diff_visualize import TextLineVisualize


def main():
    # create 2 text input boxes
    st.set_page_config(layout="wide")

    st.title("Text Diff Visualize")
    st.markdown("<hr />", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        btn_run = st.button("Visualize")
    # with col2:
    #     btn_clear = st.button("Clear")
    # with col3:
    #     btn_edit = st.button("Edit")

    col1, col2 = st.columns(2)
    with col1:
        text1 = st.text_area(
            "Text 1",
            "Input text 1 here",
        )
    with col2:
        text2 = st.text_area(
            "Text 2",
            "Input text 2 here",
        )

    if btn_run:
        visual_line = TextLineVisualize(
            highlight_color_left='rgba(255, 0, 0, 0.6)',  # Default: 'red' with opacity 0.6
            highlight_color_right='rgba(0, 255, 0, 0.6)',  # Default: 'green' with opacity 0.6
            split_char='\n',  # Default: '\n'
            empty_char='&nbsp;',  # Default: '#'
        )

        ### Visualize with streamlit
        # Convert dataframe to markdown table and render on streamlit
        rs_df = visual_line.run_single(text1, text2)

        markdown_table = rs_df.to_markdown(index=False)

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
