from django.views.generic import DetailView, TemplateView
from .models import Page, HomepageSection
from cache.models import CachedNews, CachedEvent, CachedNotice, CachedProgram, CachedAlbum
from django.utils.timezone import now
from django.db.models import Q

class HomeView(TemplateView):
    template_name = 'content/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = self.request.tenant

        # 1. Hero Data
        context['hero_data'] = {
            'eyebrow': 'Welcome to NSU',
            'title_main': 'Step Up With',
            'title_gradient': 'Admission',
            'description': 'Join one of the most prestigious private universities in Bangladesh. Shaping leaders since 2003.',
            'images': [
                { 'url': 'https://images.unsplash.com/photo-1606761568499-6d2451b23c66?q=80&w=1986&auto=format&fit=crop', 'alt': 'University Campus' },
                { 'url': 'https://images.unsplash.com/photo-1562774053-701939374585?q=80&w=1986&auto=format&fit=crop', 'alt': 'Library' },
                { 'url': 'https://images.unsplash.com/photo-1541339907198-e08756dedf3f?q=80&w=1986&auto=format&fit=crop', 'alt': 'Modern Classroom' },
                { 'url': 'https://plus.unsplash.com/premium_photo-1677567996070-68fa4181775a?q=80&w=1986&auto=format&fit=crop', 'alt': 'Students Group' }
            ]
        }

        # 2. Academic Programs Data
        context['programs_data'] = {
            'categories': ['Undergraduate', 'Graduate'],
            'items': [
                { 
                    'name': 'B.Sc. in Computer Science and Engineering (CSE)', 
                    'shortCode': 'CSE', 'category': 'Undergraduate', 'duration': '4 Years', 'credits': '140 Credit',
                    'image': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=2070&auto=format&fit=crop', 'icon': 'computer'
                },
                { 
                    'name': 'B.Sc. in Electrical and Electronic Engineering (EEE)', 
                    'shortCode': 'EEE', 'category': 'Undergraduate', 'duration': '4 Years', 'credits': '140 Credit',
                    'image': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?q=80&w=2070&auto=format&fit=crop', 'icon': 'cpu'
                },
                { 
                    'name': 'B.Sc. in Electronic and Telecommunication Engineering', 
                    'shortCode': 'ETE', 'category': 'Undergraduate', 'duration': '4 Years', 'credits': '140 Credit',
                    'image': 'https://images.unsplash.com/photo-1551624511-71852021c251?q=80&w=2070&auto=format&fit=crop', 'icon': 'radio'
                },
                { 
                    'name': 'B.Sc. in Civil Engineering (CE)', 
                    'shortCode': 'CIVIL', 'category': 'Undergraduate', 'duration': '4 Years', 'credits': '146 Credit',
                    'image': 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?q=80&w=2070&auto=format&fit=crop', 'icon': 'building'
                },
                { 
                    'name': 'Master of Business Administration (MBA)', 
                    'shortCode': 'MBA', 'category': 'Graduate', 'duration': '2 Years', 'credits': '60 Credit',
                    'image': 'https://images.unsplash.com/photo-1454165833772-d996d49513d7?q=80&w=2070&auto=format&fit=crop', 'icon': 'briefcase'
                },
                { 
                    'name': 'Master in Public Health (MPH)', 
                    'shortCode': 'MPH', 'category': 'Graduate', 'duration': '2 Years', 'credits': '52 Credit',
                    'image': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=1999&auto=format&fit=crop', 'icon': 'heart'
                }
            ]
        }

        # 3. News & Events Data
        context['events_data'] = {
            'items': [
                {
                    'title': 'Think Beyond the Syllabus with Tahsan Khan',
                    'day': '21', 'month': 'Jul',
                    'image': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=2070&auto=format&fit=crop',
                    'href': '#'
                },
                {
                    'title': 'Empowering Voices through Freedom of Association',
                    'day': '15', 'month': 'Jul',
                    'image': 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=2070&auto=format&fit=crop',
                    'href': '#'
                },
                {
                    'title': 'English Department Celebrates Emerging Talents',
                    'day': '28', 'month': 'Jun',
                    'image': 'https://images.unsplash.com/photo-1523580494863-6f303125d906?q=80&w=2070&auto=format&fit=crop',
                    'href': '#'
                },
                {
                    'title': 'Inauguration of the presidency University Library',
                    'day': '02', 'month': 'Jun',
                    'image': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=2070&auto=format&fit=crop',
                    'href': '#'
                }
            ]
        }

        # 4. Notices Data
        context['notices_data'] = {
            'items': [
                { 'title': 'Admission going on for Fall Semester 2026', 'date': '19 Feb', 'year': '2026', 'isNew': True, 'href': '#' },
                { 'title': 'Holiday Notice for International Mother Language Day', 'date': '21 Feb', 'year': '2026', 'isNew': True, 'href': '#' },
                { 'title': 'Schedule for Mid-Term Examination Spring 2026', 'date': '15 Feb', 'year': '2026', 'isNew': False, 'href': '#' },
                { 'title': 'Workshop on Cyber Security for IT Students', 'date': '10 Feb', 'year': '2026', 'isNew': False, 'href': '#' },
                { 'title': 'Annual Sports Day 2026 - Registration Open', 'date': '05 Feb', 'year': '2026', 'isNew': False, 'href': '#' },
                { 'title': 'Library Timing Extended for Final Exams', 'date': '01 Feb', 'year': '2026', 'isNew': False, 'href': '#' }
            ]
        }

        # 5. Stats Data
        context['stats_data'] = {
            'bg_image': 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2070&auto=format&fit=crop',
            'items': [
                { 'label': 'ESTABLISHED', 'target': 2003, 'icon': 'landmark', 'suffix': '' },
                { 'label': 'PROGRAMMES', 'target': 13, 'icon': 'book-open', 'suffix': '' },
                { 'label': 'TEACHERS', 'target': 100, 'icon': 'users', 'suffix': '+' },
                { 'label': 'GRADUATES', 'target': 10000, 'icon': 'graduation-cap', 'suffix': '+' }
            ]
        }

        # 6. Gallery Data
        context['gallery_data'] = {
            'items': [
                { 'id': 1, 'title': 'Guest Lecture', 'date': '21 Jul', 'image': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=600&auto=format&fit=crop', 'gridClass': 'col-span-1 row-span-1' },
                { 'id': 2, 'title': 'Cultural Performance', 'date': '15 Jul', 'image': 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=600&auto=format&fit=crop', 'gridClass': 'col-span-1 row-span-1' },
                { 'id': 3, 'title': 'Student Portrait', 'date': '28 Jun', 'image': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=800&auto=format&fit=crop', 'gridClass': 'col-span-1 row-span-2' },
                { 'id': 4, 'title': 'Awards Ceremony 2026', 'date': '10 Jun', 'image': 'https://images.unsplash.com/photo-1523580494863-6f303125d906?q=80&w=1200&auto=format&fit=crop', 'gridClass': 'col-span-2 row-span-1' },
                { 'id': 5, 'title': 'Inspiring Session', 'date': '24 Apr', 'image': 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=1200&auto=format&fit=crop', 'gridClass': 'col-span-2 row-span-1' },
                { 'id': 6, 'title': 'Grand Iftar', 'date': '14 Mar', 'image': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=600&auto=format&fit=crop', 'gridClass': 'col-span-1 row-span-1' },
                { 'id': 7, 'title': 'Presidency Day', 'date': '02 Jan', 'image': 'https://images.unsplash.com/photo-1454165833772-d996d49513d7?q=80&w=600&auto=format&fit=crop', 'gridClass': 'col-span-1 row-span-1' }
            ]
        }
        return context

class PageDetailView(DetailView):
    model = Page
    template_name = 'content/page_detail.html'
    context_object_name = 'page'

    def get_queryset(self):
        return super().get_queryset().filter(tenant=self.request.tenant, published=True)

class DepartmentsView(TemplateView):
    template_name = 'content/department.html'

class DepartmentDetailView(TemplateView):
    template_name = 'content/department_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mocking the payload based on the requested JSON structure
        context['department'] = {
            'featured': {
                'title': 'BRAC Business School',
                'description': 'The BRAC Business School (BBS) is committed to providing excellent business education and developing future leaders. We strive to create a vibrant learning community that fosters intellectual curiosity, innovation, and ethical leadership.',
                'image': {
                    'url': 'https://images.unsplash.com/photo-1523240715632-d984bc3107d1?q=80&w=2070&auto=format&fit=crop',
                    'alt': 'Overview Image'
                }
            },
            'head_message': {
                'title': 'Message from the Head, Department of Business ...',
                'profile': {
                    'name': 'Prof. Dr. Mohammed Julfikar Ali, PhD',
                    'image': {
                        'url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=1976&auto=format&fit=crop',
                        'alt': 'Prof. Dr. Mohammed Julfikar Ali'
                    },
                    'overlayDesignation': '- Head, Department of Business ...'
                },
                'messageBodyHtml': '<p>Welcome to the Department of Business Administration at Presidency University! We are proud of our commitment to providing high-quality business education that prepares our students to become future leaders and innovators.</p><p>Our dedicated faculty members are experts in their respective fields and are passionate about teaching and mentoring students. We...</p>',
                'infoTiles': [
                    {
                        'type': 'email',
                        'label': 'E-Mail',
                        'value': 'dr.jali@pu.edu.bd'
                    },
                    {
                        'type': 'designation',
                        'label': 'Designation',
                        'value': 'Head, Department of Business ...'
                    }
                ],
            },
            'faculty': {
                'sectionTitle': 'FULL TIME FACULTY MEMBERS',
                'members': [
                    {
                        'id': 'f1',
                        'name': 'Dr. Shahidul Islam Khan',
                        'image': {
                            'url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=1974&auto=format&fit=crop',
                            'alt': 'Dr. Shahidul Islam Khan'
                        },
                        'rank': 'Professor',
                        'roles': ['Head of CSE', 'Dean of School of Engineering'],
                        'email': 'shahid@pu.edu.bd',
                        'order': 1
                    },
                    {
                        'id': 'f2',
                        'name': 'Dr. Kakali Chowdhury',
                        'image': {
                            'url': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=1974&auto=format&fit=crop',
                            'alt': 'Dr. Kakali Chowdhury'
                        },
                        'rank': 'Associate Professor',
                        'email': 'kakali@pu.edu.bd',
                        'order': 2
                    },
                    {
                        'id': 'f3',
                        'name': 'Dr. Fatema Sayed',
                        'image': {
                            'url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?q=80&w=1974&auto=format&fit=crop',
                            'alt': 'Dr. Fatema Sayed'
                        },
                        'rank': 'Assistant Professor',
                        'email': 'fsayed@pu.edu.bd',
                        'phone': '01777867808',
                        'order': 3
                    }
                ]
            },
            'program': {
                'programTitle': 'Bachelor of Social Science in Economics (ECO)',
                'sections': [
                    {
                        'id': '101',
                        'slug': 'program-overview',
                        'title': 'Program Overview',
                        'contentHtml': '<p class="mb-4">The Bachelor of Social Science in Economics program provides students with a comprehensive understanding of the principles and practices of economics. The program is designed to equip students with the skills and knowledge needed to analyze and solve real-world economic problems.</p><p class="mb-4">The program aims to produce well-rounded graduates who are equipped with the skills and knowledge needed to succeed in the ever-changing global economic environment. The curriculum covers a wide range of topics within the field of economics, including micro and macroeconomics, econometrics and data analysis. Students will also study current economic issues and policy debates such as international trade, development economics, environmental economics etc. The program also allows students to take elective courses which allows them to tailor their education to their individual career goals.</p><p>Graduates of the program have gone on to successful careers in research, international development organizations, finance, banking, non-government organizations, consulting and academia, both at home and abroad.</p>',
                        'order': 1
                    },
                    {
                        'id': '102',
                        'slug': 'program-highlights',
                        'title': 'Program Highlights',
                        'contentHtml': '<ul class="space-y-4 list-disc pl-5"><li>Strong emphasis on both theoretical and applied economics, with a focus on solving real-world problems</li><li>Wide range of elective courses, allowing students to tailor their education to their specific interests and career goals</li><li>Experienced, highly qualified and diverse faculty body with expertise in various fields of economics, including micro and macroeconomics, econometrics, environmental economics, international trade and development economics</li><li>Focus on critical thinking, problem-solving and data analysis skills which prepares students for careers in fields such as finance, consulting and policy analysis</li><li>Emphasis on the application of economic theories to real-world problems and preparing students to be able to analyze, interpret and make decisions based on data</li><li>Access to computer labs with specialized statistical software packages</li></ul>',
                        'order': 2
                    },
                    {
                        'id': '103',
                        'slug': 'career-opportunities',
                        'title': 'Career Opportunities',
                        'contentHtml': '<p>Graduates have gone on to successful careers in research, international organizations, banking, and public policy.</p>',
                        'order': 3
                    }
                ]
            },
            'programs': [
                {
                    'name': 'B.Sc. in Computer Science and Engineering (CSE)',
                    'shortCode': 'CSE',
                    'duration': '4 Years',
                    'credits': '140 Credit',
                    'image_url': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=2070&auto=format&fit=crop',
                    'icon': 'computer'
                },
                {
                    'name': 'Master of Business Administration (MBA)',
                    'shortCode': 'MBA',
                    'duration': '2 Years',
                    'credits': '60 Credit',
                    'image_url': 'https://images.unsplash.com/photo-1454165833772-d996d49513d7?q=80&w=2070&auto=format&fit=crop',
                    'icon': 'briefcase'
                }
            ],
            'news_events': [
                {
                    'title': 'Think Beyond the Syllabus with Tahsan Khan',
                    'day': '21',
                    'month': 'Jul',
                    'image_url': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=2070&auto=format&fit=crop',
                    'href': '#'
                },
                {
                    'title': 'Empowering Voices through Freedom of Association and...',
                    'day': '15',
                    'month': 'Jul',
                    'image_url': 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=2070&auto=format&fit=crop',
                    'href': '#'
                }
            ],
            'gallery': [
                {
                    'id': 1,
                    'title': 'Guest Lecture',
                    'date': '21 Jul',
                    'image_url': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=600&auto=format&fit=crop',
                    'gridClass': 'col-span-1 row-span-1'
                },
                {
                    'id': 3,
                    'title': 'Student Portrait',
                    'date': '28 Jun',
                    'image_url': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=800&auto=format&fit=crop',
                    'gridClass': 'col-span-1 row-span-2'
                },
                {
                    'id': 4,
                    'title': 'Awards Ceremony 2026',
                    'date': '10 Jun',
                    'image_url': 'https://images.unsplash.com/photo-1523580494863-6f303125d906?q=80&w=1200&auto=format&fit=crop',
                    'gridClass': 'col-span-2 row-span-1'
                }
            ]
        }
        return context

class ProgramDetailView(TemplateView):
    template_name = 'content/program_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mocking the payload based on the requested screenshot structure
        context['program'] = {
            'title': 'Bachelor of Business Administration (BBA)',
            'sections': [
                {
                    'id': 'overview',
                    'title': 'Program Overview',
                    'contentHtml': '''
                    <p>This degree is ideal for those who want a future with fewer constraints. Studying BBA at BRAC University, students gain knowledge of real-world business practices, what it takes to start a successful business, and how to excel in the corporate world. The BBA program at BRAC University offers a distinctive set of specializations in various business disciplines: Accounting, Finance, E-Business, Entrepreneurship, Human Resource Management, Information Systems, Management, Marketing, Operations and Supply Chain Management, and others. Additionally, BRAC University has excellent professors who are always willing to assist students in the classroom and during consultation hours.</p>
                    <p class="mt-4">The combination of creative thinking and rigorous analysis students develop here makes them appealing for a wide range of jobs in corporates and the academic world.</p>
                    '''
                },
                {
                    'id': 'highlights',
                    'title': 'Program Highlights',
                    'contentHtml': '''
                    <p>The Bachelor of Business Administration (BBA) program aims at enabling students to acquire and practise state-of-the-art business and management knowledge and skills, thereby helping them become outstanding business leaders in the highly dynamic global environment of the 21st century. The program prepares students for entry-level managerial positions and equips them with knowledge and skills to advance to executive and senior positions in any organization. The program concentrates on Accounting, Finance, Banking and Insurance, Marketing, E-business, Human Resource Management, Computer Information Management, and Entrepreneurship. These specializations enable graduates to seek jobs in functional areas, such as marketing, finance, human resources and operations of organizations or in specific activities like accounting, information system and e-business, or to pursue a business career as an entrepreneur.</p>
                    '''
                },
                {
                    'id': 'career',
                    'title': 'Career Opportunities',
                    'contentHtml': '''
                    <p>As a BRAC University graduate, one will be able to join the ranks of successful and influential professionals who are making a difference in organizations all over the world. BRAC University's dedicated career guidance supports students throughout the year, assisting them in planning for the next stage of their careers and providing them with the tools and strategies to compete effectively in the global job market. Many of BRAC University's graduates hold senior positions in management, marketing, and finance in a variety of industries and sectors, while others have started their businesses. Recent graduates have gone on to work for organizations such as the World Bank, UNICEF, Unilever, H&M, etc.</p>
                    '''
                },
                {
                    'id': 'placement',
                    'title': 'Placement and Further Study Opportunities',
                    'contentHtml': '''
                    <p>Students of BRAC University are placed in various companies and organizations. Some of these organizations have a global presence, while some students received international placements as well. Some of the top companies, where the students of BRAC University are employed, are given below:</p>
                    '''
                },
                {
                    'id': 'curriculum',
                    'title': 'The course curriculum',
                    'contentHtml': '<p>Details about the rigorous multi-disciplinary curriculum will be positioned here.</p>'
                },
                {
                    'id': 'facilities',
                    'title': 'Facilities and Support',
                    'contentHtml': '<p>Comprehensive details about campus facilities, modern labs, and academic support.</p>'
                }
            ]
        }
        return context

class NewsListView(TemplateView):
    template_name = 'content/news_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_events'] = [
            {
                'title': 'Think Beyond the Syllabus with Tahsan Khan',
                'day': '21',
                'month': 'Jul',
                'image_url': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=2070&auto=format&fit=crop',
                'slug': 'think-beyond'
            },
            {
                'title': 'Empowering Voices through Freedom of Association',
                'day': '15',
                'month': 'Jul',
                'image_url': 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=2070&auto=format&fit=crop',
                'slug': 'empowering-voices'
            },
            {
                'title': 'English Department Celebrates Emerging Writers',
                'day': '28',
                'month': 'Jun',
                'image_url': 'https://images.unsplash.com/photo-1523580494863-6f303125d906?q=80&w=2070&auto=format&fit=crop',
                'slug': 'english-department'
            },
            {
                'title': 'Inauguration of the University Public Library',
                'day': '02',
                'month': 'Jun',
                'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=2070&auto=format&fit=crop',
                'slug': 'library-inauguration'
            }
        ]
        return context

class NewsDetailView(TemplateView):
    template_name = 'content/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We mock one detailed article mapped to any slug for demonstration.
        context['news_item'] = {
            'title': 'Think Beyond the Syllabus with Tahsan Khan',
            'date': 'July 21, 2026',
            'author': 'Dept. of Student Affairs',
            'images': [
                {'url': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=2070&auto=format&fit=crop', 'alt': 'Audience at seminar'},
                {'url': 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?q=80&w=2070&auto=format&fit=crop', 'alt': 'Tahsan Khan speaking'},
                {'url': 'https://images.unsplash.com/photo-1540317580384-e5d43867caa6?q=80&w=2070&auto=format&fit=crop', 'alt': 'Q&A Session'}
            ],
            'contentHtml': '''
                <p class="lead">In an inspiring and interactive session organized by the University, students were heavily encouraged to break academic boundaries.</p>
                <p>The event, titled "Think Beyond the Syllabus," gathered more than 500 students across multiple disciplines. Guest speakers emphasized the importance of networking, cultivating soft skills, and joining professional clubs to bolster modern employability.</p>
                <h3>Highlight Quotes</h3>
                <blockquote>"Your transcript opens the door, but your personality and extracurricular experience invite you to the table."</blockquote>
                <p>Following the keynote, a robust Q&A session empowered young scholars to ask granular questions concerning overseas higher education preparations and domestic industry integration. The university looks forward to hosting more luminaries from the industry next semester.</p>
            '''
        }
        return context

class GalleryView(TemplateView):
    template_name = 'content/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = [
            {
                'id': 1,
                'title': 'Guest Lecture',
                'date': '21 Jul',
                'slug': 'guest-lecture-2026',
                'image_url': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=600&auto=format&fit=crop',
                'gridClass': 'col-span-1 row-span-1'
            },
            {
                'id': 2,
                'title': 'Cultural Dance Performance',
                'date': '15 Jul',
                'slug': 'cultural-dance',
                'image_url': 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=600&auto=format&fit=crop',
                'gridClass': 'col-span-1 row-span-1'
            },
            {
                'id': 3,
                'title': 'Student Portrait',
                'date': '28 Jun',
                'slug': 'student-portrait',
                'image_url': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?q=80&w=800&auto=format&fit=crop',
                'gridClass': 'col-span-1 row-span-2'
            },
            {
                'id': 4,
                'title': 'Awards Ceremony 2026',
                'date': '10 Jun',
                'slug': 'awards-ceremony',
                'image_url': 'https://images.unsplash.com/photo-1523580494863-6f303125d906?q=80&w=1200&auto=format&fit=crop',
                'gridClass': 'col-span-2 row-span-1'
            },
            {
                'id': 5,
                'title': 'Inspiring Session',
                'date': '24 Apr',
                'slug': 'inspiring-session',
                'image_url': 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?q=80&w=1200&auto=format&fit=crop',
                'gridClass': 'col-span-2 row-span-1'
            },
            {
                'id': 6,
                'title': 'Grand Iftar',
                'date': '14 Mar',
                'slug': 'grand-iftar',
                'image_url': 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80&w=600&auto=format&fit=crop',
                'gridClass': 'col-span-1 row-span-1'
            },
            {
                'id': 7,
                'title': 'University Day Celebration',
                'date': '02 Jan',
                'slug': 'university-day',
                'image_url': 'https://images.unsplash.com/photo-1454165833772-d996d49513d7?q=80&w=600&auto=format&fit=crop',
                'gridClass': 'col-span-1 row-span-1'
            }
        ]
        return context

class GalleryDetailView(TemplateView):
    template_name = 'content/gallery_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mock detailed event gallery
        context['gallery_event'] = {
            'title': 'Cultural Dance Performance',
            'date': 'July 15, 2026',
            'time': '6:30 PM - 9:00 PM',
            'description': 'An evening celebrating the immense diversity and rich cultural heritage of our student body. Featuring classical and contemporary routines choreographed entirely by the Student Fine Arts Club.',
            'images': [
                'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1547153760-18fc86324498?q=80&w=1200&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1516997121675-4c2d1684aa3e?q=80&w=1200&auto=format&fit=crop'
            ]
        }
        return context

class NoticeListView(TemplateView):
    template_name = 'content/notice_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notices'] = [
            {
                'title': 'Admission going on for Fall Semester 2026',
                'full_date': '19 February, 2026',
                'day': '19',
                'month': 'Feb',
                'year': '2026',
                'is_new': True,
                'slug': 'admission-fall-2026',
                'image_url': 'https://images.unsplash.com/photo-1523050853064-dbad350e7a79?q=80&w=800&auto=format&fit=crop'
            },
            {
                'title': 'Holiday Notice for International Mother Language Day',
                'full_date': '21 February, 2026',
                'day': '21',
                'month': 'Feb',
                'year': '2026',
                'is_new': True,
                'slug': 'holiday-mother-language-day',
                'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?q=80&w=800&auto=format&fit=crop'
            },
            {
                'title': 'Schedule for Mid-Term Examination Spring 2026',
                'full_date': '15 February, 2026',
                'day': '15',
                'month': 'Feb',
                'year': '2026',
                'is_new': False,
                'slug': 'mid-term-exam-spring-2026',
                'image_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?q=80&w=800&auto=format&fit=crop'
            },
            {
                'title': 'Workshop on Cyber Security for IT Students',
                'full_date': '10 February, 2026',
                'day': '10',
                'month': 'Feb',
                'year': '2026',
                'is_new': False,
                'slug': 'cyber-security-workshop',
                'image_url': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=800&auto=format&fit=crop'
            }
        ]
        
        # News & Events for Sidebar
        context['news_events'] = [
            { 'title': 'Think Beyond the Syllabus with Tahsan Khan', 'day': '21', 'month': 'Jul', 'image': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=200&auto=format&fit=crop', 'href': '/news/think-beyond/' },
            { 'title': 'Empowering Voices through Freedom of Association', 'day': '15', 'month': 'Jul', 'image': 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=200&auto=format&fit=crop', 'href': '/news/empowering-voices/' },
            { 'title': 'English Department Celebrates Emerging Talents', 'day': '28', 'month': 'Jun', 'image': 'https://images.unsplash.com/photo-1523580494863-6f303125d906?q=80&w=200&auto=format&fit=crop', 'href': '/news/english-department/' }
        ]
        return context

class NoticeDetailView(TemplateView):
    template_name = 'content/notice_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notice'] = {
            'title': 'Admission going on for Fall Semester 2026',
            'full_date': '19 February, 2026',
            'contentHtml': '''
                <p class="lead">We are pleased to announce that the admission process for the Fall Semester 2026 is now officially open.</p>
                <p>Prospective students are encouraged to apply early to secure their place in our prestigious programs. The university offers a wide range of undergraduate and graduate courses designed to equip students with the skills needed for the 21st-century job market.</p>
                <h3>Important Deadlines:</h3>
                <ul>
                    <li>Early Bird Application: March 31, 2026</li>
                    <li>Regular Application Deadline: May 15, 2026</li>
                    <li>Admission Test: June 1, 2026</li>
                </ul>
                <p>For more information on how to apply, please visit our <a href="/admissions/">Admissions Page</a> or contact the Admission Office directly.</p>
            '''
        }
        
        # Sidebar "News & Events" data
        context['news_events'] = [
            { 'title': 'Think Beyond the Syllabus with Tahsan Khan', 'day': '21', 'month': 'Jul', 'image': 'https://images.unsplash.com/photo-1475721027785-f74ecd5ed996?q=80&w=200&auto=format&fit=crop', 'href': '/news/think-beyond/' },
            { 'title': 'Empowering Voices through Freedom of Association', 'day': '15', 'month': 'Jul', 'image': 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?q=80&w=200&auto=format&fit=crop', 'href': '/news/empowering-voices/' },
            { 'title': 'English Department Celebrates Emerging Talents', 'day': '28', 'month': 'Jun', 'image': 'https://images.unsplash.com/photo-1523580494863-6f303125d906?q=80&w=200&auto=format&fit=crop', 'href': '/news/english-department/' }
        ]

        # Recent Notices for Sidebar (Requested to remain same)
        context['recent_notices'] = [
            { 'title': 'Holiday Notice for International Mother Language Day', 'date': '21 Feb', 'year': '2026', 'isNew': True, 'href': '/notice/holiday-mother-language-day/' },
            { 'title': 'Schedule for Mid-Term Examination Spring 2026', 'date': '15 Feb', 'year': '2026', 'isNew': False, 'href': '/notice/mid-term-exam-spring-2026/' },
            { 'title': 'Workshop on Cyber Security for IT Students', 'date': '10 Feb', 'year': '2026', 'isNew': False, 'href': '/notice/cyber-security-workshop/' }
        ]
        return context

class ContactView(TemplateView):
    template_name = 'content/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract programs for the dropdown
        context['programs'] = [
            'B.Sc. in Computer Science and Engineering (CSE)',
            'B.Sc. in Electrical and Electronic Engineering (EEE)',
            'B.Sc. in Electronic and Telecommunication Engineering',
            'B.Sc. in Civil Engineering (CE)',
            'Master of Business Administration (MBA)',
            'Master in Public Health (MPH)'
        ]
        context['contact_info'] = {
            'address': 'House 11/A, Road 92, Gulshan-2, Dhaka 1212',
            'phone': '+8801766554433',
            'email': 'admission@pu.edu.bd',
            'map_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3650.603348123307!2d90.41243161543362!3d23.79720479287311!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3755c70f05596b6d%3A0x6b04f7678f280a30!2sPresidency%20University!5e0!3m2!1sen!2sbd!4v1645431000000!5m2!1sen!2sbd'
        }
        return context
