import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from tenants.models import Tenant, Domain
from content.models import HomepageSection
from cache.models import CachedProgram, CachedNews, CachedEvent, CachedNotice, CachedAlbum, CachedStaff
from branding.models import ColorPalette, FontPair, BrandAssets
from navigation.models import Menu, MenuItem
from achievements.models import Achievement
from admissions.models import AdmissionForm
from contact.models import ContactSubmission, AdmissionInquiry

class Command(BaseCommand):
    help = 'Seeds the database with dummy data for multiple schools/tenants'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting multi-tenant database seeding...")

        schools_to_seed = [
            {
                'sms_tenant_id': 'school_1',
                'name': 'Global Tech Academy',
                'subdomain': 'global',
                'domains': ['global.localhost', 'localhost', '127.0.0.1'],
                'primary_color': 'blue',
                'programs': ['Computer Science', 'Data Analytics', 'Robotics', 'Cybersecurity', 'Artificial Intelligence', 'Software Engineering', 'Information Systems', 'Digital Forensics']
            },
            {
                'sms_tenant_id': 'school_2',
                'name': 'National Science College',
                'subdomain': 'national',
                'domains': ['national.localhost'],
                'primary_color': 'green',
                'programs': ['Biology', 'Physics', 'Chemistry', 'Mathematics', 'Environmental Science', 'Astronomy', 'Geology', 'Statistics']
            }
        ]

        for school_info in schools_to_seed:
            self.stdout.write(f"Seeding Data for: {school_info['name']}...")
            
            # 1. Create Tenant
            tenant, created = Tenant.objects.get_or_create(
                sms_tenant_id=school_info['sms_tenant_id'],
                defaults={
                    'name': school_info['name'],
                    'subdomain': school_info['subdomain'],
                    'api_base_url': f"http://sms.{school_info['subdomain']}.example.com",
                    'api_key': 'dummy',
                    'api_secret': 'dummy',
                    'contact_email': f"info@{school_info['subdomain']}.example.com",
                    'contact_phone': '+1 (555) 000-0000',
                    'address': f"100 {school_info['name']} Boulevard, Tech City"
                }
            )
            
            # Domains (No ports! Middleware strips port before checking)
            for idx, domain_str in enumerate(school_info['domains']):
                Domain.objects.get_or_create(
                    domain=domain_str,
                    tenant=tenant,
                    defaults={
                        'is_primary': (idx == 0)
                    }
                )

            # 1.5. Brand Colors (New specialized fields)
            if school_info['subdomain'] == 'global':
                ColorPalette.objects.get_or_create(
                    tenant=tenant,
                    defaults={
                        'primary': '#0051FF',
                        'primary_dark': '#003ACC',
                        'primary_light': '#3B82F6',
                        'primary_glow': 'rgba(0, 81, 255, 0.35)',
                        'secondary': '#0F1D40',
                        'secondary_light': '#1A2D5A',
                        'accent': '#00D4FF',
                        'surface': '#F8FAFD',
                        'surface_alt': '#EFF4FB',
                        'footer_bg': '#1E293B',
                        'footer_text': '#F1F5F9',
                        'border': '#BFDBFE',
                        'text': '#1A1A2E',
                        'text_muted': '#64748B'
                    }
                )
            else:
                ColorPalette.objects.get_or_create(
                    tenant=tenant,
                    defaults={
                        'primary': '#059669',
                        'secondary': '#10B981',
                        'accent': '#F59E0B',
                        'surface': '#FFFFFF',
                        'surface_alt': '#ECFDF5',
                        'footer_bg': '#064E3B',
                        'footer_text': '#D1FAE5',
                        'border': '#A7F3D0',
                        'text': '#064E3B',
                        'text_muted': '#065F46'
                    }
                )

            # 2. Homepage Sections
            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='hero',
                defaults={
                    'title': f"Welcome to {school_info['name']}",
                    'subtitle': f"Discover your potential at {school_info['name']}. Excellence in every endeavor.",
                    'order': 1,
                    'config': {
                        'background_image': 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80',
                        'cta_primary_text': 'Apply Now',
                        'cta_primary_link': '/admissions/',
                        'cta_secondary_text': 'Learn More',
                        'cta_secondary_link': '/about/'
                    }
                }
            )
            
            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='features',
                defaults={
                    'title': 'Our Academic Programs',
                    'subtitle': 'Meticulously designed curriculums to inspire and challenge every student.',
                    'order': 2
                }
            )

            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='stats',
                defaults={
                    'title': 'Our Impact',
                    'order': 3,
                    'config': {
                        'students': 2500 if school_info['subdomain'] == 'global' else 1200,
                        'teachers': 200 if school_info['subdomain'] == 'global' else 90,
                        'programs': 45 if school_info['subdomain'] == 'global' else 20,
                        'years': 50 if school_info['subdomain'] == 'global' else 15
                    }
                }
            )
            
            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='news',
                defaults={
                    'title': 'Latest Updates',
                    'subtitle': 'Stay informed about what is happening on campus.',
                    'order': 4
                }
            )
            
            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='events',
                defaults={
                    'title': 'Upcoming Events',
                    'order': 5
                }
            )
            
            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='notices',
                defaults={
                    'title': 'Important Notices',
                    'order': 6
                }
            )

            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='gallery',
                defaults={
                    'title': 'Campus Life in Pictures',
                    'subtitle': 'A glimpse into our vibrant and dynamic student community.',
                    'order': 7
                }
            )

            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='achievements',
                defaults={
                    'title': 'Our Notable Achievements',
                    'subtitle': 'Celebrating the milestones, awards, and recognitions that define our commitment to excellence.',
                    'order': 8
                }
            )

            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='staff',
                defaults={
                    'title': 'Exceptional Faculty & Staff',
                    'subtitle': 'Meet the inspiring educators and professionals who are passionate about shaping the future.',
                    'order': 9
                }
            )

            HomepageSection.objects.get_or_create(
                tenant=tenant,
                section_type='cta',
                defaults={
                    'title': 'Ready to Excel? Join Us Today',
                    'subtitle': 'Our admissions team is here to help you navigate the process.',
                    'order': 10,
                    'config': {
                        'primary_text': 'Get Started',
                        'primary_link': '/admissions/apply/',
                        'secondary_text': 'Speak to Counseling',
                        'secondary_link': '/contact/counseling/'
                    }
                }
            )


            # 3. Dummy Programs (8 items)
            for idx, p_name in enumerate(school_info['programs']):
                CachedProgram.objects.get_or_create(
                    tenant=tenant,
                    sms_id=f'{school_info["sms_tenant_id"]}_prog_{idx+1}',
                    defaults={
                        'name': p_name,
                        'description': 'Advanced curriculum focusing on modern challenges.',
                        'icon': 'book',
                        'order': idx,
                        'is_published': True
                    }
                )

            # Image URLs for News and Events
            seed_images = [
                'https://plus.unsplash.com/premium_vector-1682303174219-9018338d4b5d',
                'https://plus.unsplash.com/premium_vector-1711987353813-68a5bdb6f207',
                'https://plus.unsplash.com/premium_vector-1720891748699-e91b3606f222',
                'https://plus.unsplash.com/premium_vector-1720602864608-447c2e3323e9',
                'https://plus.unsplash.com/premium_vector-1731471747401-fae8e5ef2021',
                'https://plus.unsplash.com/premium_vector-1721762658788-8af51eb930a',
                'https://plus.unsplash.com/premium_vector-1721748240192-9ac4be133756',
                'https://plus.unsplash.com/premium_vector-1722124599095-142c3f7eee93'
            ]

            # 4. Dummy News (8 items)
            num_items = 8 if school_info['subdomain'] == 'global' else 3
            for i in range(1, num_items + 1):
                img_url = seed_images[i-1] if school_info['subdomain'] == 'global' else f'https://picsum.photos/seed/{school_info["subdomain"]}news{i}/600/400'
                CachedNews.objects.get_or_create(
                    tenant=tenant,
                    sms_id=f'{school_info["sms_tenant_id"]}_news_{i}',
                    defaults={
                        'title': f"{school_info['name']} News Update {i}",
                        'slug': f"news-update-{i}",
                        'summary': f"This is a short summary for news item {i}.",
                        'content': 'Full content...',
                        'featured_image': img_url,
                        'is_published': True,
                        'created_at': timezone.now() - timedelta(days=i),
                        'updated_at': timezone.now() - timedelta(days=i)
                    }
                )

            # 5. Dummy Events (8 items)
            for i in range(1, num_items + 1):
                img_url = seed_images[i-1] if school_info['subdomain'] == 'global' else f'https://picsum.photos/seed/{school_info["subdomain"]}event{i}/600/400'
                CachedEvent.objects.get_or_create(
                    tenant=tenant,
                    sms_id=f'{school_info["sms_tenant_id"]}_event_{i}',
                    defaults={
                        'title': f"{school_info['name']} Event {i}",
                        'slug': f"event-{i}",
                        'summary': 'Join us for this amazing school event.',
                        'content': 'Full event details...',
                        'start_date': timezone.now() + timedelta(days=i*5),
                        'end_date': timezone.now() + timedelta(days=i*5, hours=2),
                        'venue': 'Main Auditorium',
                        'is_published': True,
                        'created_at': timezone.now(),
                        'updated_at': timezone.now()
                    }
                )

            # 6. Dummy Notices (8 items)
            for i in range(1, num_items + 1):
                CachedNotice.objects.get_or_create(
                    tenant=tenant,
                    sms_id=f'{school_info["sms_tenant_id"]}_notice_{i}',
                    defaults={
                        'title': f"Notice #{i} for {school_info['name']}",
                        'slug': f"notice-{i}",
                        'summary': f"Please read this important notice regarding school policy #{i}.",
                        'content': 'Notice details...',
                        'is_published': True,
                        'expiry_date': timezone.now() + timedelta(days=30),
                        'created_at': timezone.now(),
                        'updated_at': timezone.now()
                    }
                )
                
            if school_info['subdomain'] == 'global':
                # 7a. Dummy Achievements (8 items)
                for i in range(1, 9):
                    Achievement.objects.get_or_create(
                        tenant=tenant,
                        title=f"{school_info['name']} Achievement {i}",
                        defaults={
                            'description': 'Awarded for excellence in academics and sports.',
                            'date': timezone.now().date() - timedelta(days=i*30),
                            'is_published': True,
                            'order': i
                        }
                    )
                
                # 7b. Admission Forms (Dummy files)
                for i in range(1, 9):
                    AdmissionForm.objects.get_or_create(
                        tenant=tenant,
                        title=f"Admission Form {i}",
                        defaults={
                            'description': f'Sample admission form {i} description.',
                            'file': f'admission_forms/dummy_form_{i}.pdf',
                            'order': i,
                            'is_published': True
                        }
                    )
                
                # 7c. Admission Enquiries
                for i in range(1, 9):
                    AdmissionInquiry.objects.get_or_create(
                        tenant=tenant,
                        email=f"student{i}@example.com",
                        defaults={
                            'full_name': f"Prospective Student {i}",
                            'phone': f"+155512345{i:02d}",
                            'program_of_interest': school_info['programs'][i-1],
                            'grade_level': 'Undergraduate',
                            'message': 'I would like to know more about this program.'
                        }
                    )
                
                # 7d. Staff
                for i in range(1, 9):
                    CachedStaff.objects.get_or_create(
                        tenant=tenant,
                        sms_id=f'{school_info["sms_tenant_id"]}_staff_{i}',
                        defaults={
                            'name': f"Dr. Staff Member {i}",
                            'designation': 'Professor',
                            'department': school_info['programs'][i-1],
                            'bio': 'Experienced professor with a passion for teaching.',
                            'photo': f'https://i.pravatar.cc/150?u={i}',
                            'email': f"staff{i}@global.example.com",
                            'phone': f"+155598765{i:02d}",
                            'order': i,
                            'is_published': True
                        }
                    )
                
                # 7e. Contact Submissions
                for i in range(1, 9):
                    ContactSubmission.objects.get_or_create(
                        tenant=tenant,
                        email=f"contact{i}@example.com",
                        defaults={
                            'name': f"Contact Person {i}",
                            'phone': f"+155545678{i:02d}",
                            'subject': f"General Inquiry {i}",
                            'message': 'Please send me more information about the school.',
                            'ip_address': '127.0.0.1'
                        }
                    )

            # 7. Dummy Gallery Albums
            for i in range(1, 9):
                CachedAlbum.objects.get_or_create(
                    tenant=tenant,
                    sms_id=f'{school_info["sms_tenant_id"]}_album_{i}',
                    defaults={
                        'title': f"Gallery Activity {i}",
                        'description': 'Photos from our recent event.',
                        'cover_image': f'https://picsum.photos/seed/{school_info["subdomain"]}album{i}/600/600',
                        'is_published': True,
                        'created_at': timezone.now()
                    }
                )

            # 8. Menus (Header & Footer)
            header_menu, _ = Menu.objects.get_or_create(tenant=tenant, name='Header Menu', slug='header')
            footer_menu, _ = Menu.objects.get_or_create(tenant=tenant, name='Footer Menu', slug='footer')

            # Header Items
            home_item, _ = MenuItem.objects.get_or_create(menu=header_menu, title='Home', url='/', parent=None, order=1)
            about_item, _ = MenuItem.objects.get_or_create(menu=header_menu, title='About', url='/about/', parent=None, order=2)
            MenuItem.objects.get_or_create(menu=header_menu, title='History', url='/about/history/', parent=about_item, order=1)
            MenuItem.objects.get_or_create(menu=header_menu, title='Leadership', url='/about/leadership/', parent=about_item, order=2)
            MenuItem.objects.get_or_create(menu=header_menu, title='Academics', url='/academics/', parent=None, order=3)
            MenuItem.objects.get_or_create(menu=header_menu, title='Admissions', url='/admissions/', parent=None, order=4)
            
            # Footer Items
            MenuItem.objects.get_or_create(menu=footer_menu, title='About Us', url='/about/', order=1)
            MenuItem.objects.get_or_create(menu=footer_menu, title='Contact', url='/contact/', order=2)
            MenuItem.objects.get_or_create(menu=footer_menu, title='Careers', url='/careers/', order=3)

        self.stdout.write(self.style.SUCCESS("Successfully seeded multi-tenant dummy data!"))
