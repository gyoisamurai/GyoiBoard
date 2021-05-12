import os
from django import forms
from gyoithon.models import Organization, Domain, Subdomain


# Organization Registration Form.
class RegistrationOrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationOrganizationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Organization
        fields = ('name', 'region', 'industry', 'overview')


# Organization Update Form.
class UpdateOrganizationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['name'].widget.attrs['readonly'] = 'readonly'
        self.fields['domain'].widget.attrs['readonly'] = 'readonly'
        self.fields['subdomain'].widget.attrs['readonly'] = 'readonly'
        self.fields['rank'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['registration_date'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Organization
        fields = ('name', 'region', 'industry', 'overview', 'domain', 'subdomain', 'rank', 'status',
                  'registration_date')


# Domain Registration Form.
class RegistrationDomainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Domain
        fields = ('name', 'registrar', 'administrative_contact', 'registrant_name', 'registrant_organization',
                  'registrant_email', 'admin_name', 'admin_organization', 'admin_email', 'tech_name',
                  'tech_organization', 'tech_email', 'name_server')


# Domain Update Form.
class UpdateDomainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['related_organization_id'].widget.attrs['readonly'] = 'readonly'
        self.fields['name'].widget.attrs['readonly'] = 'readonly'
        self.fields['subdomain'].widget.attrs['readonly'] = 'readonly'
        self.fields['rank'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['registration_date'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Domain
        fields = ('related_organization_id', 'name', 'registrar', 'administrative_contact', 'registrant_name',
                  'registrant_organization', 'registrant_email', 'admin_name', 'admin_organization', 'admin_email',
                  'tech_name', 'tech_organization', 'tech_email', 'name_server', 'subdomain', 'rank', 'status',
                  'registration_date')


# Subdomain Registration Form.
class RegistrationSubdomainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Subdomain
        fields = ('name', 'ip_address', 'production', 'cloud_type', 'http_accessible', 'http_location',
                  'http_page_title', 'http_screenshot_url', 'http_screenshot_path', 'https_accessible',
                  'https_location', 'https_page_title', 'https_screenshot_url', 'https_screenshot_path',
                  'dns_a_record', 'dns_cname_record', 'dns_ns_record', 'dns_mx_record', 'dns_soa_record',
                  'dns_txt_record')


# Subdomain Update Form.
class UpdateSubdomainForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields['related_organization_id'].widget.attrs['readonly'] = 'readonly'
        self.fields['related_domain_id'].widget.attrs['readonly'] = 'readonly'
        self.fields['name'].widget.attrs['readonly'] = 'readonly'
        self.fields['rank'].widget.attrs['readonly'] = 'readonly'
        self.fields['status'].widget.attrs['readonly'] = 'readonly'
        self.fields['registration_date'].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = Subdomain
        fields = ('related_organization_id', 'related_domain_id', 'name', 'ip_address', 'production', 'cloud_type',
                  'http_accessible', 'http_location', 'http_page_title', 'http_screenshot_url', 'http_screenshot_path',
                  'https_accessible', 'https_location', 'https_page_title', 'https_screenshot_url',
                  'https_screenshot_path', 'dns_a_record', 'dns_cname_record', 'dns_ns_record', 'dns_mx_record',
                  'dns_soa_record', 'dns_txt_record', 'rank', 'status', 'registration_date')
