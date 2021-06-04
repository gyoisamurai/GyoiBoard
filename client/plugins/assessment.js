import { axios } from './axios.js';

export default {
  /* Get specified assessment result. */
  getAssessment(assessment_id) {
    return axios.$get(`gyoithon/api/assessment/${assessment_id}/`)
  },

  /* Get all assessment result of Organization. */
  getAssessmentOrganization(organization_id) {
    return axios.$get(`gyoithon/api/organization/${organization_id}/assessment/`)
  },

  /* Get all assessment result of Domain. */
  getAssessmentDomain(domain_id) {
    return axios.$get(`gyoithon/api/domain/${domain_id}/assessment/`)
  },

  /* Get all assessment result of Subdomain. */
  getAssessmentSubdomain(subdomain_id) {
    return axios.$get(`gyoithon/api/subdomain/${subdomain_id}/assessment/`)
  },

  /* Update specified assessment result. */
  updateSubdomain(assessment_id, modify) {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.headers.common['Content-Type'] = 'application/json';
    return axios.$put(`gyoithon/assessment/edit/${assessment_id}/`, modify)
  }
}
