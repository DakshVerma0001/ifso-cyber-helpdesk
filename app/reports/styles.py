from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

styles = getSampleStyleSheet()

TITLE = styles["Heading1"]
TITLE.alignment = TA_CENTER
TITLE.textColor = colors.darkblue
TITLE.spaceAfter = 14

SECTION = styles["Heading2"]
SECTION.textColor = colors.darkblue
SECTION.spaceBefore = 12
SECTION.spaceAfter = 6

NORMAL = styles["BodyText"]
NORMAL.leading = 18

FOOTER = styles["Italic"]
FOOTER.fontSize = 8
FOOTER.textColor = colors.grey

TABLE_HEADER = colors.HexColor("#003366")

TABLE_ALT = colors.HexColor("#F4F6F8")

PAGE_MARGIN = 1.8 * cm