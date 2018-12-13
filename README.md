# Panda Chat

## Server

### Requirements

  - Python 3.7.1
  - pip
  - (Recommended) Use Python 3's venv to create a virtual environment. The rest of the commands assume you've done this.
    - `python -m venv server\env`
  - Install other dependencies using pip.
    - `server\env\Scripts\pip install -r server\requirements.txt`

### Running it

  - Start the server.
    - `server\env\Scripts\python server\server_entry.py`
  - Start the test client.
    - `server\env\Scripts\python server\cli_chat_client.py`
