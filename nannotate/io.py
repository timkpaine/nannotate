import pandas as pd
import queue
import json
from pprint import pprint


# When running from an interactive prompt, like the python default or IPython
def console_input(msg, q, options):
    return input(_msg_to_in_cs(msg, options))


def console_output(msg, q, options):
    msg = _msg_to_out_cs(msg, options)
    if isinstance(msg, str):
        print(msg)
    else:
        pprint(msg)


def _msg_to_in_cs(msg, options):
    if msg == 'cp':
        return '\nnano>>'
    else:
        return msg


def _msg_to_out_cs(msg, options):
    if isinstance(msg, pd.DataFrame) or isinstance(msg, pd.Series):
        return msg
    elif isinstance(msg, dict):
        return msg
    if msg == 'nl':
        return '\n'
    else:
        return msg


# When running from a Jupyter notebook
def comm_input(msg, q, options):
    # q.put(msg)
    return q.get().strip()


def comm_output(msg, q, options):
    msg = _msg_to_out_cm(msg, options)
    q.put(msg)


def _msg_to_in_cm(msg, options):
    pass


def _msg_to_out_cm(msg, options):
    if isinstance(msg, pd.DataFrame) or isinstance(msg, pd.Series):
        # msg = msg.reset_index().to_json(orient='records')
        msg = msg.reset_index().to_json()
    elif isinstance(msg, dict):
        msg = json.dumps(msg, default=str)
    if msg == 'nl':
        return ''
    elif msg == 'q':
        return '{}'
    return msg


# When running as a standalone site'''
def websocket_input(msg, q, options):
    # q.put(msg)
    try:
        return q.get(timeout=1).strip()
    except queue.Empty:
        return ''


def websocket_output(msg, q, options):
    msg = _msg_to_out_ws(msg, options)
    q.put(msg)


def _msg_to_in_ws(msg, options):
    pass


def _msg_to_out_ws(msg, options):
    if isinstance(msg, pd.DataFrame) or isinstance(msg, pd.Series):
        # msg = msg.reset_index().to_json(orient='records')
        msg = msg.reset_index().to_json()
    elif isinstance(msg, dict):
        msg = json.dumps(msg, default=str)

    if msg == 'nl':
        return ''
    elif msg == 'q':
        return '{}'
    return msg
