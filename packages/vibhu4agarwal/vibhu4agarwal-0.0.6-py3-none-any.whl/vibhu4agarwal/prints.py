from .details import *

divider = '|----------------------------------------------------------------------------------------|'
padding = len(divider)-2


def print_divider(condition=True):
    if condition:
        print(divider)


def adjust_print(string):
    print('|'+string.ljust(padding, ' ')+'|')


def print_name(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Name: ' + profile['name'])
    print_divider(ediv)


def print_location(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Current Location: ' + profile['location'])
    print_divider(ediv)


def print_contacts(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Contact:')
    for platform in contact:
        adjust_print(platform + ': ' + contact[platform])
    print_divider(ediv)


def print_handles(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Handles:')
    for platform in tech_profiles:
        adjust_print(platform + ": " + tech_profiles[platform])
    print_divider(ediv)


def print_summary(sdiv=False, ediv=False):
    print_divider(sdiv)
    for line in profile['summary'].splitlines():
        adjust_print(line)
    print_divider(ediv)


def print_skills(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Skills:')
    count = 0
    three_skills = []
    for skill in profile['skills']:
        three_skills.append(skill)
        count += 1
        if count % 3 == 0:
            skill_string = ', '.join(three_skills)
            three_skills.clear()
            adjust_print(skill_string)
            count = 0
    print_divider(ediv)


def print_need(sdiv=False, ediv=False):
    print_divider(sdiv)
    for line in profile['need'].splitlines():
        adjust_print(line)
    print_divider(ediv)


def print_education(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Education:')
    for institute in education.values():
        adjust_print('')
        for line in institute.splitlines():
            adjust_print(line.strip())
    print_divider(ediv)


def print_work_exp(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Work Experience:')
    for work in work_exp:
        adjust_print('')
        adjust_print(work['company'])
        adjust_print('- ' + work['role'])
        adjust_print('- ' + work['time'])
    print_divider(ediv)


def print_open_source(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print('Open Source Profile:')
    for organization in open_source:
        adjust_print('')
        adjust_print('Organization: ' + open_source[organization]['org_name'])
        adjust_print('Role: ' + open_source[organization]['role'])
        adjust_print('Repositories: ')
        links = open_source[organization]['repo_links']
        for link in links:
            adjust_print('- ' + link)
    print_divider(ediv)


def print_organizations(sdiv=False, ediv=False):
    print_divider(sdiv)
    adjust_print("Organizations I've been a part of:")
    for org in organizations:
        adjust_print('')
        adjust_print('Organization: ' + organizations[org]['org_name'])
        adjust_print('Role        : ' + organizations[org]['role'])
        adjust_print('Location    : ' + organizations[org]['location'])
    print_divider(ediv)


def print_profile(wants_contact=False, wants_handles=False,
                  wants_skills=False, wants_need=False):
    print_name(sdiv=True)
    adjust_print(profile['title'])
    if wants_contact or wants_handles:
        print_divider()
    else:
        adjust_print('')
    print_location()
    if wants_contact:
        adjust_print('')
        print_contacts()
    if wants_handles:
        adjust_print('')
        print_handles()
    print_summary(sdiv=True)
    if wants_skills:
        adjust_print('')
        print_skills()
    if wants_need:
        adjust_print('')
        print_need()


def print_resume():
    print_profile(wants_contact=True, wants_handles=True,
                  wants_skills=True, wants_need=True)
    print_education()
    print_open_source(sdiv=True)
    print_work_exp(sdiv=True)
    print_organizations(sdiv=True)
