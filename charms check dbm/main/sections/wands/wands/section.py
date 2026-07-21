from core.section_definition import SectionDefinition
from .page import WandsPage


SECTION = SectionDefinition(
    key="wands",
    title="Wands",
    order=70,
    page_class=WandsPage,
)
