created() {
    const provider = this.$auth.$state.strategy
    const callbackParams = queryString.parse(this.$auth.ctx.from.hash)

    this.$index.post(`http://127.0.0.1:8000/rest-auth/${provider}/`, {
            access_token: callbackParams.access_token,
            code: callbackParams.code
        })
        .then((response) => {
            const data = response.data
            this.$auth.setToken(provider, data.token)
            this.$auth.setUser(data.user)
            this.$auth.setUserToken(`JWT ${data.token}`)
            this.$router.push('/top')
        })
        .catch(() => {
            this.$auth.logout()
            this.$router.push('/registration')
        })
}
