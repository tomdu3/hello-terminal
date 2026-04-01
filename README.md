# Hello Terminal

A terminal based "Hello World" web site.

## Latin Proverbs

The proverbs are taken from the website https://www.pinteric.com/proloc.html.

The script `download_proverbs.py` downloads the proverbs from the website and saves them to a JSON file. Execute it using:

```bash
uv run download_proverbs.py
```

## Stack Description

- **Backend:** Python 3 (built-in `http.server` & `socketserver`)
- **Data Storage:** JSON file (`latin_proverbs.json`)
- **Frontend (Web):** Vanilla HTML/CSS
- **Frontend (Terminal):** Plain text with ANSI color codes

## Setup and Installation

This project uses [uv](https://github.com/astral-sh/uv) to manage the Python environment. To create the environment and install dependencies, run:

```bash
uv sync
```

## Running the Server

Start the application by executing the server script within the `uv` environment:

```bash
uv run server.py
```

The server will start listening on port `8000` by default.

## Testing the Terminal Interface

To view the terminal version, open your terminal and run `curl`:

```bash
curl http://localhost:8000
```