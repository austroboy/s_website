import os
import django
from django.utils.timezone import now, timedelta
import random

# Setup Django if running as a standalone script
if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')
    django.setup()

from cache.models import CachedNews, CachedEvent, CachedNotice, CachedAlbum
from tenants.models import Tenant

def seed_global_tech():
    tenant = Tenant.objects.filter(name='Global Tech Academy').first()
    if not tenant:
        print("Global Tech Academy tenant not found.")
        return

    print(f"Seeding data for {tenant.name}...")

    # Clear existing data for this tenant to avoid duplicates if preferred, 
    # but here we'll just add or update based on sms_id
    
    # --- Seed News ---
    news_data = [
        {
            "sms_id": "news_gt_1",
            "title": "Annual Science Fair 2026 Announced",
            "slug": "annual-science-fair-2026-announced",
            "summary": "Global Tech Academy is proud to announce the upcoming Annual Science Fair, showcasing innovation and creativity.",
            "content": """
                <p>We are thrilled to announce that the <strong>Annual Science Fair 2026</strong> will take place on March 15th. This year's theme is 'Sustainable Technology for a Greener Future'.</p>
                <p>Students from all grades are encouraged to participate and present their innovative projects. There will be categories for physics, biology, chemistry, and computer science.</p>
                <p>The fair aims to foster a spirit of inquiry and scientific temper among our students. Winners will receive prestigious awards and certificates.</p>
                <ul>
                    <li>Date: March 15, 2026</li>
                    <li>Time: 9:00 AM - 4:00 PM</li>
                    <li>Venue: Main Auditorium</li>
                </ul>
                <p>Join us in celebrating the young scientists of tomorrow!</p>
            """,
            "featured_image": "https://images.unsplash.com/photo-1507413245164-6160d8298b31?q=80&w=1200&auto=format&fit=crop",
            "author_name": "Admissions Office",
            "category": "Academic"
        },
        {
            "sms_id": "news_gt_2",
            "title": "New Robotics Lab Inauguration",
            "slug": "new-robotics-lab-inauguration",
            "summary": "State-of-the-art robotics laboratory opens at Global Tech Academy to enhance STEM education.",
            "content": """
                <p>In our continuous effort to provide world-class education, Global Tech Academy has inaugurated a new, state-of-the-art <strong>Robotics and AI Lab</strong>.</p>
                <p>Equipped with the latest hardware and software, the lab will serve as a hub for students to explore the realms of automation, coding, and mechanical design.</p>
                <p>Principal Dr. Sarah Smith highlighted the importance of hands-on experience in modern technology during the opening ceremony.</p>
            """,
            "featured_image": "https://images.unsplash.com/photo-1581092334651-ddf26d9a1930?q=80&w=1200&auto=format&fit=crop",
            "author_name": "Tech Dept",
            "category": "Innovation"
        }
    ]

    for item in news_data:
        CachedNews.objects.update_or_create(
            tenant=tenant,
            sms_id=item['sms_id'],
            defaults={
                'title': item['title'],
                'slug': item['slug'],
                'summary': item['summary'],
                'content': item['content'],
                'featured_image': item['featured_image'],
                'author_name': item['author_name'],
                'category': item['category'],
                'created_at': now() - timedelta(days=random.randint(1, 10)),
                'updated_at': now(),
                'is_published': True
            }
        )

    # --- Seed Events ---
    events_data = [
        {
            "sms_id": "event_gt_1",
            "title": "Inter-School Debate Championship",
            "slug": "inter-school-debate-championship",
            "summary": "A battle of wits and eloquence featuring top schools in the region.",
            "content": "<p>Join us for the Inter-School Debate Championship where students will argue on contemporary global issues. It's a platform for honing public speaking and critical thinking skills.</p>",
            "featured_image": "https://images.unsplash.com/photo-1475721027785-f74dea327912?q=80&w=1200&auto=format&fit=crop",
            "start_date": now() + timedelta(days=5, hours=10),
            "end_date": now() + timedelta(days=5, hours=16),
            "venue": "Conference Hall A",
        },
        {
            "sms_id": "event_gt_2",
            "title": "Parent-Teacher Association Meeting",
            "slug": "pta-meeting-march",
            "summary": "Quarterly progress review and discussion on school initiatives.",
            "content": "<p>The quarterly PTA meeting is scheduled to discuss student performance and upcoming school projects. We value parental involvement in our educational journey.</p>",
            "featured_image": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?q=80&w=1200&auto=format&fit=crop",
            "start_date": now() + timedelta(days=12, hours=14),
            "end_date": now() + timedelta(days=12, hours=17),
            "venue": "School Cafeteria",
        }
    ]

    for item in events_data:
        CachedEvent.objects.update_or_create(
            tenant=tenant,
            sms_id=item['sms_id'],
            defaults={
                'title': item['title'],
                'slug': item['slug'],
                'summary': item['summary'],
                'content': item['content'],
                'featured_image': item['featured_image'],
                'start_date': item['start_date'],
                'end_date': item['end_date'],
                'venue': item['venue'],
                'created_at': now(),
                'updated_at': now(),
                'is_published': True
            }
        )

    # --- Seed Notices ---
    notices_data = [
        {
            "sms_id": "notice_gt_1",
            "title": "Admission Open for 2026-27 Session",
            "slug": "admission-open-2026-27",
            "summary": "Secure your child's future at Global Tech Academy. Admissions are now open.",
            "content": "<p>We are pleased to announce that admissions for the 2026-2027 academic session are now open. Prospective parents can collect admission forms from the office or apply online.</p>",
            "expiry_date": (now() + timedelta(days=30)).date(),
            "attachment_url": "https://example.com/admission_form.pdf"
        },
        {
            "sms_id": "notice_gt_2",
            "title": "Holiday Notice - Independence Day",
            "slug": "holiday-notice-independence-day",
            "summary": "The school will remain closed on the occasion of Independence Day.",
            "content": "<p>This is to inform all students and staff that the school will remain closed on March 26th in observance of Independence Day.</p>",
            "expiry_date": (now() + timedelta(days=10)).date(),
        }
    ]

    for item in notices_data:
        CachedNotice.objects.update_or_create(
            tenant=tenant,
            sms_id=item['sms_id'],
            defaults={
                'title': item['title'],
                'slug': item['slug'],
                'summary': item['summary'],
                'content': item['content'],
                'expiry_date': item.get('expiry_date'),
                'attachment_url': item.get('attachment_url', ''),
                'created_at': now(),
                'updated_at': now(),
                'is_published': True
            }
        )

    # --- Seed Albums ---
    albums_data = [
        {
            "sms_id": "album_gt_1",
            "title": "Sports Day 2025 Highlights",
            "description": "Memorable moments from our annual sports competition.",
            "cover_image": "https://images.unsplash.com/photo-1541252260730-0412e3e2104e?q=80&w=1200&auto=format&fit=crop",
            "media_items": [
                {"url": "https://images.unsplash.com/photo-1461896756913-6472ddead638?q=80&w=800", "caption": "The sprint finish", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1517649763962-0c623066013b?q=80&w=800", "caption": "Relay team", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1526676037777-05a232554f77?q=80&w=800", "caption": "Winners podium", "type": "image"}
            ]
        },
        {
            "sms_id": "album_gt_2",
            "title": "Cultural Night 2025",
            "description": "A celebration of diversity through music and dance.",
            "cover_image": "https://images.unsplash.com/photo-1514525253361-bee8a19740c1?q=80&w=1200&auto=format&fit=crop",
            "media_items": [
                {"url": "https://images.unsplash.com/photo-1516280440614-37939bbacd81?q=80&w=800", "caption": "Gala Opening", "type": "image"},
                {"url": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?q=80&w=800", "caption": "Dance group", "type": "image"}
            ]
        }
    ]

    for item in albums_data:
        CachedAlbum.objects.update_or_create(
            tenant=tenant,
            sms_id=item['sms_id'],
            defaults={
                'title': item['title'],
                'description': item['description'],
                'cover_image': item['cover_image'],
                'media_items': item['media_items'],
                'created_at': now() - timedelta(days=20),
                'is_published': True
            }
        )

    print("Seeding completed successfully.")

if __name__ == "__main__":
    seed_global_tech()
