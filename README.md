# CodeAlpha Language Translation Tool

## Internship Domain

Artificial Intelligence

## Task

Task 1 - Language Translation Tool

## Project Overview

CodeAlpha Language Translation Tool is a simple web-based translation application developed as part of the CodeAlpha Artificial Intelligence Internship.

The application allows users to enter text, select a source language, select a target language, and view the translated result through a clean and user-friendly interface.

This project uses an existing translation service through the `deep-translator` package. No custom AI model was trained for this project.

> Note: Translation accuracy may vary depending on the language and translation service.

## Project Objective

The objective of this project is to build a simple AI-powered language translation tool that can translate text between common languages. The project focuses on practical application development, user input handling, translation processing, error handling, and clean UI presentation.

## Features

- Clean and simple Streamlit user interface
- Text area for entering text to translate
- Source language selection with Auto Detect support
- Target language selection without Auto Detect
- Translation result displayed clearly
- Copy Translated Text button
- Friendly warning for empty input
- Friendly warning for selecting the same source and target language
- Graceful error handling for translation failures
- Translation history saved during the current session
- Clear Translation History button
- Somali language support
- Professional layout suitable for screenshots and demo video

## Supported Languages

The application supports the following languages:

- Auto Detect
- English
- Somali
- Arabic
- Spanish
- French
- German
- Italian
- Portuguese
- Hindi
- Chinese Simplified
- Japanese
- Korean
- Russian
- Swahili
- Turkish

Auto Detect is available only for the source language.

## Technologies Used

- Python
- Streamlit
- deep-translator
- HTML/CSS customization
- Git
- GitHub

## Folder Structure

```text
CodeAlpha_Language_Translation_Tool/
│
├── app.py
├── frontend.py
├── translator.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── home_page.png
    ├── translation_result.png
    └── translation_history.png