from pathlib import Path


APPLICATION_DIRECTORY = Path(__file__).resolve().parent.parent
DATABASE_PATH = APPLICATION_DIRECTORY / "data" / "charms_check_db.json"
BACKUP_DIRECTORY = APPLICATION_DIRECTORY / "data" / "backups"
