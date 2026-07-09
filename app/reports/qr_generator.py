import os
import qrcode


class QRGenerator:

    @staticmethod
    def generate(
        complaint_id: str,
        output_dir: str,
    ) -> str:

        os.makedirs(output_dir, exist_ok=True)

        path = os.path.join(
            output_dir,
            f"{complaint_id}.png",
        )

        qr = qrcode.QRCode(
            version=2,
            box_size=8,
            border=2,
        )

        qr.add_data(complaint_id)

        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        img.save(path)

        return path