from django.db import models
from django.utils import timezone


# Enum of REGION.
class REGION(models.IntegerChoices):
    NONE_SELECT = 0, '-----'
    DOMESTIC = 1, 'Domestic'
    ABROAD = 2, 'Abroad'


# Enum of INDUSTRY.
class INDUSTRY(models.IntegerChoices):
    NONE_SELECT = 0, '-----'
    ENERGY = 1, 'Energy'
    MATERIALS = 2, 'Materials'
    INDUSTRIALS = 3, 'Industrials'
    CONSUMER_DISCRETIONARY = 4, 'Consumer Discretionary'
    CONSUMER_STAPLES = 5, 'Consumer Staples'
    HEALTH_CARE = 6, 'Health Care'
    FINANCIALS = 7, 'Financials'
    INFORMATION_TECHNOLOGY = 8, 'Information Technology'
    COMMUNICATION_SERVICES = 9, 'Communication Services'
    UTILITIES = 10, 'Utilities'
    REAL_ESTATE = 11, 'Real Estate'


# Enum of Cloud Type.
class CLOUDTYPE(models.IntegerChoices):
    NONE_SELECT = 0, '-----'
    AWS = 1, 'Amazon Web Service'
    GCP = 2, 'Google Cloud Platform'
    AZURE = 3, 'Microsoft Azure'


# Enum of Production.
class PRODUCTION(models.IntegerChoices):
    NONE_SELECT = 0, '-----'
    DEVELOPMENT = 1, 'Development'
    LAUNCHED = 2, 'Launched'


# Enum of Rank.
class RANK(models.IntegerChoices):
    NONE_SELECT = 0, '-----'
    SECURE = 1, 'Secure'
    NORMAL = 2, 'Normal'
    WEAK = 3, 'Weak'
    CRITICAL = 4, 'Critical'


# Organization.
class Organization(models.Model):
    name = models.CharField(verbose_name='Organization Name', max_length=255, blank=False)
    region = models.IntegerField(verbose_name='Region', choices=REGION.choices, default=0)
    industry = models.IntegerField(verbose_name='Industry', choices=INDUSTRY.choices, default=0)
    overview = models.TextField(verbose_name='Overview', max_length=1000, default='')
    domain = models.IntegerField(verbose_name='Domain', default=0)
    subdomain = models.IntegerField(verbose_name='Subdomain', default=0)
    rank = models.IntegerField(verbose_name='Rank', choices=RANK.choices, default=0)
    status = models.CharField(verbose_name='Status', max_length=10, default='N/A')
    invisible = models.BooleanField(verbose_name='Invisible', default=False)
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
    name_server = models.TextField(verbose_name='Name Server', max_length=1000, default='N/A')
    subdomain = models.IntegerField(verbose_name='Subdomain', default=0)
    rank = models.IntegerField(verbose_name='Rank', choices=RANK.choices, default=0)
    status = models.CharField(verbose_name='Status', max_length=10, default='N/A')
    invisible = models.BooleanField(verbose_name='Invisible', default=False)
    registration_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


# Subdomain.
class Subdomain(models.Model):
    related_organization_id = models.IntegerField(verbose_name='Related Organization ID', blank=False)
    related_domain_id = models.IntegerField(verbose_name='Related Domain ID', blank=False)
    name = models.CharField(verbose_name='Subdomain Name', max_length=255, blank=False)
    ip_address = models.CharField(verbose_name='IP Address', max_length=15, default='N/A')
    production = models.IntegerField(verbose_name='Production Environment', choices=PRODUCTION.choices, default=0)
    url_origin = models.CharField(verbose_name='Top URL', max_length=255, default='N/A')
    cloud_type = models.IntegerField(verbose_name='Cloud Type', choices=CLOUDTYPE.choices, default=0)
    auth_form = models.BooleanField(verbose_name='Form Authentication', default=False)
    auth_basic = models.BooleanField(verbose_name='Basic Authentication', default=False)
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
    dns_a_record = models.TextField(verbose_name='DNS A Record', max_length=5000, default='N/A')
    dns_cname_record = models.TextField(verbose_name='DNS CNAME Record', max_length=5000, default='N/A')
    dns_ns_record = models.TextField(verbose_name='DNS NS Record', max_length=5000, default='N/A')
    dns_mx_record = models.TextField(verbose_name='DNS MX Record', max_length=5000, default='N/A')
    dns_soa_record = models.TextField(verbose_name='DNS SOA Record', max_length=5000, default='N/A')
    dns_txt_record = models.TextField(verbose_name='DNS TXT Record', max_length=5000, default='N/A')
    rank = models.IntegerField(verbose_name='Rank', choices=RANK.choices, default=0)
    status = models.CharField(verbose_name='Status', max_length=10, default='N/A')
    invisible = models.BooleanField(verbose_name='Invisible', default=False)
    registration_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


# Assessment.
class Assessment(models.Model):
    related_organization_id = models.IntegerField(verbose_name='Related Organization ID', blank=False)
    related_domain_id = models.IntegerField(verbose_name='Related Domain ID', blank=False)
    related_subdomain_id = models.IntegerField(verbose_name='Related Subdomain ID', blank=False)
    scan_date = models.DateTimeField(default=timezone.now())
    target_port = models.IntegerField(verbose_name='Port', default=80, blank=False)
    assessment_url = models.CharField(verbose_name='Assessment URL', max_length=255, default='N/A')
    http_status = models.CharField(verbose_name='HTTP Status', max_length=3, default='N/A')
    product_vendor = models.CharField(verbose_name='Product Vendor', max_length=255, default='N/A')
    product_name = models.CharField(verbose_name='Product Name', max_length=255, default='N/A')
    product_version = models.CharField(verbose_name='Product Version', max_length=255, default='N/A')
    product_type = models.CharField(verbose_name='Product Type', max_length=255, default='N/A')
    product_trigger = models.CharField(verbose_name='Product Trigger', max_length=5000, default='N/A')
    product_cveid = models.CharField(verbose_name='CVE-ID', max_length=255, default='N/A')
    auth_form_trigger_ml = models.CharField(verbose_name='ML Trigger of Form Auth', max_length=5000, default='N/A')
    auth_form_trigger_url = models.CharField(verbose_name='URL Trigger of Form Auth', max_length=5000, default='N/A')
    auth_basic_trigger = models.CharField(verbose_name='Trigger of BASIC Auth', max_length=5000, default='N/A')
    unnecessary_comments = models.CharField(verbose_name='Unnecessary Comments', max_length=5000, default='N/A')
    unnecessary_contents = models.CharField(verbose_name='Unnecessary Contents', max_length=5000, default='N/A')
    directory_index = models.CharField(verbose_name='Directory Index', max_length=5000, default='N/A')
    error_messages = models.CharField(verbose_name='Error Messages', max_length=5000, default='N/A')
    server_header = models.CharField(verbose_name='Server Header', max_length=5000, default='N/A')
    log_path = models.CharField(verbose_name='Log', max_length=1000, default='N/A')
    note = models.CharField(verbose_name='Note', max_length=5000, default='N/A')
    invisible = models.BooleanField(verbose_name='Invisible', default=False)

    def __str__(self):
        return self.related_subdomain_id
