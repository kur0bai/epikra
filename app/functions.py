from fastapi.responses import StreamingResponse
import qrcode
import qrcode.constants
from io import BytesIO

class Functions:
    """
    Generate the QR code based on text, replace file for buffer to future API integrations
    """
    def generate(self, text: str, filename: str = 'qr_code.png'):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )

        qr.add_data(text)
        qr.make(fit=True)
    
        image = qr.make_image(fill_color='black', back_color='white')
        buffer = BytesIO()
        #image.save(filename)
        image.save(buffer, format="PNG")
        buffer.seek(0)
        print(f'QR code generate as {filename}')
        return buffer


