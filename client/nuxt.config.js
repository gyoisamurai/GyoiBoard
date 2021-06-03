export default {
  mode: 'spa',
  head: {
    title: 'GyoiThon Dashboard',
    htmlAttrs: {
      lang: 'ja'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  css: [
    '~/assets/css/bootstrap.min.css',
    '~/assets/css/main.css',
  ],
  script: [
    '~/assets/js/popper.js',
    '~/assets/js/bootstrap.js',
    '~/assets/js/jquery-3.6.0.js'
  ],
  plugins: [
    { src: '~/plugins/axios.js' },
    { src: '~/plugins/organization.js' },
    { src: '~/plugins/domain.js' },
    { src: '~/plugins/subdomain.js' },
    { src: '~/plugins/modal-window.js' },
    { src: '~/plugins/filter.js' }
  ],
  components: true,
  buildModules: [
  ],
  modules: [
    'bootstrap-vue/nuxt',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/proxy',
    ['@nuxtjs/moment', ['ja']],
  ],
  axios: {
    // baseURL: "http://localhost:8000/"
    proxy: true
  },
  proxy: {
    '/gyoithon/': {
      target: 'http://localhost:8000/gyoithon/',
      pathRewrite: { '^/gyoithon/': '/' }
    },
  },
  router: {
    middleware: ['auth']
  },
  auth: {
    cookie: false,
    redirect: {
      login: '/login',
      logout: '/login',
      callback: '/callback',
      home: '/top'
    },
    strategies: {
      local: {
        token: {
          property: 'token',
          type: 'JWT',
          required: true
        },
        endpoints: {
          login: { url: '/rest-auth/login/', method: 'post', propertyName: 'token' },
          user: false,
          logout: false
        }
      },
    },
  },
  build: {
    extend (config, ctx){
    }
  },
  loading: {
    color: 'blue',
    height: '5px'
  }
}
