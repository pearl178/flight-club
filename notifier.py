import smtplib

class Notifier:
    def __init__(self, email_list):
        self.my_email = "pearl.sailikebuli@yahoo.com"
        self.password = '117878Tian'
        self.receive_emails = email_list

    def send_emails(self, message):
        with smtplib.SMTP('smtp.mail.yahoo.com', port=587) as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.password)
            for receive_email in self.receive_emails:
                connection.sendmail(
                    from_addr=self.my_email,
                    to_addrs=receive_email,
                    msg=f"Subject:LOW PRICE!\n\n {message}"
                )

