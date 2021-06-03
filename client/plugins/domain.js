import { axios } from './axios.js';

export default {
  /* Get specified domain. */
  getDomain(domain_id) {
    return axios.$get(`gyoithon/api/domain/${domain_id}/`)
  },

  /* Get all domains. */
  getDomains(organization_id) {
    return axios.$get(`gyoithon/api/organization/${organization_id}/domain/`)
  },

  /* Add new domain. */
  addDomain(organization_id, formData) {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.headers.common['Content-Type'] = 'multipart/form-data';
    return axios.$post(`gyoithon/api/organization/${organization_id}/domain/add/`, formData)
  },

  /* Update specified domain. */
  updateDomain(organization_id, domain_id, modify) {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.headers.common['Content-Type'] = 'application/json';
    return axios.$put(`gyoithon/api/organization/${organization_id}/domain/edit/${domain_id}/`, modify)
  }
}
