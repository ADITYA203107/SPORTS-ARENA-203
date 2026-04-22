from django.core.management.base import BaseCommand
from apps.academies.models import Academy

class Command(BaseCommand):
    help = 'Create dummy academy data for testing'

    def handle(self, *args, **options):
        # Clear existing academies
        Academy.objects.all().delete()
        
        academies_data = [
            {
                'name': 'Elite Badminton Academy',
                'sport': 'badminton',
                'location': '123 Sports Complex, MG Road',
                'city': 'Mumbai',
                'fees': 3000.00,
                'coach_name': 'Rahul Sharma',
                'coach_experience': 12,
                'description': 'Professional badminton training with world-class facilities. We offer coaching for beginners to advanced players with personalized attention.',
                'phone': '+91 9876543210',
                'email': 'info@elitebadminton.com',
                'website': 'https://elitebadminton.com'
            },
            {
                'name': 'AquaSwim Swimming School',
                'sport': 'swimming',
                'location': '456 Aquatic Center, Bandra',
                'city': 'Mumbai',
                'fees': 2500.00,
                'coach_name': 'Priya Patel',
                'coach_experience': 8,
                'description': 'Learn swimming from certified coaches in our Olympic-size pool. We offer classes for all age groups and skill levels.',
                'phone': '+91 9876543211',
                'email': 'learn@aquaswim.com',
                'website': 'https://aquaswim.com'
            },
            {
                'name': 'Champions Tennis Club',
                'sport': 'tennis',
                'location': '789 Tennis Court, Juhu',
                'city': 'Mumbai',
                'fees': 4000.00,
                'coach_name': 'Vikram Singh',
                'coach_experience': 15,
                'description': 'Premier tennis coaching with ITF certified coaches. State-of-the-art courts and professional training programs.',
                'phone': '+91 9876543212',
                'email': 'info@championstennis.com',
                'website': 'https://championstennis.com'
            },
            {
                'name': 'United Football Academy',
                'sport': 'football',
                'location': '321 Football Ground, Andheri',
                'city': 'Mumbai',
                'fees': 2000.00,
                'coach_name': 'James Rodriguez',
                'coach_experience': 10,
                'description': 'Professional football training focusing on technical skills, teamwork, and physical fitness. Join our academy to become a football champion.',
                'phone': '+91 9876543213',
                'email': 'join@unitedfootball.com',
                'website': 'https://unitedfootball.com'
            },
            {
                'name': 'Master Cricket Academy',
                'sport': 'cricket',
                'location': '654 Cricket Pitch, Shivaji Park',
                'city': 'Mumbai',
                'fees': 3500.00,
                'coach_name': 'Anil Kumar',
                'coach_experience': 20,
                'description': 'Learn cricket from former Ranji players. We provide comprehensive coaching covering batting, bowling, and fielding techniques.',
                'phone': '+91 9876543214',
                'email': 'info@mastercricket.com',
                'website': 'https://mastercricket.com'
            },
            {
                'name': 'Hoops Basketball Academy',
                'sport': 'basketball',
                'location': '987 Basketball Court, Worli',
                'city': 'Mumbai',
                'fees': 2800.00,
                'coach_name': 'Michael Johnson',
                'coach_experience': 7,
                'description': 'Professional basketball training with focus on fundamentals, strategy, and physical conditioning. Join us to elevate your game.',
                'phone': '+91 9876543215',
                'email': 'hoops@basketballacademy.com',
                'website': 'https://hoopsbasketball.com'
            },
            {
                'name': 'Smash Volleyball Club',
                'sport': 'volleyball',
                'location': '147 Sports Arena, Marine Lines',
                'city': 'Mumbai',
                'fees': 2200.00,
                'coach_name': 'Sarah Williams',
                'coach_experience': 9,
                'description': 'Professional volleyball coaching for all levels. We focus on technique, teamwork, and competitive spirit.',
                'phone': '+91 9876543216',
                'email': 'info@smashvolleyball.com',
                'website': 'https://smashvolleyball.com'
            },
            {
                'name': 'Ping Pong Masters',
                'sport': 'table_tennis',
                'location': '258 Indoor Sports, Powai',
                'city': 'Mumbai',
                'fees': 1800.00,
                'coach_name': 'David Lee',
                'coach_experience': 11,
                'description': 'Table tennis coaching with international standard equipment. Learn from state-level champions and improve your game.',
                'phone': '+91 9876543217',
                'email': 'learn@pingpongmasters.com',
                'website': 'https://pingpongmasters.com'
            },
            {
                'name': 'Strategic Chess Academy',
                'sport': 'chess',
                'location': '369 Learning Center, Dadar',
                'city': 'Mumbai',
                'fees': 1500.00,
                'coach_name': 'Rajesh Gupta',
                'coach_experience': 25,
                'description': 'Learn chess from FIDE-rated coaches. We offer courses for beginners to advanced players with focus on strategy and tactics.',
                'phone': '+91 9876543218',
                'email': 'info@strategicchess.com',
                'website': 'https://strategicchess.com'
            },
            {
                'name': 'Peaceful Yoga Studio',
                'sport': 'yoga',
                'location': '741 Wellness Center, Goregaon',
                'city': 'Mumbai',
                'fees': 1200.00,
                'coach_name': 'Anita Desai',
                'coach_experience': 14,
                'description': 'Traditional yoga and meditation classes for all levels. Find your inner peace and improve your physical and mental well-being.',
                'phone': '+91 9876543219',
                'email': 'info@peacefulyoga.com',
                'website': 'https://peacefulyoga.com'
            },
            {
                'name': 'Delhi Badminton Club',
                'sport': 'badminton',
                'location': '111 Sports Complex, Connaught Place',
                'city': 'Delhi',
                'fees': 2800.00,
                'coach_name': 'Amit Verma',
                'coach_experience': 10,
                'description': 'Premium badminton coaching in the heart of Delhi. We offer world-class facilities and expert coaching.',
                'phone': '+91 9876543220',
                'email': 'info@delhibadminton.com',
                'website': 'https://delhibadminton.com'
            },
            {
                'name': 'Bangalore Swimming Institute',
                'sport': 'swimming',
                'location': '222 Aquatic Center, Indiranagar',
                'city': 'Bangalore',
                'fees': 2700.00,
                'coach_name': 'Nandini Reddy',
                'coach_experience': 6,
                'description': 'Modern swimming facility with heated pools and certified instructors. Learn swimming in a safe and comfortable environment.',
                'phone': '+91 9876543221',
                'email': 'learn@bangaloreswimming.com',
                'website': 'https://bangaloreswimming.com'
            }
        ]
        
        created_count = 0
        for academy_data in academies_data:
            academy = Academy.objects.create(**academy_data)
            created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} dummy academies!')
        )
