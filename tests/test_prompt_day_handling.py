from datetime import datetime
from unittest import TestCase

from ui.prompt_logic import (
    DAY_ORDER,
    migrate_prompt_record,
    normalize_day,
    prompt_days,
    prompt_is_valid_for_moment,
    prompt_sort_key,
)


class PromptDayHandlingTests(TestCase):
    def test_normalize_day_supports_dutch_and_english_aliases(self):
        self.assertEqual(normalize_day("Monday"), "ma")
        self.assertEqual(normalize_day("maandag"), "ma")
        self.assertEqual(normalize_day("sun"), "zo")

    def test_migrate_prompt_record_converts_legacy_day_to_days_list(self):
        migrated = migrate_prompt_record({"start": "08:00", "day": "woensdag"})
        self.assertEqual(migrated["days"], ["wo"])
        self.assertNotIn("day", migrated)

    def test_migrate_prompt_record_interprets_blanco_as_every_day(self):
        migrated = migrate_prompt_record({"start": "08:00", "day": "Blanco"})
        self.assertEqual(migrated["days"], DAY_ORDER)

    def test_prompt_days_prefers_days_array_and_normalizes_duplicates(self):
        prompt = {"days": ["Tuesday", "di", "dinsdag", "zo"]}
        self.assertEqual(prompt_days(prompt), ["di", "zo"])

    def test_prompt_days_are_sorted_in_weekday_order(self):
        prompt = {"days": ["za", "ma", "wo"]}
        self.assertEqual(prompt_days(prompt), ["ma", "wo", "za"])

    def test_prompt_sort_key_is_day_first_then_hour(self):
        monday_late = {"day": "ma", "start": "11:00", "end": "12:00", "show": "B"}
        tuesday_early = {"day": "di", "start": "07:00", "end": "08:00", "show": "A"}
        monday_early = {"day": "ma", "start": "07:00", "end": "08:00", "show": "C"}

        sorted_prompts = sorted([monday_late, tuesday_early, monday_early], key=prompt_sort_key)
        self.assertEqual(sorted_prompts, [monday_early, monday_late, tuesday_early])

    def test_prompt_selection_supports_legacy_day_field(self):
        moment = datetime(2026, 9, 7, 9, 30)  # Monday
        prompt = {"day": "monday", "start": "09:00", "end": "10:00", "active": True}
        self.assertTrue(prompt_is_valid_for_moment(prompt, moment))

    def test_prompt_selection_uses_days_list_when_available(self):
        monday = datetime(2026, 9, 7, 9, 30)
        prompt = {"days": ["di", "wo"], "start": "09:00", "end": "10:00", "active": True}
        self.assertFalse(prompt_is_valid_for_moment(prompt, monday))
