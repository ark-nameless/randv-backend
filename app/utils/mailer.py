import smtplib
from email.mime.text import MIMEText

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
            msg['From'] = Address("R & V Private Resort", "Reservation Confirmation", self.sender_mail)
            msg['To'] = email 
            msg.set_content(content, subtype='html')

            with smtplib.SMTP_SSL(self.smtp_server_domain_name, int(self.port)) as server: 
                # server.starttls()
                server.login(self.sender_mail, self.pasword)
                server.send_message(msg)
                
            print(msg)

        except Exception as e: 
            print(e)


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
    def generate_package_reservation_email(customer_name, arrival_date, departure_date, id):
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
            <p><strong>Subject:</strong> Reservation Confirmation - R & V Private Resort - {arrival_date} to {departure_date} - Reservation Id: {id}</p>
            <br>
            <p>Dear {customer_name},</p>
            <br>
            <p>Thank you for choosing to stay at R & V Private Resort. We are delighted to confirm your reservation for the following dates:</p>
            <br>
            <p><strong>Check In Date:</strong> {arrival_date}</p>
            <p><strong>Check Out Date:</strong> {departure_date}</p>
            <br>
            <p>We are excited to welcome you to our luxurious resort and ensure that your stay with us is nothing short of exceptional. Our dedicated staff is committed to providing personalized service and creating unforgettable memories for our esteemed guests.</p>
            <br>
            <p>As a guest at R & V Private Resort, you will have access to our premium amenities, including:</p>
            <ul>
                <li>{amenities_list}</li>
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
                <li>Cancellations request are subject for approval in which the amount of refund may vary.</li>
            </ul>
            <br>
            <p>Once again, we are thrilled that you have chosen R & V Private Resort for your upcoming getaway. We are confident that your stay will exceed your expectations, leaving you with cherished memories. If you have any questions or need further assistance, please feel free to reach out to us.</p>
            <br>
            <p>We look forward to welcoming you to R & V Private Resort and providing you with an unforgettable experience.</p>
            <br>
            <p>Warm regards,</p>
            <p>If you want to cancel your reservation, Please follow this link to apply for cancellation</p>
            <a href="{settings.FRONTEND_URL}/cancel/{id}">Cancel Reservation</a>
        </body>
        </html>
        """

        return html_template
    
    def generate_cancellation_response_email(self, customer_name, reservation_number, arrival_date, departure_date):
        html_template = f"""
        <html>
        <head></head>
        <body>
            <p><strong>Subject:</strong> Reservation Cancellation Request - {reservation_number}</p>
            <br>
            <p>Dear {customer_name},</p>
            <br>
            <p>We have received your request to cancel your reservation at R & V Private Resort. We understand that circumstances may arise that necessitate a change in your travel plans, and we are here to assist you.</p>
            <br>
            <p>After reviewing your reservation details, we will inform you if you can receive the full amount of refund or incure some penalty</p>
            <br>
            <p><strong>Reservation Number:</strong> {reservation_number}</p>
            <p><strong>Check In Date:</strong> {arrival_date}</p>
            <p><strong>Check Out Date:</strong> {departure_date}</p>
            <br>
            <p><strong>Cancellation Policy:</strong></p>
            <ul>
                <li>Cancellation requests are subject to approval, and the amount of refund may vary.</li>
            </ul>
            <br>
            <p>Please note that the cancellation charges are based on our resort's cancellation policy and are necessary to compensate for the reserved accommodations and services that were being held exclusively for your stay.</p>
            <br>
            <p>To proceed with the cancellation, kindly confirm your acceptance of the applicable charges by replying to this email. Upon confirmation, we will initiate the refund process or, if applicable, provide you with a detailed breakdown of the cancellation fees.</p>
            <br>
            <p>Should you have any further questions or concerns, please do not hesitate to reach out to us. We value your patronage and are committed to providing the utmost support during this process.</p>
            <br>
            <p>Thank you for your understanding, and we hope to have the opportunity to welcome you back to R & V Private Resort in the future.</p>
            <br>
        </body>
        </html>
        """

        return html_template

    def generate_rejected_cancellation_response_email(self, customer_name, reservation_number, arrival_date, departure_date, rejection_notes):
        html_template = f"""
        <html>
        <head></head>
        <body>
            <p><strong>Subject:</strong> Reservation Cancellation Request - {reservation_number}</p>
            <br>
            <p>Dear {customer_name},</p>
            <br>
            <p>We have carefully reviewed your cancellation request for reservation {reservation_number} at R & V Private Resort.</p>
            <br>
            <p>Unfortunately, we are unable to approve your cancellation at this time. The details of your reservation are as follows:</p>
            <br>
            <p><strong>Reservation Number:</strong> {reservation_number}</p>
            <p><strong>Check In Date:</strong> {arrival_date}</p>
            <p><strong>Check Out Date:</strong> {departure_date}</p>
            <br>
            <p><strong>Rejection Notes:</strong></p>
            <p>{rejection_notes}</p>
            <br>
            <p>We understand that circumstances may change, and we apologize for any inconvenience caused. If you have any further questions or concerns, please do not hesitate to reach out to us.</p>
            <br>
            <p>Thank you for your understanding, and we hope to have the opportunity to welcome you to R & V Private Resort in the future.</p>
            <br>
        </body>
        </html>
        """

        return html_template


    def generate_accepted_cancellation_response_email(self, customer_name, reservation_number, arrival_date, departure_date, refund_amount, additional_notes):
        html_template = f"""
        <html>
        <head></head>
        <body>
            <p><strong>Subject:</strong> Reservation Cancellation Request - {reservation_number}</p>
            <br>
            <p>Dear {customer_name},</p>
            <br>
            <p>We have processed your cancellation request for reservation {reservation_number} at R & V Private Resort.</p>
            <br>
            <p>The details of your canceled reservation are as follows:</p>
            <br>
            <p><strong>Reservation Number:</strong> {reservation_number}</p>
            <p><strong>Check In Date:</strong> {arrival_date}</p>
            <p><strong>Chekc Out Date:</strong> {departure_date}</p>
            <br>
            <p>We are pleased to inform you that a refund in the amount of {refund_amount} has been initiated. The refund will be processed according to the original payment method used during the reservation.</p>
            <br>
            <p><strong>Additional Notes:</strong></p>
            <p>{additional_notes}</p>
            <br>
            <p>If you have any further questions or concerns, please do not hesitate to reach out to us. We value your patronage and look forward to the opportunity to serve you in the future.</p>
            <br>
            <p>Thank you for choosing R & V Private Resort.</p>
            <br>
        </body>
        </html>
        """

        return html_template

    def generate_check_out_thank_you_email(self, customer_name, reservation_id):
        html_template = f"""
        <html>
        <head></head>
        <body>
            <p><strong>Subject:</strong> Thank You for Your Stay - Feedback Request</p>
            <br>
            <p>Dear {customer_name},</p>
            <br>
            <p>Thank you for choosing R & V Private Resort as your accommodation during your recent stay. We hope you had a wonderful experience and enjoyed your time with us.</p>
            <br>
            <p>We value your feedback and would greatly appreciate it if you could take a moment to share your experience with us. Your valuable input will help us improve and provide even better services to our future guests.</p>
            <br>
            <p>Please click on the link below to leave a review:</p>
            <p><a href="{self.origin}/review/{reservation_id}">Review for your Experience</a></p>
            <br>
            <p>We genuinely appreciate your time and feedback. Thank you once again for choosing R & V Private Resort. We look forward to serving you again in the future.</p>
            <br>
        </body>
        </html>
        """

        return html_template

    def generate_payment_accepted_email(self, customer_name, reservation_number, payment_amount):
        html_template = f"""
        <html>
        <head></head>
        <body>
            <p><strong>Subject:</strong> Payment Accepted - Reservation {reservation_number}</p>
            <br>
            <p>Dear {customer_name},</p>
            <br>
            <p>Thank you for your recent payment for reservation {reservation_number} at R & V Private Resort.</p>
            <br>
            <p>We are pleased to inform you that your payment of {payment_amount} has been successfully accepted.</p>
            <br>
            <p>Payment Details:</p>
            <ul>
                <li>Reservation Number: {reservation_number}</li>
                <li>Payment Amount: {payment_amount}</li>
            </ul>
            <br>
            <p>If you have any questions or require any further assistance regarding your reservation, please do not hesitate to contact us. We look forward to welcoming you to R & V Private Resort and ensuring a delightful stay for you.</p>
            <br>
            <p>Thank you for choosing R & V Private Resort.</p>
            <br>
        </body>
        </html>
        """

        return html_template
    

    def generate_password_reset_email(self, staff_name, token):
        html_template = f"""
        <html>
        <head></head>
        <body>
            <p><strong>Subject:</strong> Staff Password Reset Request</p>
            <br>
            <p>Dear {staff_name},</p>
            <br>
            <p>We have received a request to reset your password for your staff account at R & V Private Resort.</p>
            <br>
            <p>To proceed with the password reset, please click on the link below:</p>
            <p><a href="{self.origin}/reset-password/{token}">Password Reset Link</a></p>
            <br>
            <p>If you did not request a password reset, please ignore this email.</p>
            <br>
            <p>If you require any further assistance or have any questions, please contact our support team. We are here to assist you.</p>
            <br>
            <p>Thank you for being a valued member of the R & V Private Resort staff.</p>
            <br>
        </html>
        """

        return html_template