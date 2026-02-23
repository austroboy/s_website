from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain
from navigation.models import Menu, MenuItem
from content.models import Page
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seed initial navigation and functional pages for the current tenant'

    def handle(self, *args, **options):
        # 1. Ensure a default tenant exists
        tenant, created = Tenant.objects.get_or_create(
            sms_tenant_id='school_1',
            defaults={
                'name': 'Global Tech Academy',
                'api_base_url': 'http://sms.global.example.com',
                'api_key': 'key',
                'api_secret': 'secret',
                'contact_email': 'info@sms.global.example.com',
                'contact_phone': '+1 234 567 890',
                'address': 'Global Tech Campus, Innovation City'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created tenant: {tenant.name}'))
        
        # Ensure domain exists (handle IntegrityError if already exists)
        domain_name = 'global.localhost'  # Using localhost subdomain for local testing
        domain_obj = Domain.objects.filter(domain=domain_name).first()
        if not domain_obj:
            Domain.objects.create(domain=domain_name, tenant=tenant, is_primary=True)
        elif domain_obj.tenant != tenant:
            self.stdout.write(self.style.WARNING(f"Domain '{domain_name}' is already assigned to tenant: {domain_obj.tenant.name}"))

        # 2. Create Header Menu
        header_menu, _ = Menu.objects.get_or_create(tenant=tenant, slug='header', defaults={'name': 'Header Menu'})
        
        # 3. Create Functional Pages
        pages_data = [
            ('About Us', 'A brief history and mission of our school.'),
            ('Admission Requirements', 'Detailed information on what is needed to apply.'),
            ('Fee Structure', 'A breakdown of tuition and other fees.'),
            ('Privacy Policy', 'Our policy on data protection.'),
            ('Terms of Service', 'Terms for using our website.'),
        ]

        pages = {}
        for title, dummy_content in pages_data:
            slug = slugify(title)
            page, created = Page.objects.get_or_create(
                tenant=tenant,
                slug=slug,
                defaults={
                    'title': title,
                    'content': f'<h2>{title}</h2><p>{dummy_content}</p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>',
                    'published': True
                }
            )
            pages[slug] = page
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created page: {title}'))

        # 4. Create Header Menu Items
        header_items = [
            ('Home', '/', 1),
            ('About', pages['about-us'].slug, 2, True),
            ('Academics', '/academics/', 3),
            ('Admissions', '/admissions/', 4),
            ('Achievements', '/achievements/', 5),
            ('Documents', '/documents/', 6),
            ('News', '/news/', 7),
            ('Contact', '/contact/', 8),
        ]

        for title, url_or_slug, order, *is_page in header_items:
            item_defaults = {'order': order, 'is_active': True}
            if is_page:
                item_defaults['page'] = pages[url_or_slug]
                item_defaults['url'] = f'/{url_or_slug}/'
            else:
                item_defaults['url'] = url_or_slug

            MenuItem.objects.update_or_create(
                menu=header_menu,
                title=title,
                defaults=item_defaults
            )

        # Add Academics Dropdown Children
        academics_parent = MenuItem.objects.get(menu=header_menu, title='Academics')
        academics_children = [
            ('All Programs', '/academics/', 1),
            ('Faculty/Staff', '/staff/', 2),
            ('Academic Calendar', '/events/', 3),
        ]
        for title, url, order in academics_children:
            MenuItem.objects.update_or_create(
                menu=header_menu,
                parent=academics_parent,
                title=title,
                defaults={'url': url, 'order': order}
            )

        # Add Admissions Dropdown Children
        admissions_parent = MenuItem.objects.get(menu=header_menu, title='Admissions')
        admissions_children = [
            ('Process Overview', '/admissions/', 1),
            ('Admission Requirements', f"/{pages['admission-requirements'].slug}/", 2, pages['admission-requirements']),
            ('Fee Structure', f"/{pages['fee-structure'].slug}/", 3, pages['fee-structure']),
            ('Online Inquiry', '/contact/admissions/', 4),
        ]
        for title, url, order, *page in admissions_children:
            defaults = {'url': url, 'order': order}
            if page:
                defaults['page'] = page[0]
            MenuItem.objects.update_or_create(
                menu=header_menu,
                parent=admissions_parent,
                title=title,
                defaults=defaults
            )

        # 5. Create Footer Menu
        footer_menu, _ = Menu.objects.get_or_create(tenant=tenant, slug='footer', defaults={'name': 'Footer Menu'})
        footer_items = [
            ('Home', '/', 1),
            ('About Us', f"/{pages['about-us'].slug}/", 2, pages['about-us']),
            ('Achievements', '/achievements/', 3),
            ('School Documents', '/documents/', 4),
            ('Privacy Policy', f"/{pages['privacy-policy'].slug}/", 5, pages['privacy-policy']),
        ]
        for title, url, order, *page in footer_items:
            defaults = {'url': url, 'order': order}
            if page:
                defaults['page'] = page[0]
            MenuItem.objects.update_or_create(
                menu=footer_menu,
                title=title,
                defaults=defaults
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded navigation and functional pages.'))
