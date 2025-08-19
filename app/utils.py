



def send_contact_email(request, *args, **kwargs):
    email = kwargs.get("email")
    subject = kwargs.get("subject")
    message = kwargs.get("message")

   
