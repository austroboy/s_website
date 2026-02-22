import json

def get_navigation_items():
    """
    Returns the structured navigation items for the header.
    """
    return [
        {
            'label': 'About',
            'hasDropdown': True,
            'megaMenu': [
                {
                    'title': 'ABOUT NSU',
                    'href': '/about/history', # Or a general about page if exists
                    'items': [
                        { 'label': 'Brief History', 'href': '/about/history' },
                        { 'label': 'Vision, Mission & Strategy', 'href': '/about/vision-mission' },
                        { 'label': 'International Advisory Board', 'href': '/about/advisory-board' },
                        { 'label': 'Accreditation', 'href': '/about/accreditation' },
                        { 'label': 'International Recognition', 'href': '/about/recognition' },
                        { 'label': 'Facts About NSU', 'href': '/about/facts' }
                    ]
                },
                {
                    'title': 'NSU Trustees',
                    'items': [
                        { 'label': 'Board of Trustees', 'href': '/about/trustees' }
                    ]
                },
                {
                    'title': 'Executive Leaders',
                    'items': [
                        { 'label': 'VC, Pro-VC & Treasurer', 'href': '/about/leadership' },
                        { 'label': 'Deans, Chairs & Directors', 'href': '/about/deans' },
                        { 'label': 'Administration', 'href': '/about/administration' }
                    ]
                },
                {
                    'title': 'Authorities',
                    'items': [
                        { 'label': 'Syndicate', 'href': '/about/syndicate' },
                        { 'label': 'Academic Council', 'href': '/about/academic-council' }
                    ]
                }
            ]
        },
        {
            'label': 'Academic',
            'hasDropdown': True,
            'megaMenu': [
                {
                    'title': 'SCHOOLS',
                    'href': '/departments/',
                    'items': [
                        { 'label': 'School of Business & Economics', 'href': '/departments/sbe' },
                        { 'label': 'School of Engineering & Physical Sciences', 'href': '/departments/seps' },
                        { 'label': 'School of Humanities & Social Sciences', 'href': '/departments/shss' },
                        { 'label': 'School of Health & Life Sciences', 'href': '/departments/shls' }
                    ]
                },
                {
                    'title': 'PROGRAMS',
                    'href': '/programs/',
                    'items': [
                        { 'label': 'Undergraduate Programs', 'href': '/programs/undergraduate' },
                        { 'label': 'Graduate Programs', 'href': '/programs/graduate' },
                        { 'label': 'PhD Programs', 'href': '/programs/phd' }
                    ]
                }
            ]
        },
         { 'label': 'Admission', 'href': '/admissions/', 'hasDropdown': False },
        { 'label': 'News', 'href': '/news/', 'hasDropdown': False },
        { 'label': 'Gallery', 'href': '/gallery/', 'hasDropdown': False },
        { 'label': 'Notice', 'href': '/notice/', 'hasDropdown': False },
        { 'label': 'Contact Us', 'href': '/contact-us/', 'hasDropdown': False },
    ]

def navigation(request):
    """
    Context processor to inject navigation items globally.
    """
    return {
        'navigation_items_json': json.dumps(get_navigation_items())
    }
