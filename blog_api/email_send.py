from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def emailsender(data):
    subject = 'Welcome to Our Service'
    message = render_to_string('emails/welcome_email.html', {
        'first_name': data['first_name'],
        'username': data['username'],
        'email': data['email'],
    })
    from_email = 'badgotidheeraj@gmail.com'
    recipient_list = [data['email']]
    
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'  # Main content is now text/html
    email.send()
