<template xmlns="http://www.w3.org/1999/html">
  <section>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/top">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page"><a href="/top">Organization List</a></li>
        <li class="breadcrumb-item active" aria-current="page"><NuxtLink :to="`/organization/${organization.id}/`">{{ organization.name }}</NuxtLink></li>
        <li class="breadcrumb-item active" aria-current="page"><NuxtLink :to="`/organization/${organization.id}/domain/${domain.id}/`">{{ domain.name }}</NuxtLink></li>
        <li class="breadcrumb-item active" aria-current="page">{{ subdomain.name }}</li>
      </ol>
    </nav>

    <h1 class="h2">{{ subdomain.name }}</h1>
    <p>{{ subdomain.overview }}</p>

    <div class="col-12 col-xl-12 mb-4 mb-lg-0">
      <div class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table">
              <tr>
                <th>Registration Date:</th>
                <td>{{ subdomain.registration_date | formatDate }}</td>
              </tr>
              <tr>
                <th>IP Address:</th>
                <td v-html="subdomain.ip_address.replace(/\n/g,'<br/>')">{{ subdomain.ip_address }}</td>
              <tr>
                <th>Environment:</th>
                <td>{{ subdomain.production | exchangeProduction }}</td>
              </tr>
              <tr>
                <th>Cloud Type:</th>
                <td>{{ subdomain.cloud_type | exchangeCloudType }}</td>
              </tr>
              <tr>
                <th>HTTP Accessible:</th>
                <td>{{ subdomain.http_accessible }}</td>
              </tr>
              <tr>
                <th>HTTPS Accessible	:</th>
                <td>{{ subdomain.https_accessible }}</td>
              </tr>
              <tr>
                <th>DNS Record:</th>
                <td v-html="subdomain.dns_a_record.replace(/\n/g,'<br/>')">{{ subdomain.dns_a_record }}</td>
              </tr>
              <tr>
                <th>Rank:</th>
                <td>{{ subdomain.rank | exchangeRank }}</td>
              </tr>
              <tr>
                <th>Status:</th>
                <td>{{ subdomain.status | exchangeStatus }}</td>
              </tr>
              <tr>
                <th colspan="2">
                  <div class="form-group row">
                    <div class="col-sm-offset-2 col-sm-10">
                      <button @click="openUpdateSubdomain()" type="submit" class="btn btn-info">Update</button>
                      <button type="submit" class="btn btn-warning">Assess</button>
                    </div>
                  </div>
                </th>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Update Subdomain. -->
    <modal name="modal-subdomain-update" height="auto" weight="auto" :scrollable="true" :draggable="true">
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
              <button type="submit" class="btn btn-primary" @click.prevent="updateSubdomain()">Update</button>
              <button type="submit" class="btn btn-danger" @click.prevent="closeUpdateSubdomain()">Cancel</button>
            </div>
          </div>
        </form>
      </div>
    </modal>

    <hr>
    <h1 class="h2">Assessment Results</h1>
    <p>Assessment Results of {{ subdomain.name }}.</p>
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
                  <NuxtLink class="btn btn-primary btn-sm" :to="`/subdomain/${subdomain.id}/`">View</NuxtLink>
                  <button @click="hideSubdomain(subdomain)" class="btn btn-danger btn-sm">Hide</button>
                </td>
              </tr>
              <tr>
                <td colspan="10">
                  <button type="submit" class="btn btn-primary">Registration</button>
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
      title: "Subdomain Detail",
      meta: [
        {
          name: 'description',
          content: 'Subdomain Detail'
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
      subdomain: {
        name: "",
        registration_date: "",
        ip_address: "",
        http_accessible: "",
        https_accessible: "",
        dns_a_record: "",
        rank: "",
        status: "",
        related_organization_id: "",
        related_domain_id: "",
      },
    }
  },
  watch: {
    '$route.query': '$asyncData'
  },

  async asyncData({ params }) {
    try {
      const subdomain = await SubdomainAPI.getSubdomain(params.id)
      const organization = await OrganizationAPI.getOrganization(subdomain.related_organization_id)
      const domain = await DomainAPI.getDomain(subdomain.related_domain_id)
      return { organization, domain, subdomain }
    } catch (e) {
      return { organization: [], domain: [], subdomain: [] }
    }
  },

  methods :{
    /* Open modal window for updating Subdomain. */
    async openUpdateSubdomain() {
      this.$modal.show("modal-subdomain-update");
    },
    /* Hide modal window for updating Subdomain. */
    async closeUpdateSubdomain() {
      this.$modal.hide("modal-subdomain-update");
    },
    /* Submit form for updating Subdomain. */
    async updateSubdomain() {
      const updatedSubdomain = this.subdomain
      const formData = new FormData()
      for (const data in updatedSubdomain) {
        formData.append(data, updatedSubdomain[data])
      }
      await SubdomainAPI.updateSubdomain(this.subdomain.related_organization_id, this.subdomain.related_domain_id, formData)
      await this.closeUpdateSubdomain()
    },
  }
}
</script>
