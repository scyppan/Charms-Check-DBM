from core.section_definition import SectionDefinition
from .page import PotionsPage


SECTION = SectionDefinition(
    key="potions",
    title="Potions",
    order=160,
    page_class=PotionsPage,
)
