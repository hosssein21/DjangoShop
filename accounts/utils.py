from threading import Thread
from django.core.mail import send_mail


class EmailThread(Thread):
    
    def __init__(self,email_obj):
        Thread.__init__(self)
        self.email_obj = email_obj
        
    def run(self):
        self.email_obj.send()
        
class TemplateEmailThread(Thread):
    def __init__(self, subject, html_message, plain_message, from_email, recipient_list):
        self.subject = subject
        self.html_message = html_message
        self.plain_message = plain_message
        self.from_email = from_email
        self.recipient_list = recipient_list
        Thread.__init__(self)
    
    def run(self):
        send_mail(
            subject=self.subject,
            message=self.plain_message,
            from_email=self.from_email,
            recipient_list=self.recipient_list,
            html_message=self.html_message,
        )
        
        