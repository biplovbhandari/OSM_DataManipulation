import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText

class Email:
    def __init__(self):
        self.auth_email = "jimmysalami999@gmail.com" # source email
        self.auth_email_password = "q;6jT{2j" # source email password

    def sendComfirmation(self, adminEmail, adminFirstName, adminLastName):
        content = "This person want to register to Sateltiles. Do you want make person admin or normal user? ADMIN , NORMAL"
        message = "From: From Sateltiles <jimmysalami999@gmail.com> \n" + "To: To " + adminFirstName + " " + adminLastName + " <" + adminEmail + ">\n" + "Subject: Confirmation on registration \n" + content

        # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
        s = smtplib.SMTP_SSL("smtp.gmail.com",465)
        try:
            s.login(self.auth_email, self.auth_email_password)
            s.sendmail(self.auth_email, adminEmail, message)
        except:
            print "Error can not login to server"
            
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

