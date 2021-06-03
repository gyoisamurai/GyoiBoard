<template>
  <section>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/top">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page"><a href="/top">Organization List</a></li>
        <li class="breadcrumb-item active" aria-current="page">{{ organization.name }}</li>
      </ol>
    </nav>

    <h1 class="h2">{{ organization.name }}</h1>
    <p>{{ organization.overview }}</p>

    <div class="col-12 col-xl-12 mb-4 mb-lg-0">
      <div class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table">
              <tr>
                <th>Registration Date:</th>
                <td>{{ organization.registration_date | formatDate }}</td>
              </tr>
              <tr>
                <th>Region:</th>
                <td>{{ organization.region | exchangeRegion }}</td>
              <tr>
                <th>Industry:</th>
                <td>{{ organization.industry | exchangeIndustry }}</td>
              </tr>
              <tr>
                <th>Domains:</th>
                <td>{{ organization.domain }}</td>
              </tr>
              <tr>
                <th>Subdomains:</th>
                <td>{{ organization.subdomain }}</td>
              </tr>
              <tr>
                <th>Rank:</th>
                <td>{{ organization.rank | exchangeRank }}</td>
              </tr>
              <tr>
                <th>Status:</th>
                <td>{{ organization.status | exchangeStatus }}</td>
              </tr>
              <tr>
                <th colspan="2">
                  <div class="form-group row">
                    <div class="col-sm-offset-2 col-sm-10">
                      <button @click="openUpdateOrganization()" type="submit" class="btn btn-info">Update</button>
                      <button type="submit" class="btn btn-success">Search Domain</button>
                      <button type="submit" class="btn btn-warning">Show Report</button>
                    </div>
                  </div>
                </th>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Update Organization. -->
    <modal name="modal-organization-update" height="auto" :scrollable="true" :draggable="true">
      <div class="modal-header">
        <h1 class="my-3 text-3xl font-semibold text-gray-700">Organization Update</h1>
      </div>
      <div class="modal-body">
        <p>You can update organization information.</p>
        <form class="form-horizontal">
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="organization.name" name="name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Region:</label>
            <div class="col-sm-10">
              <select class="form-select" v-model="organization.region" name="region">
                <option selected value="0">-----</option>
                <option value="1">Domestic</option>
                <option value="2">Abroad</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="industry">Industry:</label>
            <div class="col-sm-10">
              <select class="form-select" v-model="organization.industry" name="industry">
                <option selected value="0">-----</option>
                <option value="1">Energy</option>
                <option value="2">Materials</option>
                <option value="3">Industrials</option>
                <option value="4">Consumer Discretionary</option>
                <option value="5">Consumer Staples</option>
                <option value="6">Health Care</option>
                <option value="7">Financials</option>
                <option value="8">Information Technology</option>
                <option value="9">Communication Services</option>
                <option value="10">Utilities</option>
                <option value="11">Real Estate</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="overview">Overview:</label>
            <div class="col-sm-10">
              <textarea id="overview" v-model="organization.overview" name="overview" rows="5" class="form-control">
              </textarea>
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-primary" @click.prevent="updateOrganization()">Update</button>
              <button type="submit" class="btn btn-danger" @click.prevent="closeUpdateOrganization()">Cancel</button>
            </div>
          </div>
        </form>
      </div>
    </modal>

    <!-- Add new Domain. -->
    <modal name="modal-domain-registration" height="auto" :scrollable="true" :draggable="true">
      <div class="modal-header">
        <h1 class="my-3 text-3xl font-semibold text-gray-700">Domain Registration</h1>
      </div>
      <div class="modal-body">
        <p>You can register a new domain.</p>
        <form class="form-horizontal">
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="name" v-model="domains.name" name="name" placeholder="Domain Name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Registrar:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="registrar" v-model="domains.registrar" name="registrar" placeholder="Registrar">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Administrative Contact:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="administrative_contact" v-model="domains.administrative_contact " name="administrative_contact" placeholder="Administrative Contact">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Registrant Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="registrant_name" v-model="domains.registrant_name" name="registrant_name" placeholder="Registrant Name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Registrant Organization:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="registrant_organization" v-model="domains.registrant_organization" name="registrant_organization" placeholder="Registrant Organization">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Registrant Email:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="registrant_email" v-model="domains.registrant_email" name="registrant_email" placeholder="Registrant Email">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Admin Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="admin_name" v-model="domains.admin_name" name="admin_name" placeholder="Admin Name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Admin Organization:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="admin_organization" v-model="domains.admin_organization" name="admin_organization" placeholder="Admin Organization">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Admin Email:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="admin_email" v-model="domains.admin_email" name="admin_email" placeholder="Admin Email">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Tech Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="tech_name" v-model="domains.tech_name" name="tech_name" placeholder="Tech Name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Tech Organization:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="tech_organization" v-model="domains.tech_organization" name="tech_organization" placeholder="Tech Organization">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Tech Email:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="tech_email" v-model="domains.tech_email" name="tech_email" placeholder="Tech Email">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Name Server:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="name_server" v-model="domains.name_server" name="name_server" placeholder="Name Server">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="overview">Overview:</label>
            <div class="col-sm-10">
              <textarea v-model="domains.overview" name="overview" rows="5" placeholder="Overview" class="form-control">
              </textarea>
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-primary" @click.prevent="addDomain(organization.id)">Registration</button>
              <button type="submit" class="btn btn-danger" @click.prevent="closeRegistrationDomain()">Cancel</button>
            </div>
          </div>
        </form>
      </div>
    </modal>

    <hr>
    <h1 class="h2">Domain List</h1>
    <p>A domain list of {{ organization.name }}.</p>
    <div class="col-12 col-xl-12 mb-4 mb-lg-0">
      <div class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table">
              <thead>
              <tr>
                <th>No</th>
                <th>Name</th>
                <th>Registration Date</th>
                <th>Registrant Organization</th>
                <th>Registrant Email</th>
                <th>Subdomains</th>
                <th>Rank</th>
                <th>Status</th>
                <th colspan="2"></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="domain of domains" :key="organization.id" @click="$data.domain = domain" v-if="!domain.invisible">
                <th scope="row">{{ domain.id }}</th>
                <td>{{ domain.name }}</td>
                <td>{{ domain.registration_date | formatDate }}</td>
                <td>{{ domain.registrant_organization }}</td>
                <td>{{ domain.registrant_email }}</td>
                <td>{{ domain.subdomain }}</td>
                <td>{{ domain.rank | exchangeRank }}</td>
                <td>{{ domain.status | exchangeStatus }}</td>
                <td>
                  <input type="checkbox" name="
                  bulk_vulnerability_assessment" value="1">
                </td>
                <td>
                  <NuxtLink class="btn btn-primary btn-sm" :to="`./domain/${domain.id}/`">View</NuxtLink>
                  <button @click="hideDomain(domain)" class="btn btn-danger btn-sm">Hide</button>
                  <button type="submit" class="btn btn-warning btn-sm">Report</button>
                </td>
              </tr>
              <tr>
                <td colspan="10">
                  <button @click="openRegistrationDomain()" type="submit" class="btn btn-primary">Registration</button>
                  <button type="submit" class="btn btn-success">Search Subdomain</button>
                  <button type="submit" class="btn btn-warning">Assess</button>
                  <button type="submit" class="btn btn-dark">Search & Assess</button>
                  <button type="submit" class="btn btn-secondary">Hidden Domain</button>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import OrganizationAPI from '@/plugins/organization';
import DomainAPI from '@/plugins/domain';

export default {
  middleware: ['auth'],
  computed: {
    state () {
      return JSON.stringify(this.$auth.$state, undefined, 2)
    }
  },
  head() {
    return {
      title: "Organization Detail",
      meta: [
        {
          name: 'description',
          content: 'Organization Detail'
        },
      ],
    }
  },
  data() {
    return {
      organization: {
        name: "",
        region: "",
        industry: "",
        overview: "",
      },
      domains: {},
      domain: {
        name: "",
        overview: "",
        registrar: "",
        registration_date: "",
        administrative_contact: "",
        registrant_name: "",
        registrant_organization: "",
        registrant_email: "",
        admin_name: "",
        admin_organization: "",
        admin_email: "",
        tech_name: "",
        tech_organization: "",
        tech_email: "",
        name_server: "",
        subdomain: "",
        rank: "",
        status: "",
        related_organization_id: "",
      },
    }
  },
  watch: {
    '$route.query': '$asyncData'
  },

  async asyncData({ params }) {
    try {
      const organization = await OrganizationAPI.getOrganization(params.id)
      const domains = await DomainAPI.getDomains(params.id)
      return { organization, domains }
    } catch (e) {
      return { organization: [], domains: [] }
    }
  },

  methods :{
    /* Open modal window for updating Organization. */
    async openUpdateOrganization() {
      this.$modal.show("modal-organization-update");
    },
    /* Hide modal window for updating Organization. */
    async closeUpdateOrganization() {
      this.$modal.hide("modal-organization-update");
    },
    /* Submit form for updating Organization. */
    async updateOrganization() {
      const updatedOrganization = this.organization
      const formData = new FormData()
      for (const data in updatedOrganization) {
        formData.append(data, updatedOrganization[data])
      }
      await OrganizationAPI.updateOrganization(this.organization.id, formData)
      await this.closeUpdateOrganization()
    },
    /* Open modal window for registration Domain. */
    async openRegistrationDomain() {
      this.$modal.show("modal-domain-registration");
    },
    /* Hide modal window for registration Domain. */
    async closeRegistrationDomain() {
      this.$modal.hide("modal-domain-registration");
    },
    /* Submit form for adding Domain. */
    async addDomain(organization_id) {
      const formData = new FormData()
      for (const data in this.domains) {
        formData.append(data, this.domains[data])
      }
      formData.append('related_organization_id', organization_id)
      await DomainAPI.addDomain(organization_id, formData)
      this.organization = await OrganizationAPI.getOrganization(organization_id)
      this.domains = await DomainAPI.getDomains(organization_id)
      await this.closeRegistrationDomain()
    },
    /* Hide specific Organization. */
    async hideDomain(hide_domain) {
      hide_domain.invisible = true;
      await DomainAPI.updateDomain(this.organization.id, hide_domain.id, hide_domain)
      this.organization = await OrganizationAPI.getOrganization(this.organization.id)
      this.domains = await DomainAPI.getDomains(this.organization.id)
    },
  }
}
</script>
