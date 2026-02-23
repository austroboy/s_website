import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from tenants.models import Tenant, Domain
from content.models import HomepageSection
from cache.models import CachedProgram, CachedNews, CachedEvent, CachedNotice, CachedAlbum
from branding.models import ColorPalette, FontPair, BrandAssets
from navigation.models import Menu, MenuItem

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
                        'primary': '#1D4ED8',
                        'secondary': '#06B6D4',
                        'accent': '#F59E0B',
                        'surface': '#FFFFFF',
                        'surface_alt': '#EFF6FF',
                        'footer_bg': '#1E293B',
                        'footer_text': '#F1F5F9',
                        'border': '#BFDBFE',
                        'text': '#1E293B',
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
                section_type='cta',
                defaults={
                    'title': 'Ready to Excel? Join Us Today',
                    'subtitle': 'Our admissions team is here to help you navigate the process.',
                    'order': 9,
                    'config': {
                        'primary_text': 'Get Started',
                        'primary_link': '/admissions/apply/',
                        'secondary_text': 'Speak to Counseling',
                        'secondary_link': '/contact/counseling/'
                    }
                }
            )

            # 3. Dummy Programs
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

            # 4. Dummy News
            for i in range(1, 4):
                CachedNews.objects.get_or_create(
                    tenant=tenant,
                    sms_id=f'{school_info["sms_tenant_id"]}_news_{i}',
                    defaults={
                        'title': f"{school_info['name']} News Update {i}",
                        'slug': f"news-update-{i}",
                        'summary': f"This is a short summary for news item {i}.",
                        'content': 'Full content...',
                        'featured_image': f'https://picsum.photos/seed/{school_info["subdomain"]}news{i}/600/400',
                        'is_published': True,
                        'created_at': timezone.now() - timedelta(days=i),
                        'updated_at': timezone.now() - timedelta(days=i)
                    }
                )

            # 5. Dummy Events
            for i in range(1, 4):
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

            # 6. Dummy Notices
            for i in range(1, 4):
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
