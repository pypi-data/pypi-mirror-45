import json
import sys
import os
import webbrowser

from bs4 import BeautifulSoup
import requests

from atarg import utils
from atarg.languages import languages

ATCODER_LOGIN_URL = 'https://atcoder.jp/login'
SETTING_FILE = os.environ['HOME'] + '/.atarg.json'

def extract_by_name(html_text: str, name: str):
    """
    HTMLテキストを解析し、
    HTML要素のうち、attributeのnameがnameと一致するものの値を返す

    Parameters
    ----------
    html_text : str
        HTMLテキスト
    name : str
        name attributeの名前

    Returns
    ----------
    value
        attributeのnameがnameと一致するものの値
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    try:
        value = soup.find(attrs={'name': name}).get('value')
    except AttributeError as err:
        sys.stderr.write('Attribute[{}] is not found in HTML\n'.format(name))
        sys.exit(1)
    return value


def login(username: str, password: str) -> requests.Session:
    """
    Atcoderにログインする

    Parameters
    ----------
    username : str
        ユーザ名
    password : str
        パスワード

    Returns
    ----------
    session
        ログインに成功したセッション
    """
    session = requests.Session()
    response = session.get(ATCODER_LOGIN_URL)
    csrf_token = extract_by_name(response.text, 'csrf_token')
    data = {
            'username': username,
            'password': password,
            'csrf_token': csrf_token,
            }
    response = session.post(ATCODER_LOGIN_URL, data=data)
    if 'Username or Password is incorrect.' in response.text:
        sys.stderr.write('Authentication failure\n')
        sys.exit(1)
    return session


def submit(contest: str, contest_no: int, task: str, source_code_filename: str):
    """
    Atcoderに解答を提出する

    Parameters
    ----------
    contest
        コンテスト名. ABC, ARC or AGC
    contest_no
        コンテストの番号
    task
        タスク名. A, B, C or D

    Returns
    ----------
    """
    settings = None
    with open(SETTING_FILE) as f:
        settings = json.loads(f.read())

    session = login(settings['username'], settings['password'])
    task_url = utils.compose_task_url(contest, contest_no, task)
    task_response = session.get(task_url)
    csrf_token = extract_by_name(task_response.text, 'csrf_token')
    task_screen_name = extract_by_name(task_response.text, 'data.TaskScreenName')

    with open(source_code_filename) as f:
        source_code_text = f.read()
        data = {
                'csrf_token': csrf_token,
                'data.LanguageId': languages[settings['language']],
                'sourceCode': source_code_text,
                'data.TaskScreenName': task_screen_name,
                }
        submit_url = utils.compose_submit_url(contest, contest_no)
        submit_response = session.post(submit_url, data=data)
        webbrowser.open(submit_response.url)
