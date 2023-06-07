import smtplib, ssl
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
from app.config.config import settings


class Mailer:

    def __init__(self):
        self.port = settings.MAILER_PORT 
        self.smtp_server_domain_name = settings.MAILER_DOMAIN
        self.sender_mail = settings.MAILER_USERNAME
        self.pasword = settings.MAILER_PASSWORD
        self.origin = settings.FRONTEND_URL

    def send(self, email, subject, content):
        try :
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = Address("MSEUFCI Class Scheduling", "class_schedules", self.sender_mail)
            msg['To'] = email 
            msg.set_content(content)

            server = smtplib.SMTP(self.smtp_server_domain_name, self.port)

            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.sender_mail, self.pasword)

            server.send_message(msg)

        except Exception as e: 
            print(e)
        finally: 
            server.quit() #type: ignore


    def send_(self, email, token): 
        msg = EmailMessage()
        msg['Subject'] = 'MSEUFCI Scheduling Password Reset'
        msg['From'] = self.sender_mail 
        msg['To'] = email
        msg.set_content(f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body class="flex flex-col justify-center items-center w-full">
                <div class="relative flex min-h-screen flex-col justify-center overflow-hidden bg-gray-50 py-6 sm:py-12">
                    <img src="https://asset.cloudinary.com/dfua49gkk/fe43ea85497cc64f089494d27415a618" alt="" class="absolute top-1/2 left-1/2 max-w-none -translate-x-1/2 -translate-y-1/2" width="1308" />
                    <div class="absolute inset-0 bg-[url(/img/grid.svg)] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
                        <div class="relative bg-white px-6 pt-10 pb-8 shadow-xl ring-1 ring-gray-900/5 sm:mx-auto sm:max-w-lg sm:rounded-lg sm:px-10">
                            <div class="mx-auto max-w-md">
                                <img src="https://res.cloudinary.com/dfua49gkk/image/upload/v1668132679/class-scheduling/logo-filled_heuqyp.png" alt="Tailwind Play" style="height: 64px"/>
                                <h1 class="text-2xl font-semibold font-sans">Manuel S. Enverga University Foundation Candelaria Incorporated.</h1>
                                <div class="divide-y divide-gray-300/50">
                                <div class="space-y-6 py-8 text-base leading-7 text-gray-600">
                                    <p>We have received your request for password reset</p>
                                    <p>Please follow this link to reset your password</p>
                                    <a href="{self.origin}/{token}/change-password" class="text-red-500 hover:text-red-600">Reset Password &rarr;</a>
                                </div>
                                <div class="pt-8 text-base font-semibold leading-7">
                                    <p class="text-gray-900">Login to website</p>
                                    <a href="{self.origin}/login" class="text-sky-500 hover:text-sky-600">MSEUFCI Scheduling &rarr;</a>
                                    </p>
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        ''', subtype='html')

        with smtplib.SMTP(self.smtp_server_domain_name, self.port) as server: 
            server.starttls()
            server.login(self.sender_mail, self.pasword)
            server.send_message(msg)

    @staticmethod
    def generate_package_reservation_email(customer_name, arrival_date, departure_date, num_guests, room_type):
        amenities = [
            "Adult Swimming Pool"
            "Kiddie Pool"
            "1 Open Room (king size bed)"
            "1 AC room (double deck)"
            "2 Sleeper foams"
            "Folding chair"
            "2 Shower areas"
            "3 comfort rooms"
            "Free use of Griller"
            "Videoke"
            "Free use of Tables and Chairs"
            "Free use of Mountain bikes"
            "Bar counter"
            "Kitchen Area"
            "Heavy Duty Gas Stove with LPG"
            "Refrigerator"
            "Water Dispenser"
            "Microwave"
            "2 Electric fans"
            "2 Bahay kubo"
            "Lounge areas"
            "Parking space"
        ]

        amenities_list = ''.join([f"<li>{amenity}</li>" for amenity in amenities])

        html_template = f"""
        <html>
        <head></head>
        <body>
            <p><strong>Subject:</strong> Reservation Confirmation - R & V Private Resort - {arrival_date} to {departure_date}</p>
            <br>
            <p>Dear {customer_name},</p>
            <br>
            <p>Thank you for choosing to stay at R & V Private Resort. We are delighted to confirm your reservation for the following dates:</p>
            <br>
            <p><strong>Arrival Date:</strong> {arrival_date}</p>
            <p><strong>Departure Date:</strong> {departure_date}</p>
            <br>
            <p><strong>Number of Guests:</strong> {num_guests}</p>
            <br>
            <p><strong>Accommodation:</strong> {room_type}</p>
            <br>
            <p>We are excited to welcome you to our luxurious resort and ensure that your stay with us is nothing short of exceptional. Our dedicated staff is committed to providing personalized service and creating unforgettable memories for our esteemed guests.</p>
            <br>
            <p>As a guest at R & V Private Resort, you will have access to our premium amenities, including:</p>
            <ul>
                {amenities_list}
            </ul>
            <br>
            <p>Should you require any additional information or have specific preferences, please do not hesitate to contact our concierge desk at [resort contact number] or via email at [resort email address].</p>
            <br>
            <p>We kindly request that you arrive at our resort reception on the specified arrival date, where our friendly staff will be ready to assist you with the check-in process. Please note that check-in time is at [check-in time] and check-out time is at [check-out time].</p>
            <br>
            <p><strong>Payment Details:</strong></p>
            <p>To secure your reservation, a deposit of [deposit amount] is required. We offer various payment options, including credit card payments and bank transfers. Detailed payment instructions will be provided upon your request.</p>
            <br>
            <p><strong>Cancellation Policy:</strong></p>
            <ul>
                <li>Cancellations made [number of days] or more prior to the arrival date are eligible for a full refund of the deposit.</li>
                <li>Cancellations made within [number of days] of the arrival date will result in the forfeiture of the deposit.</li>
            </ul>
            <br>
            <p>Once again, we are thrilled that you have chosen R & V Private Resort for your upcoming getaway. We are confident that your stay will exceed your expectations, leaving you with cherished memories. If you have any questions or need further assistance, please feel free to reach out to us.</p>
            <br>
            <p>We look forward to welcoming you to R & V Private Resort and providing you with an unforgettable experience.</p>
            <br>
            <p>Warm regards,</p>
            <p>[Resort Manager's Name]</p>
            <p>[Resort Name]</p>
            <p>[Resort Contact Information]</p>
        </body>
        </html>
        """

        return html_template