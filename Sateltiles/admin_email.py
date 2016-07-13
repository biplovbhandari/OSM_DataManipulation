import smtplib
import settings as setting
import wx
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.MIMEBase import MIMEBase
from email import Encoders

class Email:
    def sendComfirmation(self, adminEmail, adminFirstName, adminLastName, userFN, userLN):
        adminName = adminFirstName + " " + adminLastName
        msg = MIMEMultipart()
        msg["Subject"] = setting.subject_for_confirmation 
        msg["From"] = setting.from_sender
        msg["To"] = adminName
        massage = """User name: \'%s %s\' would like to join our Sateltiles community.
                    Please check in the program for confirmation.""" %(userFN, userLN)
        part1 = MIMEText(massage, "plain")
        msg.attach(part1)
        # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
        try:
            s = smtplib.SMTP_SSL("smtp.gmail.com",465)
            s.login(setting.auth_email, setting.auth_email_password)
            s.sendmail(setting.auth_email, adminEmail, msg.as_string())
        except:
            wx.MessageBox("Connection error", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            s.quit()

    def sendPassword(self, userEmail, userFirstName, userLastName, user_password):
        SUBJECT = "Your Sateltiles password"
        userName = userFirstName + " " + userLastName
        msg = MIMEMultipart()
        msg["Subject"] = setting.subject_for_getPassword 
        msg["From"] = setting.from_sender
        msg["To"] = userName
        massage = "Your Sateltiles password is \'%s\'" %(user_password)
        part1 = MIMEText(massage, "plain")
        msg.attach(part1)
        # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
        s = smtplib.SMTP_SSL("smtp.gmail.com",465)
        try:
            s.login(setting.auth_email, setting.auth_email_password)
            s.sendmail(setting.auth_email, userEmail, msg.as_string())
        except:
            wx.MessageBox("Connection error", "Error", 
            wx.OK | wx.ICON_ERROR)
        finally:
            s.quit()
