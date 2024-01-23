import difflib
import re
from typing import List, Tuple

import pandas as pd


class TextLineVisualize:
    def __init__(
        self,
        highlight_color_left: str = 'rgba(255, 0, 0, 0.6)',
        highlight_color_right: str = 'rgba(0, 255, 0, 0.6)',
        split_char: str = '\n',
        empty_char: str = '&nbsp;',
    ) -> None:
        self.color_left = f"<span style='background-color: {highlight_color_left};'>"
        self.color_right = f"<span style='background-color: {highlight_color_right};'>"
        self.reset_code = '</span>'
        self.split_char = split_char
        self.empty_char = empty_char

    def run_single(self, text1: str, text2: str) -> pd.DataFrame:
        """Run visualization for a pair of texts.

        Args:
            text1 (str): Original text
            text2 (str): Predicted text

        Returns:
            pd.DataFrame: Dataframe of visualization result
        """
        text1 = text1.strip()
        text2 = text2.strip()

        text1 = text1.split(self.split_char)
        text2 = text2.split(self.split_char)

        diff = difflib.Differ().compare(text1, text2)

        result1, result2 = self._highlight_differences(list(diff))

        df = pd.DataFrame(columns=['Left Index', 'Text 1', 'Right Index', 'Text 2'])

        line_num1 = 1
        line_num2 = 1
        for line1, line2 in zip(result1, result2):
            row = {
                'Left Index': None,
                'Text 1': None,
                'Right Index': None,
                'Text 2': None,
            }
            if line1 != "":
                if line1.startswith("-"):
                    gt_index = f":red[{str(line_num1) + line1[0]}]"
                else:
                    gt_index = str(line_num1) + line1[0]
                row['Left Index'] = gt_index
                row['Text 1'] = line1[1:]
                line_num1 += 1
            else:
                row['Text 1'] = line1

            if line2 != "":
                if line2.startswith("+"):
                    pred_index = f":green[{str(line_num2) + line2[0]}]"
                else:
                    pred_index = str(line_num2) + line2[0]
                row['Right Index'] = pred_index
                row['Text 2'] = line2[1:]
                line_num2 += 1
            else:
                row['Text 2'] = line2

            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

        return df

    def _highlight_differences(
        self, diff_result: List[str]
    ) -> Tuple[List[str], List[str]]:
        """Highlight differences between two texts.

        Args:
            diff_result (list[str]): diff result get from difflib.Differ().compare
            text1 (list[str]): list of strings of text1
            text2 (list[str]): list of strings of text2

        Returns:
            tuple[list[str], list[str]]: list of strings of text1 and text2 after highlighted
        """

        merge_rs = self._merge_diff_result(diff_result)

        left_list, right_list = [], []

        equal_annotation = "="
        left_annotation = "-"
        right_annotation = "+"
        while merge_rs != []:
            line = merge_rs.pop(0)
            if line.startswith("  "):
                left_list.append(equal_annotation + line[2:])
                right_list.append(equal_annotation + line[2:])

            elif line.startswith("- "):
                if (
                    merge_rs != []
                    and merge_rs[0].startswith("+ ")
                    and (self.color_right in merge_rs[0] or self.color_left in line)
                ):
                    left_list.append(left_annotation + line[2:])
                    right_list.append(right_annotation + merge_rs.pop(0)[2:])

                else:
                    color_full_left = self.color_left + line[2:] + self.reset_code
                    left_list.append(left_annotation + color_full_left)
                    right_list.append("")

            elif line.startswith("+ "):
                color_full_right = self.color_right + line[2:] + self.reset_code
                left_list.append("")
                right_list.append(right_annotation + color_full_right)

        return left_list, right_list

    def _merge_diff_result(self, diff_result: List[str]) -> List[str]:
        """Merge diff result to highlight differences between two texts.

        Args:
            diff_result (List[str]): diff result get from difflib.Differ().compare

        Returns:
            List[str]: merged diff result
        """
        merged_diff_result = []
        for idx, line in enumerate(diff_result):
            if line.startswith("  "):
                merged_diff_result.append(line)

            elif line.startswith("? "):
                color = (
                    self.color_left
                    if diff_result[idx - 1].startswith("- ")
                    else self.color_right
                )
                diff_ranges = self._find_ranges_with_indices(diff_result[idx][2:])
                merged_diff_result.append(
                    diff_result[idx - 1][:2]
                    + self._insert_color_tags(
                        diff_result[idx - 1][2:], diff_ranges, color
                    )
                )
            else:
                if idx < len(diff_result) - 1 and diff_result[idx + 1].startswith("? "):
                    continue
                merged_diff_result.append(line)

        return merged_diff_result

    def _find_ranges_with_indices(self, diff_string: str) -> List[Tuple[int, int]]:
        """Find ranges with indices that need to be highlighted.

        Args:
            diff_string (str): input diff string get from difflib.Differ().compare

        Returns:
            list[tuple[int, int]]: list of (start_index, end_index) of ranges that need to be highlighted
        """
        patterns = r'(\++|-+|\^+)'
        matches = re.finditer(patterns, diff_string)
        ranges = []
        for match in matches:
            start_index = match.start()
            end_index = match.end() - 1
            ranges.append((start_index, end_index))

        return ranges

    def _insert_color_tags(
        self, input_string: str, ranges: List[Tuple[int, int]], highlight_code: str
    ) -> str:
        """Insert color tags to input string at given ranges.

        Args:
            input_string (str): string to be highlighted
            ranges (list[tuple[int, int]]): list of (start_index, end_index) of ranges that need to be highlighted
            highlight_code (str): color code

        Returns:
            str: highlighted string
        """
        offset = 0
        for start, end in ranges:
            modified_start = start + offset
            modified_end = end + offset
            input_string = (
                input_string[:modified_start]
                + highlight_code
                + input_string[modified_start : modified_end + 1]
                + self.reset_code
                + input_string[modified_end + 1 :]
            )
            offset += len(highlight_code) + len(self.reset_code)

        return input_string


if __name__ == '__main__':
    text1 = '''
    BT VN: Cảm nhận về bài ca dao sau : 
    " Cày đồng đang buổi ban trưaMồ hôi thánh thót như mua ruộng cây 
    Ai ơi bưng bát cơm đầy. 
    Dẻo thơm một hạt đắng cay muôn phần?
    '''

    text2 = '''
    BT VN: Cảm nhận về bài ca dao sau : 
    " Cày đồng đang buổi ban trưa 
    Ai ơi bưng bát cơm đầy. Mổ hôi thánh thót như mua ruộng cây 
    Dẻo thơ m một hạt đắng cay muôn p hồn?
    '''

    visual_line = TextLineVisualize(
        highlight_color_left='rgba(255, 0, 0, 0.6)',  # Default: 'red' with opacity 0.6
        highlight_color_right='rgba(0, 255, 0, 0.6)',  # Default: 'green' with opacity 0.6
        split_char='\n',  # Default: '\n'
        empty_char='&nbsp;',  # Default: '#'
    )

    ### Visualize with streamlit
    import streamlit as st

    st.set_page_config(layout="wide")

    # Convert dataframe to markdown table and render on streamlit
    rs_df = visual_line.run_single(text1, text2)
    st.dataframe(rs_df)
    st.markdown(rs_df.to_markdown(index=False), unsafe_allow_html=True)
