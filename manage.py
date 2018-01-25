#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "d_appointments_project.settings")
    
    # Different port manage.py file 
    import django
    django.setup()

    # Override default port for `runserver` command
    from django.core.management.commands.runserver import Command as runserver
    runserver.default_port = "5001"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)