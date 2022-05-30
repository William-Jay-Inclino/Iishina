<template>
  <div class="content-body">
    <div class="title">Space List</div>
    
    <SpaceList />
  </div>
</template>

<script>
import SpaceList from "@/components/space/SpaceList.vue";
export default {
  name: 'App',
  components: {
    SpaceList
  }
}
</script>

<style scoped>
.content-body{
  width:100vw;
  min-height: calc(100vh - 87px);
  background-color: white;
  padding:50px 150px;
}

.title{
    font-size: 32px;
    font-family: Verdana, sans-serif;;
    font-weight: bold;
    text-transform: uppercase;
}
</style>