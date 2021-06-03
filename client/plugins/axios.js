export let axios;

export default ({ store, $axios }) => {
  $axios.defaults.baseURL = 'http://localhost:8000/'
  $axios.onRequest(config => {
    config.headers.Authorization = localStorage.getItem('auth._token.local');
    config.headers.Accept = 'application/json';
  });

  $axios.onResponse(response => {
    return Promise.resolve(response);
  })

  $axios.onError(error => {
    return Promise.reject(error.response);
  });

  axios = $axios;
}
