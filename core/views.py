from django.views.generic import TemplateView, ListView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Service, ContactMessage
from blog.models import Post
from .forms import ContactForm
from .gmail_oauth import get_gmail_service, create_message
import base64
from email.mime.text import MIMEText
import logging
import json

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)[:6]
        context['latest_posts'] = Post.objects.filter(published=True)[:3]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True)
        return context

class ServiceListView(ListView):
    model = Service
    template_name = 'core/services.html'
    context_object_name = 'services'
    queryset = Service.objects.filter(is_active=True)

class ContactView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        print("ContactView form_valid called")
        logger.info("Processing contact form submission")
        
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        
        print(f"Form data - Name: {name}, Email: {email}, Subject: {subject}")
        logger.debug(f"Form data - Name: {name}, Email: {email}, Subject: {subject}")
        
        try:
            # Get Gmail credentials
            try:
                print("Getting Gmail credentials")
                logger.debug("Getting Gmail credentials")
                creds = get_gmail_service()
                print("Successfully got Gmail credentials")
                logger.info("Successfully got Gmail credentials")
            except Exception as e:
                print(f"Gmail credentials error: {str(e)}")
                logger.error(f"Gmail credentials error: {str(e)}")
                messages.error(self.request, str(e))
                return self.form_invalid(form)
            
            # Prepare email context
            context = {
                'name': name,
                'subject': subject,
                'message': message
            }
            
            # Create HTML and plain text versions
            html_message = render_to_string('emails/contact_confirmation.html', context)
            plain_message = strip_tags(html_message)
            
            print("Creating email messages")
            logger.debug("Creating email messages")
            
            # Create message for user
            user_message = create_message(
                settings.DEFAULT_FROM_EMAIL,
                email,
                'Thank You for Contacting AceAttorn Legal Solutions',
                plain_message,
                html_message
            )
            
            # Create message for admin
            admin_message = create_message(
                settings.DEFAULT_FROM_EMAIL,
                settings.ADMIN_EMAIL,
                'New Contact Form Submission',
                f"New contact form submission:\nName: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
            )
            
            print("Preparing to send emails")
            logger.debug("Preparing to send emails")
            
            # Send emails using Gmail API
            import google.auth.transport.requests
            import google.oauth2.credentials
            import requests
            
            request_obj = google.auth.transport.requests.Request()
            creds.refresh(request_obj)
            
            headers = {
                'Authorization': f'Bearer {creds.token}',
                'Content-Type': 'application/json',
            }
            
            print("Token:", creds.token)
            print("Headers:", headers)
            
            success_count = 0
            # Send both emails
            for msg_type, msg in [('confirmation', user_message), ('notification', admin_message)]:
                try:
                    print(f"Attempting to send {msg_type} email")
                    logger.debug(f"Attempting to send {msg_type} email")
                    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
                    
                    url = 'https://www.googleapis.com/gmail/v1/users/me/messages/send'
                    data = {'raw': raw}
                    
                    print(f"Making API request to: {url}")
                    print(f"Request data: {json.dumps(data)}")
                    
                    response = requests.post(
                        url,
                        headers=headers,
                        json=data
                    )
                    
                    print(f"Response status: {response.status_code}")
                    print(f"Response content: {response.text}")
                    
                    response.raise_for_status()
                    message_id = response.json().get('id')
                    print(f"Successfully sent {msg_type} email. Message ID: {message_id}")
                    logger.info(f"Successfully sent {msg_type} email. Message ID: {message_id}")
                    success_count += 1
                except Exception as e:
                    print(f"Failed to send {msg_type} email: {str(e)}")
                    logger.error(f"Failed to send {msg_type} email: {str(e)}", exc_info=True)
                    if msg_type == 'confirmation':
                        messages.warning(self.request, 'Your message was received, but we could not send you a confirmation email.')
                    else:
                        messages.warning(self.request, 'Your message was received, but our notification system encountered an error.')
            
            if success_count == 2:
                print("Both emails sent successfully")
                logger.info("Both emails sent successfully")
                messages.success(self.request, 'Thank you for your message. We will get back to you soon!')
            elif success_count == 0:
                print("Failed to send both emails")
                logger.error("Failed to send both emails")
                messages.error(self.request, 'There was an error sending your message. Please try again later.')
            
            # Save the contact message to database
            try:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    subject=subject,
                    message=message,
                    sent_successfully=success_count > 0
                )
                print("Contact message saved to database")
                logger.info("Contact message saved to database")
            except Exception as e:
                print(f"Failed to save contact message to database: {str(e)}")
                logger.error(f"Failed to save contact message to database: {str(e)}", exc_info=True)
            
            return super().form_valid(form)
            
        except Exception as e:
            print(f"Error in contact form: {str(e)}")
            logger.error(f"Error in contact form: {str(e)}", exc_info=True)
            messages.error(self.request, f'There was an error processing your message: {str(e)}')
            return self.form_invalid(form)
            
    def form_invalid(self, form):
        print("Form is invalid")
        print("Form errors:", form.errors)
        messages.error(self.request, 'Please correct the errors in the form.')
        return super().form_invalid(form)
