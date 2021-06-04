import { axios } from './axios.js';

export default {
  /* Get specified subdomain. */
  getSubdomain(subdomain_id) {
    return axios.$get(`gyoithon/api/subdomain/${subdomain_id}/`)
  },

  /* Get all subdomains. */
  getSubdomains(organization_id, domain_id) {
    return axios.$get(`gyoithon/api/organization/${organization_id}/domain/${domain_id}/subdomain/`)
  },

  /* Add new subdomain. */
  addSubdomain(organization_id, domain_id, formData) {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.headers.common['Content-Type'] = 'multipart/form-data';
    return axios.$post(`gyoithon/api/organization/${organization_id}/domain/${domain_id}/subdomain/add/`, formData)
  },

  /* Update specified subdomain. */
  updateSubdomain(organization_id, domain_id, modify) {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.headers.common['Content-Type'] = 'application/json';
    return axios.$put(`gyoithon/api/organization/${organization_id}/domain/${domain_id}/subdomain/edit/${modify.id}/`, modify)
  }
}
