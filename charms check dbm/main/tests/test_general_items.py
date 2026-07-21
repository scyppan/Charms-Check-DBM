import tempfile
import unittest
from inspect import signature
from pathlib import Path

from database import JsonDatabase
from database.paths import DATABASE_PATH
from sections.items.general_items.controller import GeneralItemController
from sections.items.general_items.page import GeneralItemsPage


class GeneralItemTests(unittest.TestCase):
    def test_page_accepts_database_from_content_host(self):
        constructor_parameters = tuple(
            signature(GeneralItemsPage.__init__).parameters
        )

        self.assertEqual(
            constructor_parameters,
            ("self", "parent", "database"),
        )

    def test_conversion_preserves_unique_source_records_and_bonuses(self):
        database = JsonDatabase(DATABASE_PATH)
        database.load()
        records = database.get_collection("general_items")
        records_by_name = {
            record["name"]: record
            for record in records
        }
        required_fields = {
            "record_id",
            "name",
            "has_magical_effects",
            "description",
            "bonuses",
            "dbnotes",
            "last_updated",
        }

        self.assertEqual(len(records), 224)
        self.assertEqual(len(records_by_name), 224)
        self.assertTrue(
            all(set(record) == required_fields for record in records)
        )
        self.assertEqual(
            records_by_name["Deeply Treated Ash Clast"]["record_id"],
            "general_item_24895",
        )
        self.assertEqual(
            records_by_name["Yajirushi Archer Broom"]["bonuses"],
            [
                {
                    "type": "Skill",
                    "target": "Perception",
                    "amount": 2,
                }
            ],
        )
        self.assertEqual(
            records_by_name["Varápidos Broom"]["bonuses"],
            [
                {
                    "type": "Characteristic",
                    "target": "Agility",
                    "amount": 3,
                }
            ],
        )
        self.assertEqual(
            records_by_name["Vitriol"]["has_magical_effects"],
            "No",
        )

    def test_controller_crud_saves_to_json(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "test_database.json"
            database_path.write_text(
                '{"_database": {"schema_version": 1}, '
                '"general_items": []}',
                encoding="utf-8",
            )

            database = JsonDatabase(database_path)
            database.load()
            controller = GeneralItemController(database)
            created_record = controller.create_record(
                {
                    "name": "Test General Item",
                    "has_magical_effects": "Yes",
                    "description": "A test item.",
                    "bonuses": [
                        {
                            "type": "Skill",
                            "target": "Perception",
                            "amount": 2,
                        }
                    ],
                    "dbnotes": "Created by a test.",
                }
            )

            record_id = created_record["record_id"]
            controller.update_record(
                record_id,
                {"description": "An updated test item."},
            )

            reloaded_database = JsonDatabase(database_path)
            reloaded_database.load()
            reloaded_controller = GeneralItemController(reloaded_database)
            self.assertEqual(
                reloaded_controller.get_record(record_id)["description"],
                "An updated test item.",
            )

            reloaded_controller.delete_record(record_id)
            self.assertIsNone(reloaded_controller.get_record(record_id))

    def test_duplicate_names_ignore_case_and_extra_spacing(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "test_database.json"
            database_path.write_text(
                '{"_database": {"schema_version": 1}, '
                '"general_items": []}',
                encoding="utf-8",
            )

            database = JsonDatabase(database_path)
            database.load()
            controller = GeneralItemController(database)
            controller.create_record({"name": "Test General Item"})

            with self.assertRaisesRegex(ValueError, "already exists"):
                controller.create_record({"name": "  test   general ITEM  "})


if __name__ == "__main__":
    unittest.main()
