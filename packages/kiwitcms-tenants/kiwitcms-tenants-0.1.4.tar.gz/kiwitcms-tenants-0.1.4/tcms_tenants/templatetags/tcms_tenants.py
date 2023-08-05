# Copyright (c) 2019 Alexander Todorov <atodorov@MrSenko.com>

# Licensed under the GPL 3.0: https://www.gnu.org/licenses/gpl-3.0.txt

from django import template
from django.db import connection

from tcms_tenants import utils

register = template.Library()


@register.simple_tag
def tenant_url(request):
    return utils.tenant_url(request, connection.schema_name)
