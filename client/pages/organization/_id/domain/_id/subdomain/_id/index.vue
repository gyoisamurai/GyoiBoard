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
                      <button type="submit" class="btn btn-info">Re-Search</button>
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
                <th>URL</th>
                <th>Product Name</th>
                <th>Vendor</th>
                <th>Type</th>
                <th>CVE-ID</th>
                <th>Scan Date</th>
                <th colspan="2"></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="assessment of assessments" @click="$data.assessment = assessment" v-if="!subdomain.invisible">
                <td scope="row">{{ assessment.id }}</td>
                <td>{{ assessment.assessment_url }}</td>
                <td>{{ assessment.product_name }} / {{ assessment.product_version }}</td>
                <td>{{ assessment.product_vendor }}</td>
                <td>{{ assessment.product_type }}</td>
                <td v-html="assessment.product_cveid.replace(/\n/g,'<br/>')">{{ assessment.product_cveid }}</td>
                <td>{{ assessment.scan_date | formatDate }}</td>
                <td>
                  <NuxtLink class="btn btn-primary btn-sm" :to="`/subdomain/${subdomain.id}/`">View</NuxtLink>
                  <button @click="hideSubdomain(subdomain)" class="btn btn-danger btn-sm">Hide</button>
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
import AssessmentAPI from '~/plugins/assessment';

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
      assessments: {},
      assessment: {
        assessment_url: "",
        product_vendor: "",
        product_name: "",
        product_version: "",
        product_type: "",
        product_cveid: "",
        scan_date: "",
        related_organization_id: "",
        related_domain_id: "",
        related_subdomain_id: "",
      }
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
      const assessments = await AssessmentAPI.getAssessmentSubdomain(params.id)
      return { organization, domain, subdomain, assessments }
    } catch (e) {
      return { organization: [], domain: [], subdomain: [], assessments: [] }
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
