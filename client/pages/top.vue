<template>
  <section>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item"><a href="/top">Home</a></li>
        <li class="breadcrumb-item active" aria-current="page">Organization List</li>
      </ol>
    </nav>

    <h1 class="h2">Organization List</h1>
    <p>This is the organization list.</p>

    <div class="col-12 col-xl-12 mb-4 mb-lg-0">
      <div class="card">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table">
              <thead>
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Organization</th>
                <th scope="col">Registration date</th>
                <th scope="col">Domains</th>
                <th scope="col">Subdomains</th>
                <th scope="col">Rank</th>
                <th scope="col">Status</th>
                <th scope="col" colspan="2"></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="organization of organizations" :key="organization.id" @click="$data.organization = organization" v-if="!organization.invisible">
                <td>{{ organization.id }}</td>
                <td>{{ organization.name }}</td>
                <td>{{ organization.registration_date | formatDate }}</td>
                <td>{{ organization.domain }}</td>
                <td>{{ organization.subdomain }}</td>
                <td>{{ organization.rank | exchangeRank }}</td>
                <td>{{ organization.status | exchangeStatus }}</td>
                <td>
                  <input type="checkbox" name="bulk_vulnerability_assessment" value="1">
                </td>
                <td>
                  <NuxtLink class="btn btn-primary btn-sm" :to="`/organization/${organization.id}/`">View</NuxtLink>
                  <button @click="hideOrganization(organization)" class="btn btn-danger btn-sm">Hide</button>
                </td>
              </tr>
              <tr>
                <td colspan="9">
                  <button @click="openRegistration()" type="submit" class="btn btn-primary">Registration</button>
                  <button type="submit" class="btn btn-success">Search Domain/Subdomain</button>
                  <button type="submit" class="btn btn-warning">Assess</button>
                  <button type="submit" class="btn btn-dark">Search & Assess</button>
                  <button type="submit" class="btn btn-secondary">Hidden List</button>
                </td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Add new Organization. -->
      <modal name="modal-organization-registration" height="auto" :scrollable="true" :draggable="true">
        <div class="modal-header">
          <h1 class="my-3 text-3xl font-semibold text-gray-700">Organization Registration</h1>
        </div>
        <div class="modal-body">
          <p>You can register a new organization.</p>
          <form class="form-horizontal">
            <div class="form-group">
              <label class="control-label col-sm-2" for="name">Name:</label>
              <div class="col-sm-10">
                <input type="text" class="form-control" id="name" v-model="organizations.name" name="name" placeholder="Organization Name" required>
              </div>
            </div>
            <div class="form-group">
              <label class="control-label col-sm-2" for="region">Region:</label>
              <div class="col-sm-10">
                <select class="form-select" id="region" v-model="organizations.region" name="region">
                  <option selected value="0">-----</option>
                  <option value="1">Domestic</option>
                  <option value="2">Abroad</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label class="control-label col-sm-2" for="industry">Industry:</label>
              <div class="col-sm-10">
                <select class="form-select" v-model="organizations.industry" name="industry">
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
                <textarea v-model="organizations.overview" name="overview" rows="5" placeholder="Overview" class="form-control" required>
                </textarea>
              </div>
            </div>
            <div class="form-group row">
              <div class="col-sm-offset-2 col-sm-10">
                <button type="submit" class="btn btn-primary" @click.prevent="addOrganization()">Registration</button>
                <button type="submit" class="btn btn-danger" @click.prevent="closeRegistration()">Cancel</button>
              </div>
            </div>
          </form>
        </div>
      </modal>
    </div>
  </section>
</template>

<script>
import OrganizationAPI from '@/plugins/organization';

export default {
  middleware: ['auth'],
  computed: {
    state () {
      return JSON.stringify(this.$auth.$state, undefined, 2)
    }
  },
  head() {
    return {
      title: "Organization List",
      meta: [
        {
          name: 'description',
          content: 'Organization List'
        },
      ],
    }
  },
  data() {
    return {
      organizations: {},
      organization: {
        name: "",
        region: "",
        industry: "",
        overview: "",
      },
    }
  },
  watch: {
    '$route.query': '$fetch'
  },

  async fetch() {
    this.organizations = await OrganizationAPI.getOrganizations()
  },

  methods: {
    /* Open modal window for adding Organization. */
    async openRegistration() {
      this.$modal.show("modal-organization-registration");
    },
    /* Hide modal window for adding Organization. */
    async closeRegistration() {
      this.$modal.hide("modal-organization-registration");
    },
    /* Submit form for adding Organization. */
    async addOrganization() {
      const formData = new FormData()
      for (const data in this.organizations) {
        formData.append(data, this.organizations[data])
      }
      await OrganizationAPI.addOrganization(formData)
      this.organizations = await OrganizationAPI.getOrganizations()
      await this.closeRegistration()
    },

    /* Hide specific Organization. */
    async hideOrganization(hide_organization) {
      hide_organization.invisible = true;
      await OrganizationAPI.updateOrganization(hide_organization.id, hide_organization)
      this.organizations = await OrganizationAPI.getOrganizations()
    },
  },
}
</script>
