from reportlab.lib.colors import Color


def draw_watermark(canvas, doc):

    canvas.saveState()

    canvas.setFont(
        "Helvetica-Bold",
        55,
    )

    canvas.setFillColor(
        Color(
            0.90,
            0.90,
            0.90,
            alpha=0.20,
        )
    )

    canvas.rotate(35)

    canvas.drawCentredString(
        260,
        0,
        "CONFIDENTIAL",
    )

    canvas.restoreState()

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        9,
    )

    canvas.drawRightString(
        560,
        20,
        f"Page {doc.page}",
    )

    canvas.restoreState()