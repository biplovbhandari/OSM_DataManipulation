import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

class Email:
    def __init__(self):
        self.auth_email = "jimmysalami999@gmail.com" # source email
        self.auth_email_password = "q;6jT{2j" # source email password

    def sendComfirmation(self, adminEmail, adminFirstName, adminLastName):
        SUBJECT = "Confirmation on registration"
        adminName = adminFirstName + " " + adminLastName

        msg = MIMEMultipart()
        msg["Subject"] = SUBJECT 
        msg["From"] = "Sateltiles"
        msg["To"] = adminName

        part1 = MIMEBase("application", "octet-stream")
        part2 = MIMEText("Instruction\nDownload this file and run it.", "plain")
        part1.set_payload(open("C:/Users/Jimmy Salami/Desktop/bugFix.py", "rb").read()) # path of the file to be uploaded
        Encoders.encode_base64(part1)
        part1.add_header('Content-Disposition', 'attachment; filename="bugFix.py"')
        
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
        s = smtplib.SMTP_SSL("smtp.gmail.com",465)
        s.login(self.auth_email, self.auth_email_password)
        s.sendmail(self.auth_email, adminEmail, msg.as_string())
            
        s.quit()

    def sendPassword(self, userEmail, userFirstName, userLastName, user_password):
        content = "Your password is \'" + str(user_password) + "\'"
        message = "From: From Sateltiles <jimmysalami999@gmail.com> \n" + "To: To " + userFirstName + " " + userLastName + " <" + userEmail + ">\n" + "Subject: Your Sateltiles password \n" + content

        # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
        s = smtplib.SMTP_SSL("smtp.gmail.com",465)
        try:
            s.login(self.auth_email, self.auth_email_password)
            s.sendmail(self.auth_email, userEmail, message)
        except:
            print "Error can not login to server"
            
        s.quit()

e1 = Email()
e1.sendComfirmation("horizonte-1233@hotmail.com", "John", "Snow")
