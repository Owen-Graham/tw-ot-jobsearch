"""
Translation module for job postings
Uses Google Translate API to translate Chinese to English
"""

import logging
from typing import Dict, Optional
import httpx
from functools import lru_cache

logger = logging.getLogger(__name__)


class JobTranslator:
    """Translates job postings to English"""

    # Google Translate API endpoint (free, no key required for basic usage)
    TRANSLATE_API = "https://translate.googleapis.com/translate_a/element.js"

    def __init__(self):
        """Initialize translator"""
        self.cache = {}

    async def translate_text(self, text: str, max_length: int = 500) -> str:
        """
        Translate Chinese text to English

        Args:
            text: Text to translate
            max_length: Maximum length to process (for safety)

        Returns:
            Translated English text
        """
        if not text or len(text.strip()) == 0:
            return text

        # Check cache first
        cache_key = f"trans_{text[:50]}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Use simple free translation API
            translated = await self._translate_with_google(text)
            self.cache[cache_key] = translated
            return translated
        except Exception as e:
            logger.warning(f"Translation failed for '{text[:50]}': {e}")
            return text

    async def _translate_with_google(self, text: str) -> str:
        """Use Google Translate via simple HTTP request"""
        try:
            async with httpx.AsyncClient() as client:
                # Using a simple translation endpoint
                params = {
                    'client': 'gtx',
                    'sl': 'zh-CN',  # Source: Simplified Chinese (works for Traditional too)
                    'tl': 'en',      # Target: English
                    'dt': 't',       # Get translation
                    'q': text[:500]  # Limit text length
                }

                response = await client.get(
                    'https://translate.google.com/translate_a/single',
                    params=params,
                    timeout=10,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                )
                response.raise_for_status()

                # Parse response - it returns JSON with translations
                import json
                data = response.json()

                # Extract translated text from response
                if data and len(data) > 0 and isinstance(data[0], list):
                    translated_parts = []
                    for item in data[0]:
                        if isinstance(item, list) and len(item) > 0:
                            translated_parts.append(item[0])
                    return ''.join(translated_parts)

                return text
        except Exception as e:
            logger.debug(f"Google Translate API failed: {e}")
            # Fallback: return original text
            return text

    async def translate_job(self, job: Dict) -> Dict:
        """
        Translate all text fields in a job posting

        Args:
            job: Job dictionary with Chinese text

        Returns:
            Job dictionary with added English translations
        """
        translated_job = job.copy()

        # Translate key fields
        fields_to_translate = ['title', 'location', 'organization', 'employment_type', 'salary']

        for field in fields_to_translate:
            if field in job and job[field]:
                translated_job[f'{field}_en'] = await self.translate_text(job[field])

        return translated_job

    def get_cached_size(self) -> int:
        """Return cache size"""
        return len(self.cache)
