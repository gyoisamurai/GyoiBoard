import { axios } from './axios.js';

export default {
  /* Get specified organization. */
  getOrganization(id) {
    return axios.$get(`gyoithon/api/organization/${id}/`)
  },

  /* Get all organizations. */
  getOrganizations() {
    return axios.$get(`gyoithon/api/organization/`)
  },

  /* Add new organization. */
  addOrganization(formData) {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.headers.common['Content-Type'] = 'multipart/form-data';
    return axios.$post(`gyoithon/api/organization/add/`, formData)
  },

  /* Update specified organization. */
  updateOrganization(id, modify) {
    axios.defaults.xsrfCookieName = "csrftoken";
    axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    axios.defaults.headers.common['Content-Type'] = 'application/json';
    return axios.$put(`gyoithon/api/organization/edit/${id}/`, modify)
  }
}
