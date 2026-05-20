from deep_translator import GoogleTranslator


# Language names are shown in the app. Language codes are used by deep-translator.
# Auto Detect is used only for the source language.
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Somali": "so",
    "Arabic": "ar",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Chinese Simplified": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Swahili": "sw",
    "Turkish": "tr",
}

MAX_HISTORY_ITEMS = 5


def get_source_languages():
    """Return all source languages, including Auto Detect."""
    return list(LANGUAGES.keys())


def get_target_languages():
    """Return target languages without Auto Detect."""
    return [language for language in LANGUAGES.keys() if language != "Auto Detect"]


def translate_text(text, source_language_name, target_language_name):
    """Translate text from the selected source language to the target language."""
    source_code = LANGUAGES[source_language_name]
    target_code = LANGUAGES[target_language_name]

    translator = GoogleTranslator(source=source_code, target=target_code)
    return translator.translate(text)


def create_history_item(source_name, target_name, original_text, translated_text):
    """Create one translation history record."""
    return {
        "source": source_name,
        "target": target_name,
        "original": original_text,
        "translated": translated_text,
    }


def limit_history(history):
    """Keep only the latest history items for the current session."""
    return history[:MAX_HISTORY_ITEMS]
