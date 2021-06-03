<template>
    <div>
        <b-jumbotron class="text-center">
            <h3>Welcome to GyoiThon Dashboard</h3>
            This is a demo page.
            <div class="mt-1">
                <template v-if="$auth.$state.loggedIn">
                    <b-btn class="ml-3" variant="info" to="/top">
                        Top
                    </b-btn>
                    <b-btn class="ml-3" variant="danger" @click="$auth.logout()">
                        Logout
                    </b-btn>
                </template>
                <b-btn v-else variant="success" to="/login">
                    Login
                </b-btn>
            </div>
        </b-jumbotron>

        <div>
            User status:
            <b-badge>{{ $auth.$state.loggedIn ? 'Logged In' : 'Guest' }}</b-badge>
        </div>
    </div>
</template>

<script>
export default {
  layout ({ $auth }) {
    return $auth.loggedIn ? 'top' : 'login'
  },
}


</script>
