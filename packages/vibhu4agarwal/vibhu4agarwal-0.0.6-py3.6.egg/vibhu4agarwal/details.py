def fix(string):
    return string.ljust(22, ' ')


profile = {'name': "Vibhu Agarwal",
           'location': "Noida, India",
           'title': "Python and Open Source Enthusiast | Web Developer",
           'summary': """{}: Back-End Web Develoment
{}: Web-Scraping, Python - Testing & Packaging
{}: Machine Learning, GCP and Desktop App. Development
{}: Working with projects which could help me learn something new
{}: Summer Internships (1-2 months)""".format(fix('Primary area of work'),
                                              fix('Greatly Involved with'),
                                              fix('Also worked on'),
                                              fix('Interested in'),
                                              fix('Looking For')),
           'need': """Hit me up anytime if you've got an interesting project and need help with anything.
If the codebase is in alien language, I can still make contributions by documenting it.""",
           'skills': ['Web Development',
                      'SQL',
                      'Machine Learning',
                      'Python Testing',
                      'Python Packaging',
                      'Browser and Task Automation']}

education = {'university': """Jaypee Institute of Information Technology, Noida
             - Computer Science and Engineering - Integrated (B.Tech. & M.Tech.)
             - 2017-Present (Current Semester: IV)""",
             'school': """St.Joseph's College, Allahabad
             - XII (I.S.C.) - 2017
             - X (I.C.S.E.) - 2015"""}

contact = {'Telegram': "vibhu4agarwal",
           'Mail': "vibhu4agarwal@gmail.com"}

tech_profiles = {'LinkedIn': "https://www.linkedin.com/in/vibhu4agarwal/",
                 'GitHub': "https://github.com/Vibhu-Agarwal"}
                 # 'Codechef': "https://www.codechef.com/users/vibhu4agarwal"}

blog = 'vibhu-agarwal.blogspot.com'

internity = {'company': "Internity Foundation",
             'role': "Machine Learning Intern",
             'time': '12/2018 - 01/2019'}

geeksforgeeks = {'company': "GeeksforGeeks",
                 'role': "Technical Content Scripter (Intern)",
                 'time': "03/2019 - 04/2019"}

work_exp = [geeksforgeeks, internity]

open_source = {
    'Marauders': {'org_name': 'Marauders',
                  'repo_links': ['https://github.com/Marauders-9998/Marauders-Website',
                                 'https://github.com/Marauders-9998/Attendance-Management-using-Face-Recognition'],
                  'role': 'Owner'},
    'pandas': {'org_name': 'pandas_dev',
               'repo_links': ['https://github.com/pandas-dev/pandas'],
               'role': 'Contributor'},
    'kivy': {'org_name': 'kivy',
             'repo_links': ['https://github.com/kivy/plyer'],
             'role': 'Contributor'},
    'nexB': {'org_name': 'nexB',
             'repo_links': ['https://github.com/nexB/scancode-toolkit'],
             'role': 'Contributor'}
}

organizations = {
    'DSC': {
        'org_name': 'Developer Student Clubs',
        'role': 'Technical Coordinator',
        'location': 'JIIT, Noida'
    }
}