"""
Management command to populate sample FAQ data for DAY 4
Run: python manage.py populate_faq
"""
from django.core.management.base import BaseCommand
from apps.core.models import FAQCategory, FAQ


class Command(BaseCommand):
    help = 'Populate sample FAQ data for SPORTS ARENA'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating FAQ data...')

        # Clear existing data
        FAQ.objects.all().delete()
        FAQCategory.objects.all().delete()

        # Create Categories
        learner = FAQCategory.objects.create(
            name="Learner FAQs",
            slug="learner",
            category_type="learner",
            icon="🎓",
            order=1
        )

        owner = FAQCategory.objects.create(
            name="Academy Owner FAQs",
            slug="owner",
            category_type="owner",
            icon="🏢",
            order=2
        )

        technical = FAQCategory.objects.create(
            name="Technical FAQs",
            slug="technical",
            category_type="technical",
            icon="⚙️",
            order=3
        )

        # Learner FAQs
        learner_faqs = [
            {
                "question": "How do I compare academies?",
                "answer": "Use the Compare feature on the Explore page. Select up to 3 academies by clicking the 'Compare' button on each academy card. Then click 'View Comparison' to see a side-by-side analysis of facilities, coaches, pricing, ratings, and more.",
                "is_popular": True,
                "order": 1
            },
            {
                "question": "How to chat with academy owners?",
                "answer": "Navigate to any academy detail page and click the 'Chat Now' button. You must be logged in as a learner to access the chat feature. The academy owner will receive a notification and can respond to your messages.",
                "is_popular": True,
                "order": 2
            },
            {
                "question": "How do recommendations work?",
                "answer": "Our smart recommendation system analyzes your activity, saved academies, and preferences to suggest academies that match your interests. The more you interact with the platform, the better the recommendations become.",
                "is_popular": True,
                "order": 3
            },
            {
                "question": "How to save academies?",
                "answer": "Click the heart icon on any academy card to save it to your favorites. You can view all saved academies from your dashboard under 'Saved Academies'.",
                "is_popular": False,
                "order": 4
            },
            {
                "question": "How to book a session?",
                "answer": "Visit the academy detail page, click 'Book Now', select your preferred date and time, add any special requirements, and submit. You'll receive a confirmation email and notification once the academy approves your booking.",
                "is_popular": True,
                "order": 5
            },
            {
                "question": "Can I cancel a booking?",
                "answer": "Yes, you can cancel bookings from your dashboard under 'My Bookings'. Cancellation policies may vary by academy. Contact the academy directly for specific cancellation terms.",
                "is_popular": False,
                "order": 6
            },
        ]

        # Owner FAQs
        owner_faqs = [
            {
                "question": "How to upload coaches?",
                "answer": "Go to your Dashboard → Manage Coaches → Add New Coach. Fill in coach details including name, specialization, experience, certifications, and upload a professional photo. You can add multiple coaches to showcase your team.",
                "is_popular": True,
                "order": 1
            },
            {
                "question": "How to update academy profile?",
                "answer": "Navigate to Dashboard → Manage Academy. Here you can update your academy name, description, facilities, sports offered, pricing, contact information, and upload photos. Changes are reflected immediately on your public profile.",
                "is_popular": True,
                "order": 2
            },
            {
                "question": "How to manage bookings?",
                "answer": "Access Dashboard → View Bookings to see all incoming booking requests. You can approve or reject bookings, view learner details, and communicate directly through the chat system. Learners receive email notifications of your decisions.",
                "is_popular": True,
                "order": 3
            },
            {
                "question": "How to respond to users?",
                "answer": "When learners send you messages, you'll receive a notification. Click on the notification or go to Chat Inbox to view and respond to messages. Quick responses improve your academy's reputation.",
                "is_popular": False,
                "order": 4
            },
            {
                "question": "How to upload academy photos?",
                "answer": "Go to Dashboard → Upload Photos. You can upload multiple high-quality images showcasing your facilities, training sessions, equipment, and achievements. Good photos attract more learners.",
                "is_popular": False,
                "order": 5
            },
            {
                "question": "How to improve my academy ranking?",
                "answer": "Rankings are based on ratings, response time, booking completion rate, and profile completeness. Maintain high-quality service, respond quickly to inquiries, complete your profile, and encourage satisfied learners to leave reviews.",
                "is_popular": True,
                "order": 6
            },
        ]

        # Technical FAQs
        technical_faqs = [
            {
                "question": "How to reset my password?",
                "answer": "Click 'Forgot Password' on the login page. Enter your registered email address and we'll send you a password reset link. Follow the link to create a new password. If you don't receive the email, check your spam folder.",
                "is_popular": True,
                "order": 1
            },
            {
                "question": "Account recovery process",
                "answer": "If you can't access your account, use the 'Forgot Password' feature. If you no longer have access to your email, contact our support team at support@sportsarena.com with your account details for manual verification.",
                "is_popular": False,
                "order": 2
            },
            {
                "question": "Why am I not receiving notifications?",
                "answer": "Check your notification settings in your profile. Ensure your email address is verified. Check your spam/junk folder. If the issue persists, create a support ticket and our team will investigate.",
                "is_popular": True,
                "order": 3
            },
            {
                "question": "Email verification issue",
                "answer": "If you didn't receive the verification email, check your spam folder. You can request a new verification email from your profile settings. If the problem continues, contact support with your registered email address.",
                "is_popular": False,
                "order": 4
            },
            {
                "question": "How to change my email address?",
                "answer": "Go to Profile Settings → Account Information → Update Email. You'll need to verify the new email address before the change takes effect. For security, you may be asked to confirm your current password.",
                "is_popular": False,
                "order": 5
            },
            {
                "question": "Browser compatibility issues",
                "answer": "SPORTS ARENA works best on modern browsers: Chrome, Firefox, Safari, and Edge (latest versions). Clear your browser cache and cookies if you experience issues. Disable ad blockers if features aren't working properly.",
                "is_popular": False,
                "order": 6
            },
        ]

        # Create FAQs
        for faq_data in learner_faqs:
            FAQ.objects.create(category=learner, **faq_data)

        for faq_data in owner_faqs:
            FAQ.objects.create(category=owner, **faq_data)

        for faq_data in technical_faqs:
            FAQ.objects.create(category=technical, **faq_data)

        self.stdout.write(self.style.SUCCESS('Created {} categories'.format(FAQCategory.objects.count())))
        self.stdout.write(self.style.SUCCESS('Created {} FAQs'.format(FAQ.objects.count())))
        self.stdout.write(self.style.SUCCESS('FAQ data populated successfully!'))
