import smtplib
from PIL import Image
from io import BytesIO
import os
from email.message import EmailMessage

SENDER = "lhanco@gmail.com"
PASSWORD = os.getenv("Python_App_Send_Email")
RECEIVER = "lhanco@gmail.com"


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we have just seen a new customer.")

    with open(image_path, "rb") as file:
        content = file.read()

    image_data = BytesIO(content)
    image_attached = Image.open(image_data)
    image_format = image_attached.format

    email_message.add_attachment(content,
                                 filename=f"new_customer.{image_attached.format}",
                                 maintype="image",
                                 subtype=image_format)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

    print("Email was sent!")


if __name__ == "__main__":
    send_email(image_path="images/11.png")


























































