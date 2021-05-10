from django.db import models
from django.utils import timezone


# Organization.
class Organization(models.Model):
    name = models.CharField(verbose_name='Organization Name', max_length=255, blank=False)
    overview = models.CharField(verbose_name='Overview', max_length=255, default='N/A')
    domain = models.IntegerField(verbose_name='Domain', default=0)
    subdomain = models.IntegerField(verbose_name='Subdomain', default=0)
    status = models.CharField(verbose_name='Status', max_length=10, default='N/A')
    registration_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


# Domain.
class Domain(models.Model):
    related_organization_id = models.IntegerField(verbose_name='Related Organization ID', blank=False)
    name = models.CharField(verbose_name='Domain Name', max_length=255, blank=False)
    registrar = models.CharField(verbose_name='Registrar', max_length=255, default='N/A')
    administrative_contact = models.CharField(verbose_name='Administrative Contact', max_length=255, default='N/A')
    registrant_name = models.CharField(verbose_name='Registrant Name', max_length=255, default='N/A')
    registrant_organization = models.CharField(verbose_name='Registrant Organization', max_length=255, default='N/A')
    registrant_email = models.CharField(verbose_name='Registrant Email', max_length=255, default='N/A')
    admin_name = models.CharField(verbose_name='Admin Name', max_length=255, default='N/A')
    admin_organization = models.CharField(verbose_name='Admin Organization', max_length=255, default='N/A')
    admin_email = models.CharField(verbose_name='Admin Email', max_length=255, default='N/A')
    tech_name = models.CharField(verbose_name='Tech Name', max_length=255, default='N/A')
    tech_organization = models.CharField(verbose_name='Tech Organization', max_length=255, default='N/A')
    tech_email = models.CharField(verbose_name='Tech Email', max_length=255, default='N/A')
    name_server = models.CharField(verbose_name='Name Server', max_length=1000, default='N/A')
    subdomain = models.IntegerField(verbose_name='Subdomain', default=0)
    status = models.CharField(verbose_name='Status', max_length=10, default='N/A')
    registration_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


# Subdomain.
class Subdomain(models.Model):
    related_organization_id = models.IntegerField(verbose_name='Related Organization ID', blank=False)
    related_domain_id = models.IntegerField(verbose_name='Related Domain ID', blank=False)
    name = models.CharField(verbose_name='Subdomain Name', max_length=255, blank=False)
    ip_address = models.CharField(verbose_name='IP Address', max_length=15, default='N/A')
    http_accessible = models.CharField(verbose_name='Accessible (HTTP)', max_length=255, default='N/A')
    http_location = models.CharField(verbose_name='Location (HTTP)', max_length=1000, default='N/A')
    http_page_title = models.CharField(verbose_name='Page Title (HTTP)', max_length=1000, default='N/A')
    http_screenshot_url = models.CharField(verbose_name='Screenshot Captured URL (HTTP)', max_length=1000, default='N/A')
    http_screenshot_path = models.CharField(verbose_name='Path to save the Screenshot (HTTP)', max_length=1000, default='N/A')
    https_accessible = models.CharField(verbose_name='Accessible (HTTPS)', max_length=255, default='N/A')
    https_location = models.CharField(verbose_name='Location (HTTPS)', max_length=1000, default='N/A')
    https_page_title = models.CharField(verbose_name='Page Title (HTTPS)', max_length=1000, default='N/A')
    https_screenshot_url = models.CharField(verbose_name='Screenshot Captured URL (HTTPS)', max_length=1000, default='N/A')
    https_screenshot_path = models.CharField(verbose_name='Path to save the Screenshot (HTTPS)', max_length=1000, default='N/A')
    dns_a_record = models.CharField(verbose_name='DNS A Record', max_length=5000, default='N/A')
    dns_cname_record = models.CharField(verbose_name='DNS CNAME Record', max_length=5000, default='N/A')
    dns_ns_record = models.CharField(verbose_name='DNS NS Record', max_length=5000, default='N/A')
    dns_mx_record = models.CharField(verbose_name='DNS MX Record', max_length=5000, default='N/A')
    dns_soa_record = models.CharField(verbose_name='DNS SOA Record', max_length=5000, default='N/A')
    dns_txt_record = models.CharField(verbose_name='DNS TXT Record', max_length=5000, default='N/A')
    status = models.CharField(verbose_name='Status', max_length=10, default='N/A')
    registration_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name
