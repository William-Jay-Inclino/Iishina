<template>
  <div class="about">
    <h1>Space 3D View</h1>
    <li v-for="space in spaces" :key="space.id">
      <Space3d v-bind:space="space" />
    </li>
  </div>
</template>

<script>
import Space3d from "@/components/space/Space3d.vue";
export default {
  components: {
    Space3d,
  },
  data() {
    return {
      spaces: [
        {
          id: "qSGGhhjTYbN",
          src: "/bundle/showcase.html?m=qSGGhhjTYbN&applicationKey=a3ae8341bd8f44899eba16df86307d7d",
          width: "640",
          height: "400",
        },

        // https://my.matterport.com/show/?m=oFndTgraRhM
        {
          id: "oFndTgraRhM",
          width: "640",
          height: "400",
        },
        // https://my.matterport.com/show/?m=Msfg36od5J3
        {
          id: "Msfg36od5J3",
          width: "640",
          height: "400",
        },
        // https://my.matterport.com/show/?m=WPJ6pU7S7nE
        {
          id: "WPJ6pU7S7nE",
          width: "640",
          height: "400",
        },
        // https://my.matterport.com/show/?m=f58wynh3kDh
        {
          id: "f58wynh3kDh",
          src: "/bundle/showcase.html?m=f58wynh3kDh&applicationKey=a3ae8341bd8f44899eba16df86307d7d",
          width: "640",
          height: "400",
        },
      ],
    };
  },
};
</script>

<style>
</style>