import qrcode
import qrcode.constants

class Functions:
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
        image.save(filename)
        print(f'QR code generate as {filename}')



