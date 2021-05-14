from typing import Optional

import pandas as pd
import sweetviz as sv

from pywebio import start_server
from pywebio.input import file_upload
from pywebio.output import put_html, put_loading, put_markdown
from pywebio.session import info as session_info


def app():
    file = file_upload(label='Upload your CSV file', accept='.csv')
    content = file['content'].decode('utf-8')
    df = _on_frame(content)
    create_profile(df, title='Title of your dataset')


def _on_frame(content: str, use_cols=True, sep=','):
    data = [x.split(sep) for x in content.split('\n')]
    if use_cols:
        return pd.DataFrame(data[1:], columns=data[0])
    else:
        return pd.DataFrame(data)


def t(eng, rus):
    return rus if 'ru' in session_info.user_language else eng


def create_profile(df: pd.DataFrame = None, title: Optional[str] = 'Title'):
    profile = None
    with put_loading(shape='grow'):
        report = sv.analyze(df)
        # NOTE: Line below will take some time to complete...
        profile = report.show_html(layout='vertical')
    if profile:
        print(session_info.user_language)
        put_html(profile)
    else:
        put_markdown(
            t(
                r"""
                ## <p align="middle">_Errors occured analyzing the \"csv\" file._</p>
                """,
                r"""
                ## <p align="middle">_При анализе загруженного \"csv\" файла возникли ошибки._</p>
                """
            ), strip_indent=4
        )


if __name__ == '__main__':
    start_server(app, port=37791, debug=False, cdn=False)
