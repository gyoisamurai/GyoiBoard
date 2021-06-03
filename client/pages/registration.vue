<template>
    <div>
        <h2 class="text-center">
            Registration
        </h2>
        <hr>
        <b-alert v-if="errorMessage" show variant="danger">
            {{ errorMessage }}
        </b-alert>
        <b-row align-h="center" class="pt-4">
            <b-col md="4">
                <b-card bg-variant="light">
                    <busy-overlay/>
                    <form @keydown.enter="registration">
                        <b-form-group label="Email">
                            <b-input ref="email" v-model="email"/>
                        </b-form-group>

                        <b-form-group label="Password">
                            <b-input v-model="password" type="password"/>
                        </b-form-group>

                        <b-form-group label="PasswordConfirm">
                            <b-input v-model="passwordConfirm" type="password"/>
                        </b-form-group>

                        <div class="text-center">
                            <b-btn variant="primary" block @click="registration">
                                Registration
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
import busyOverlay from '~/components/busy-overlay'

export default {
  middleware: ['auth'],
  options: {
    auth: false
  },
  components: { busyOverlay },
  data () {
    return {
      email: '',
      password: '',
      passwordConfirm: '',
      error: null
    }
  },
  computed: {
    errorMessage () {
      const { error } = this

      if (!error || typeof error === 'string') {
        return error
      }
      let msg = ''
      if (error.message) {
        msg += error.message
      }
      if (error.errors) {
        msg += `(${JSON.stringify(error.errors)
          .replace(/[{}"[\]]/g, '')
          .replace(/:/g, ': ')
          .replace(/,/g, ' ')})`
      }
      return msg
    }
  },
  methods: {
    async registration () {
      this.error = null

      this.$axios.post(`/server/rest-auth/registration/`, {
        email: this.email,
        password1: this.password,
        password2: this.passwordConfirm
      })
        .then(() => {
          this.$router.push('/top')
        })
        .catch((e) => {
          this.error = e.response.data
        })
    }
  }
}
</script>
