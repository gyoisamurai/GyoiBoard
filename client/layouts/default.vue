<template>
  <div>
    <Header />
    <Navigator />
  </div>
</template>

<script>
  import Header from "~/components/Header.vue";
  import Navigator from "~/components/Navigator.vue";
  export default {
    components: {
      Header,
      Navigator,
    }
  };
</script>
