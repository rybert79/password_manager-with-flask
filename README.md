# 🛡️ Cyber Vault - Secure Cryptography Manager

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-1.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-38BDF8?style=for-the-badge&logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Cyber Vault** is a web-based Password Manager featuring a dynamic, responsive user interface styled with a modern **Cyberpunk Glassmorphism** aesthetic. Built on top of Python's Flask framework, this application utilizes the **Fernet (Symmetric Encryption)** implementation from the `cryptography` library to guarantee that all locally stored credentials remain fully encrypted and inaccessible without the master key.

---

## 🚀 Key Features

*   **Symmetric Encryption (Fernet):** High-grade cryptographic protection ensuring that data within the local storage cannot be read as plain text without the correct master key.
*   **Dynamic First-Run Key Generator:** The system automatically detects if no database exists on the initial run, generates a secure key, and provides an interactive *double-click auto-copy text block*.
*   **Secure Session Authentication:** Implements Flask Session handling to protect the dashboard route (`/home`) from unauthorized direct URL access.
*   **Glassmorphism Dashboard UI:** Sleek frontend driven by Tailwind CSS utilities, featuring real-time backdrop blur filtering, neon status indicators, and full mobile responsiveness.
*   **Asynchronous CRUD Interaction:** 
    *   **Create:** Easily append new credentials alongside automatic localized timestamps.
    *   **Read:** Displays your secured accounts with a JavaScript-driven *Toggle Visibility* (Eye icon) mechanism.
    *   **Update:** Modify existing records instantly via an inline **Modal Pop-up** without tedious page redirects.
    *   **Delete:** Built-in deletion safety triggers using browser confirmations to prevent accidental data loss.

---

## 🛠️ Tech Stack

*   **Backend:** Python, Flask Framework
*   **Cryptography:** `cryptography.fernet`
*   **Frontend:** HTML5, Tailwind CSS (via CDN), FontAwesome Icons
*   **Database:** Local JSON Storage (`data.json`)

---

## 🇮🇩 Code & Syntax Localisation Note
> **Note on Syntax:** While the user interface and documentation are presented in English, the underlying backend architecture, function definitions, database keys, and variable namings are written using **Indonesian syntax** (e.g., `enkrip()`, `dekrip()`, `liatdata()`, `user_ubah`). This was intentionally structured to align with local development logic while maintaining top-tier security standards.

---
