<template>
    <div>
        <h2 class="text-center">
            Login
        </h2>
        <hr>
        <b-alert v-if="$auth.$state.redirect" show>
            You have to login before accessing to
            <strong>{{ $auth.$state.redirect }}</strong>
        </b-alert>
        <b-row align-h="center" class="pt-4">
            <b-col md="4">
                <b-card bg-variant="light">
                    <busy-overlay/>
                    <form @keydown.enter="loginWithAuthModule">
                        <b-form-group label="Email">
                            <b-input ref="email" v-model="email"/>
                        </b-form-group>

                        <b-form-group label="Password">
                            <b-input v-model="password" type="password"/>
                        </b-form-group>

                        <div class="text-center">
                            <b-btn variant="primary" block @click="loginWithAuthModule">
                                Login
                            </b-btn>
                        </div>
                    </form>
                </b-card>
            </b-col>
        </b-row>
    </div>
</template>

<style scoped>
    .login-button {
        border: 0;
    }
</style>

<script>
export default {
  data () {
    return {
      email: '',
      password: '',
      error: null
    }
  },
  methods: {
    async loginWithAuthModule () {
      await this.$auth.loginWith('local', {
        data: {
          email: this.email,
          password: this.password
        }
      })
        .then(() => {
          this.$router.push('/top')
          },
          (error) => {
            return error
          })
    }
  }
}
</script>
