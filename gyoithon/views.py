from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages

from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from gyoiboard.tasks import executation
from gyoithon.util import Utilty
from gyoithon.models import Organization, Domain, Subdomain
from gyoithon.forms import RegistrationOrganizationForm, UpdateOrganizationForm, RegistrationDomainForm, \
    UpdateDomainForm, RegistrationSubdomainForm, UpdateSubdomainForm
from gyoithon.serializers import OrganizationSerializer, DomainSerializer, SubdomainSerializer


# Organization List.
class OrganizationViewSet(ListAPIView):
    model = Organization
    queryset = Organization.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationSerializer


# Organization Detail.
class OrganizationDetailSet(RetrieveAPIView):
    model = Organization
    queryset = Organization.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationSerializer


# Add new Organization.
class OrganizationCreateSet(CreateAPIView):
    model = Organization
    queryset = Organization.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationSerializer


# Update Organization.
class OrganizationUpdateSet(UpdateAPIView):
    model = Organization
    queryset = Organization.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OrganizationSerializer


# Domain List.
class DomainViewSet(ListAPIView):
    model = Domain
    permission_classes = (IsAuthenticated,)
    serializer_class = DomainSerializer

    def get_queryset(self):
        related_organization_id = self.kwargs['related_organization_id']
        return Domain.objects.filter(related_organization_id__exact=related_organization_id,
                                     invisible__exact=False).order_by('id')


# Domain Detail.
class DomainDetailSet(RetrieveAPIView):
    model = Domain
    queryset = Domain.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DomainSerializer


# Add new Domain.
class DomainCreateSet(CreateAPIView):
    model = Domain
    queryset = Domain.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DomainSerializer


# Update Domain.
class DomainUpdateSet(UpdateAPIView):
    model = Domain
    queryset = Domain.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = DomainSerializer


# Subdomain List.
class SubdomainViewSet(ListAPIView):
    model = Subdomain
    queryset = Subdomain.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubdomainSerializer

    def get_queryset(self):
        related_organization_id = self.kwargs['related_organization_id']
        related_domain_id = self.kwargs['related_domain_id']
        return Subdomain.objects.filter(related_organization_id__exact=related_organization_id,
                                        related_domain_id__exact=related_domain_id,
                                        invisible__exact=False).order_by('id')


# Subdomain Detail.
class SubdomainDetailSet(RetrieveAPIView):
    model = Subdomain
    queryset = Subdomain.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubdomainSerializer


# Add new Subdomain.
class SubdomainCreateSet(CreateAPIView):
    model = Subdomain
    queryset = Subdomain.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubdomainSerializer


# Update Subdomain.
class SubdomainUpdateSet(UpdateAPIView):
    model = Subdomain
    queryset = Subdomain.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = SubdomainSerializer


# Top Page (Dashboard).
def top_page(request):
    organizations = Organization.objects.all().order_by('id')
    return render(request, 'gyoithon/index.html', {'organizations': organizations})


# Top Page (Dashboard).
def registration(request):
    if request.method == 'POST':
        form = RegistrationOrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.save()
            messages.success(request, 'You have registered a new organization: "{}".'.format(organization.name))
            return redirect('gyoithon:top_page')
    else:
        form = RegistrationOrganizationForm()

    return render(request, 'gyoithon/registration.html', {'form': form})


# Organization list.
def list_organization(request):
    organizations = Organization.objects.all().order_by('id')
    return render(request, 'gyoithon/list_organization.html', {'organizations': organizations})


# Edit Organization.
def edit_organization(request, organization_id=None):
    if organization_id:
        organization = get_object_or_404(Organization, pk=organization_id)
    else:
        organization = Organization()

    if request.method == 'POST':
        form = UpdateOrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.save()
            messages.success(request, 'Update organization: {}.{}'.format(organization_id, organization.name))
            domains = Domain.objects.filter(related_organization_id__exact=organization.id).order_by('id')
            return render(request, 'gyoithon/detail_organization.html', {'organization': organization,
                                                                         'domains': domains})
    else:
        form = UpdateOrganizationForm(instance=organization)

    return render(request, 'gyoithon/edit_organization.html', dict(organization=organization,
                                                                   form=form,
                                                                   organization_id=organization_id))


# Delete organization.
def delete_organization(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    organization.invisible = True
    organization.save()
    messages.success(request, 'Delete organization "{}.{}"'.format(organization_id, organization.name))
    return redirect('gyoithon:top_page')


# Organization detail.
def detail_organization(request, organization_id):
    if organization_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domains = Domain.objects.filter(related_organization_id__exact=organization.id).order_by('id')
        return render(request, 'gyoithon/detail_organization.html', {'organization': organization,
                                                                     'domains': domains})
    else:
        return redirect('gyoithon:top_page')


# Registration domain.
def registration_domain(request, organization_id):
    if organization_id:
        organization = get_object_or_404(Organization, pk=organization_id)
    else:
        return redirect('gyoithon:top_page')

    if request.method == 'POST':
        form = RegistrationDomainForm(request.POST)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.related_organization_id = organization_id
            domain.save()
            messages.success(request, 'You added new domain: "{}".'.format(domain.name))
            domains = Domain.objects.filter(related_organization_id__exact=organization_id,
                                            invisible__exact=False).order_by('id')
            organization.domain = len(domains)
            organization.save()
            return render(request, 'gyoithon/detail_organization.html', {'organization': organization,
                                                                         'domains': domains})
    else:
        form = RegistrationDomainForm()
        form.organization_id = organization_id

    return render(request, 'gyoithon/registration_domain.html', {'form': form,
                                                                 'organization': organization})


# Edit domain.
def edit_domain(request, organization_id, domain_id):
    if organization_id and domain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)
    else:
        domain = Domain()

    if request.method == 'POST':
        form = UpdateDomainForm(request.POST, instance=domain)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.save()
            messages.success(request, 'Update domain: {}.{}'.format(domain.id, domain.name))
            subdomains = Subdomain.objects.filter(related_organization_id__exact=organization_id,
                                                  related_domain_id__exact=domain_id).order_by('id')
            return render(request, 'gyoithon/detail_domain.html', {'organization': organization,
                                                                   'domain': domain,
                                                                   'subdomains': subdomains})
    else:
        form = UpdateDomainForm(instance=domain)

    return render(request, 'gyoithon/edit_domain.html', {'form': form,
                                                         'organization': organization,
                                                         'domain': domain})


# Delete domain.
def delete_domain(request, organization_id, domain_id):
    if organization_id and domain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)
    else:
        return redirect('gyoithon:top_page')

    domain.invisible = True
    domain.save()
    messages.success(request, 'Delete domain "{}.{}"'.format(domain_id, domain.name))
    organization.domain -= 1
    organization.save()

    return redirect('gyoithon:top_page')


# Domain detail.
def detail_domain(request, organization_id, domain_id):
    if organization_id and domain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)
        subdomains = Subdomain.objects.filter(related_organization_id__exact=organization_id,
                                              related_domain_id__exact=domain_id).order_by('name')
        return render(request, 'gyoithon/detail_domain.html', {'organization': organization,
                                                               'domain': domain,
                                                               'subdomains': subdomains})
    else:
        return redirect('gyoithon:top_page')


# Registration subdomain.
def registration_subdomain(request, organization_id, domain_id):
    if organization_id and domain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)
    else:
        return redirect('gyoithon:top_page')

    if request.method == 'POST':
        form = RegistrationSubdomainForm(request.POST)
        if form.is_valid():
            # Update Subdomain.
            subdomain = form.save(commit=False)
            subdomain.related_organization_id = organization_id
            subdomain.related_domain_id = domain_id
            subdomain.save()
            messages.success(request, 'You added new subdomain: "{}".'.format(subdomain.name))
            all_subdomains = Subdomain.objects.filter(related_organization_id__exact=organization_id,
                                                      invisible__exact=False).order_by('name')
            domain_subdomains = Subdomain.objects.filter(related_organization_id__exact=organization_id,
                                                         related_domain_id__exact=domain_id,
                                                         invisible_exact=False).order_by('name')
            organization.subdomain = len(all_subdomains)
            organization.save()
            domain.subdomain = len(domain_subdomains)
            domain.save()
            return render(request, 'gyoithon/detail_domain.html', {'organization': organization,
                                                                   'domain': domain,
                                                                   'subdomains': domain_subdomains})
    else:
        form = RegistrationSubdomainForm()
        form.related_organization_id = organization_id
        form.related_domain_id = domain_id

    return render(request, 'gyoithon/registration_subdomain.html', {'form': form,
                                                                    'organization': organization,
                                                                    'domain': domain})


# Edit subdomain.
def edit_subdomain(request, organization_id, domain_id, subdomain_id):
    if organization_id and domain_id and subdomain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)
        subdomain = get_object_or_404(Subdomain,
                                      pk=subdomain_id,
                                      related_organization_id=organization_id,
                                      related_domain_id=domain_id)
    else:
        subdomain = Subdomain()

    if request.method == 'POST':
        form = UpdateSubdomainForm(request.POST, instance=subdomain)
        if form.is_valid():
            subdomain = form.save(commit=False)
            subdomain.save()
            messages.success(request, 'Update subdomain: {}.{}'.format(subdomain.id, subdomain.name))
            return render(request, 'gyoithon/detail_subdomain.html', {'organization': organization,
                                                                      'domain': domain,
                                                                      'subdomain': subdomain})
    else:
        form = UpdateSubdomainForm(instance=subdomain)

    return render(request, 'gyoithon/edit_subdomain.html', {'form': form,
                                                            'organization': organization,
                                                            'domain': domain,
                                                            'subdomain': subdomain})


# Delete subdomain.
def delete_subdomain(request, organization_id, domain_id, subdomain_id):
    if organization_id and subdomain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)
    else:
        return redirect('gyoithon:top_page')

    subdomain = get_object_or_404(Subdomain,
                                  pk=subdomain_id,
                                  related_organization_id=organization_id,
                                  related_domain_id=domain_id)
    subdomain.invisible = True
    subdomain.save()
    messages.success(request, 'Delete subdomain "{}.{}"'.format(subdomain_id, subdomain.name))
    organization.subdomain -= 1
    organization.save()
    domain.subdomain -= 1
    domain.save()
    return redirect('gyoithon:top_page')


# Subdomain detail.
def detail_subdomain(request, organization_id, domain_id, subdomain_id):
    if organization_id and domain_id and subdomain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)
        subdomain = get_object_or_404(Subdomain,
                                      pk=subdomain_id,
                                      related_organization_id=organization_id,
                                      related_domain_id=domain_id)
        return render(request, 'gyoithon/detail_subdomain.html', {'organization': organization,
                                                                  'domain': domain,
                                                                  'subdomain': subdomain})
    else:
        return redirect('gyoithon:top_page')


# Search Domain.
def search_domain(request, organization_id):
    if organization_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        messages.warning(request, 'Not Implementation Search Domain for "{}"'.format(organization.name))
        return redirect('gyoithon:top_page')
    else:
        return redirect('gyoithon:top_page')


# Search Subdomain.
def search_subdomain(request, organization_id, domain_id):
    utility = Utilty()
    if organization_id and domain_id:
        organization = get_object_or_404(Organization, pk=organization_id)
        domain = get_object_or_404(Domain, pk=domain_id, related_organization_id=organization_id)

        # Execution.
        executation_type = 'search_subdomain'
        command_option = utility.build_command(executation_type)
        command = 'python3 {}gyoithon.py {}'.format(settings.GYOITHON_DIR, command_option)
        executation.delay('{}'.format(command))

        # Update to ScanResult.
        organization.status = 1
        organization.save()
        domain.status = 1
        domain.save()

        return redirect('gyoithon:top_page')
    else:
        return redirect('gyoithon:top_page')
