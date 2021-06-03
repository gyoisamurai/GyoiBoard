<template xmlns="http://www.w3.org/1999/html">
  <section>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/top">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page"><a href="/top">Organization List</a></li>
        <li class="breadcrumb-item active" aria-current="page"><NuxtLink :to="`/organization/${organization.id}/`">{{ organization.name }}</NuxtLink></li>
        <li class="breadcrumb-item active" aria-current="page">{{ domain.name }}</li>
      </ol>
    </nav>

    <h1 class="h2">{{ domain.name }}</h1>
    <p>{{ domain.overview }}</p>

    <div class="col-12 col-xl-12 mb-4 mb-lg-0">
      <div class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table">
              <tr>
                <th>Registration Date:</th>
                <td>{{ domain.registration_date | formatDate }}</td>
              </tr>
              <tr>
                <th>Registrar:</th>
                <td>{{ domain.registrar }}</td>
              <tr>
                <th>Administrative Contact:</th>
                <td>{{ domain.administrative_contact }}</td>
              </tr>
              <tr>
                <th>Registrant Name:</th>
                <td>{{ domain.registrant_name }}</td>
              </tr>
              <tr>
                <th>Registrant Organization:</th>
                <td>{{ domain.registrant_organization }}</td>
              </tr>
              <tr>
                <th>Registrant Email:</th>
                <td>{{ domain.registrant_email }}</td>
              </tr>
              <tr>
                <th>Admin Name:</th>
                <td>{{ domain.admin_name | exchangeStatus }}</td>
              </tr>
              <tr>
                <th>Admin Organization:</th>
                <td>{{ domain.admin_organization }}</td>
              </tr>
              <tr>
                <th>Admin Email:</th>
                <td>{{ domain.admin_email }}</td>
              </tr>
              <tr>
                <th>Tech Name:</th>
                <td>{{ domain.tech_name }}</td>
              </tr>
              <tr>
                <th>Tech Organization:</th>
                <td>{{ domain.tech_organization }}</td>
              </tr>
              <tr>
                <th>Tech Email:</th>
                <td>{{ domain.tech_email }}</td>
              </tr>
              <tr>
                <th>Name Server:</th>
                <td v-html="domain.name_server.replace(/\n/g,'<br/>')">{{ domain.name_server }}</td>
              </tr>
              <tr>
                <th>Subdomains:</th>
                <td>{{ domain.subdomain }}</td>
              </tr>
              <tr>
                <th>Rank:</th>
                <td>{{ domain.rank | exchangeRank }}</td>
              </tr>
              <tr>
                <th>Status:</th>
                <td>{{ domain.status | exchangeStatus }}</td>
              </tr>
              <tr>
                <th colspan="2">
                  <div class="form-group row">
                    <div class="col-sm-offset-2 col-sm-10">
                      <button @click="openUpdateDomain()" type="submit" class="btn btn-info">Update</button>
                      <button type="submit" class="btn btn-success">Search Subdomain</button>
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

    <!-- Update Domain. -->
    <modal name="modal-domain-update" height="auto" weight="auto" :scrollable="true" :draggable="true">
      <div class="modal-header">
        <h1 class="my-3 text-3xl font-semibold text-gray-700">Domain Update</h1>
      </div>
      <div class="modal-body">
        <p>You can update domain information.</p>
        <form class="form-horizontal">
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.name" name="name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Registrar:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.registrar" name="registrar">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Administrative Contact:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.administrative_contact" name="administrative_contact">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Registrant Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.registrant_name" name="registrant_name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Registrant Organization:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.registrant_organization" name="registrant_organization">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Registrant Email:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.registrant_email" name="registrant_email">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Admin Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.admin_name" name="admin_name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Admin Organization:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.admin_organization" name="admin_organization">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Admin Email:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.admin_email" name="admin_email">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Tech Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.tech_name" name="tech_name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Tech Organization:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.tech_organization" name="tech_organization">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Tech Email:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" v-model="domain.tech_email" name="tech_email">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="region">Name Server:</label>
            <div class="col-sm-10">
              <textarea id="name_server" v-model="domain.name_server" name="name_server" rows="5" class="form-control">
              </textarea>
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="overview">Overview:</label>
            <div class="col-sm-10">
              <textarea id="overview" v-model="domain.overview" name="overview" rows="5" class="form-control">
              </textarea>
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-primary" @click.prevent="updateDomain()">Update</button>
              <button type="submit" class="btn btn-danger" @click.prevent="closeUpdateDomain()">Cancel</button>
            </div>
          </div>
        </form>
      </div>
    </modal>

    <!-- Add new Subdomain. -->
    <modal name="modal-subdomain-registration" height="auto" :scrollable="true" :draggable="true">
      <div class="modal-header">
        <h1 class="my-3 text-3xl font-semibold text-gray-700">Subdomain Registration</h1>
      </div>
      <div class="modal-body">
        <p>You can register a new subdomain.</p>
        <form class="form-horizontal">
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">Name:</label>
            <div class="col-sm-10">
              <input type="text" class="form-control" id="name" v-model="subdomains.name" name="name" placeholder="Subdomain Name">
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="name">IP Address:</label>
            <div class="col-sm-10">
              <textarea v-model="subdomains.ip_address" name="ip_address" rows="5" placeholder="IP Address" class="form-control">
              </textarea>
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="industry">Production Environment:</label>
            <div class="col-sm-10">
              <select class="form-select" v-model="subdomains.production" name="production">
                <option selected value="0">-----</option>
                <option value="1">Development</option>
                <option value="2">Production</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="industry">Cloud Type:</label>
            <div class="col-sm-10">
              <select class="form-select" v-model="subdomains.cloud_type" name="cloud_type">
                <option selected value="0">-----</option>
                <option value="1">Amazon Web Service</option>
                <option value="2">Google Cloud Platform</option>
                <option value="3">Microsoft Azure</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="control-label col-sm-2" for="overview">Overview:</label>
            <div class="col-sm-10">
              <textarea v-model="subdomains.overview" name="overview" rows="5" placeholder="Overview" class="form-control">
              </textarea>
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-offset-2 col-sm-10">
              <button type="submit" class="btn btn-primary" @click.prevent="addSubdomain(organization.id, domain.id)">Registration</button>
              <button type="submit" class="btn btn-danger" @click.prevent="closeRegistrationSubdomain()">Cancel</button>
            </div>
          </div>
        </form>
      </div>
    </modal>

    <hr>
    <h1 class="h2">Subdomain List</h1>
    <p>A subdomain list of {{ domain.name }}.</p>
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
                <th>IP Address</th>
                <th>HTTP Accessible</th>
                <th>HTTPS Accessible</th>
                <th>Rank</th>
                <th>Status</th>
                <th colspan="2"></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="subdomain of subdomains" :key="domain.id" @click="$data.subdomain = subdomain" v-if="!subdomain.invisible">
                <th scope="row">{{ subdomain.id }}</th>
                <td>{{ subdomain.name }}</td>
                <td>{{ subdomain.registration_date | formatDate }}</td>
                <td>{{ subdomain.ip_address }}</td>
                <td>{{ subdomain.http_accessible }}</td>
                <td>{{ subdomain.https_accessible }}</td>
                <td>{{ subdomain.rank | exchangeRank }}</td>
                <td>{{ subdomain.status | exchangeStatus }}</td>
                <td>
                  <input type="checkbox" name="
                  bulk_vulnerability_assessment" value="1">
                </td>
                <td>
                  <NuxtLink class="btn btn-primary btn-sm" :to="`./subdomain/${subdomain.id}/`">View</NuxtLink>
                  <button @click="hideSubdomain(organization.id, domain.id, subdomain)" class="btn btn-danger btn-sm">Hide</button>
                  <button type="submit" class="btn btn-warning btn-sm">Report</button>
                </td>
              </tr>
              <tr>
                <td colspan="10">
                  <button @click="openRegistrationSubdomain()" type="submit" class="btn btn-primary">Registration</button>
                  <button type="submit" class="btn btn-warning">Assess</button>
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
import OrganizationAPI from '~/plugins/organization';
import DomainAPI from '~/plugins/domain';
import SubdomainAPI from '~/plugins/subdomain';

export default {
  middleware: ['auth'],
  computed: {
    state () {
      return JSON.stringify(this.$auth.$state, undefined, 2)
    }
  },
  head() {
    return {
      title: "Domain Detail",
      meta: [
        {
          name: 'description',
          content: 'Domain Detail'
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
      subdomains: {},
      subdomain: {
        name: "",
        registration_date: "",
        ip_address: "",
        production: "",
        cloud_type: "",
        http_accessible: "",
        https_accessible: "",
        rank: "",
        status: "",
      },
    }
  },
  watch: {
    '$route.query': '$asyncData'
  },

  async asyncData({ params }) {
    try {
      const domain = await DomainAPI.getDomain(params.id)
      const organization = await OrganizationAPI.getOrganization(domain.related_organization_id)
      const subdomains = await SubdomainAPI.getSubdomains(domain.related_organization_id, domain.id)
      return { organization, domain, subdomains }
    } catch (e) {
      return { organization: [], domain: [], subdomains: [] }
    }
  },

  methods :{
    /* Open modal window for updating Domain. */
    async openUpdateDomain() {
      this.$modal.show("modal-domain-update");
    },
    /* Hide modal window for updating Domain. */
    async closeUpdateDomain() {
      this.$modal.hide("modal-domain-update");
    },
    /* Submit form for updating Domain. */
    async updateDomain() {
      const updatedDomain = this.domain
      const formData = new FormData()
      for (const data in updatedDomain) {
        formData.append(data, updatedDomain[data])
      }
      await DomainAPI.updateDomain(this.domain.related_organization_id, this.domain.id, formData)
      await this.closeUpdateDomain()
    },
    /* Open modal window for registration Subdomain. */
    async openRegistrationSubdomain() {
      this.$modal.show("modal-subdomain-registration");
    },
    /* Hide modal window for registration Subdomain. */
    async closeRegistrationSubdomain() {
      this.$modal.hide("modal-subdomain-registration");
    },
    /* Submit form for adding Subdomain. */
    async addSubdomain(organization_id, domain_id) {
      const formData = new FormData()
      for (const data in this.subdomains) {
        formData.append(data, this.subdomains[data])
      }
      formData.append('related_organization_id', organization_id)
      formData.append('related_domain_id', domain_id)
      await SubdomainAPI.addSubdomain(organization_id, domain_id, formData)
      this.domain = await DomainAPI.getDomain(domain_id)
      this.subdomains = await SubdomainAPI.getSubdomains(organization_id, domain_id)
      await this.closeRegistrationSubdomain()
    },
    /* Hide specific Subdomain. */
    async hideSubdomain(organization_id, domain_id, hide_subdomain) {
      hide_subdomain.invisible = true;
      await SubdomainAPI.updateSubdomain(organization_id, domain_id, hide_subdomain)
      this.domain = await DomainAPI.getDomain(domain_id)
      this.subdomains = await SubdomainAPI.getSubdomains(organization_id, domain_id)
    },
  }
}
</script>
