from collections import namedtuple

Issue = namedtuple('Issue', ['id'])

Project = namedtuple('Project', ['id'])

Command = namedtuple('Command', ['issues', 'query'])
