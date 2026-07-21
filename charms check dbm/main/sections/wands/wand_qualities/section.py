from core.section_definition import SectionDefinition
from .page import WandQualitiesPage


SECTION = SectionDefinition(
    key="wand_qualities",
    title="Wand Qualities",
    order=60,
    page_class=WandQualitiesPage,
)
