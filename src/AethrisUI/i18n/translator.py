from typing import Dict, Any, Optional
from ..core.context import create_context

class I18n:
    _translations: Dict[str, Dict[str, str]] = {}
    _current_locale: str = "en"
    locale_context = create_context('locale')
    
    @classmethod
    def add_translations(cls, locale: str, translations: Dict[str, str]):
        cls._translations[locale] = translations
    
    @classmethod
    def set_locale(cls, locale: str):
        if locale in cls._translations:
            cls._current_locale = locale
    
    @classmethod
    def t(cls, key: str, params: Dict[str, Any] = None) -> str:
        translation = cls._translations.get(cls._current_locale, {}).get(key, key)
        if params:
            return translation.format(**params)
        return translation

def use_translation():
    from ..hooks import use_context
    locale = use_context(I18n.locale_context)
    return I18n.t 