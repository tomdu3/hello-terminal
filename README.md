# 🏛️ Hello Terminal: The Latin Reference

A terminal-first, dual-client Latin grammar reference and proverb tool. Built for the modern classicist who lives in the CLI but appreciates a beautiful web interface.

## 🚀 Overview

**Hello Terminal** is a lightweight web server that serves different content based on how you access it.
- **Terminal Users (`curl`, `wget`)**: Get high-contrast, ANSI-colored text with ASCII art.
- **Web Browsers**: Get a responsive HTML experience that mirrors the terminal aesthetic.

The project has evolved from a simple "Hello World" into a comprehensive reference for Latin declensions, conjugations, and grammatical exceptions.

---

## ✨ Features

- **Terminal-First Experience**: Optimized for `curl`. Use it without leaving your development environment.
- **Dual Rendering Engine**: A custom backend detects your `User-Agent` to serve either `.term` (ANSI/Plaintext) or `.html` templates.
- **Comprehensive Latin Reference**:
  - **Declensions**: Full tables for 1st through 5th declensions.
  - **Conjugations**: Active indicative tables for 1st, 2nd, 3rd, 3rd-io, and 4th conjugations.
  - **Grammatical Exceptions**: Specialized pages for tricky declension exceptions.
- **Proverb of the Day**: Every visit to the home page serves a new wisdom from a curated dataset of Latin proverbs.
- **Ultra-Lightweight**: Built using Python's native `http.server`. Zero heavy frameworks, maximum speed.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14 (utilizing `http.server` & `socketserver`)
- **Environment**: Managed by [uv](https://github.com/astral-sh/uv)
- **Data**: JSON-backed proverb storage (`latin_proverbs.json`)
- **Templating**: Custom `renderers.py` supporting `.term` (str.format) and `.html` rendering.

---

## 📖 Available Routes

You can access any of these routes via your browser or terminal:

### Grammar Reference
| Category | Routes |
| :--- | :--- |
| **Declensions** | `/first-declension`, `/second-declension`, `/third-declension`, `/fourth-declension`, `/fifth-declension` |
| **Conjugations** | `/first-conjugation`, `/second-conjugation`, `/third-conjugation`, `/third-io-conjugation`, `/fourth-conjugation` |
| **Exceptions** | `/first-declension-ex`, `/second-declension-ex`, `/third-declension-ex` |

### General
- `/`: Home page with the **Proverb of the Day**.
- `/assets/`: Direct access to ASCII art and images.

---

## 🏗️ Setup & Running

This project uses `uv` for environment management.

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the server**:
   ```bash
   uv run server.py
   ```
   The server will start at `http://localhost:8000`.

---

## 🖱️ Usage Examples

### From the Terminal (Recommended)
```bash
# Get the proverb of the day
curl http://localhost:8000

# Look up the 3rd declension
curl http://localhost:8000/third-declension

# Check exceptions for the 2nd declension
curl http://localhost:8000/second-declension-ex
```

### From the Browser
Simply navigate to `http://localhost:8000` in your favorite browser to see the HTML version of the terminal interface.

---

## ⚙️ How it Works

The server uses a custom `serve_template` function in `server.py` that checks the `User-Agent` header. If it finds keywords like `curl`, `wget`, or `httpie`, it triggers the `terminal_renderer` which injects ANSI color codes defined in `utils/renderers.py` into a `.term` template. Otherwise, it uses the `html_renderer` for a standard web response.