<!--
A nested tree component that recursively renders itself.
You can double click on an item to turn it into a folder.
-->

<script>
import { useLayerStore } from "@/stores/layer";
import TreeItem from "@/components/layer/TreeItem.vue";

let treeData = {
  name: "My Tree",
  children: [
    { name: "hello" },
    { name: "wat" },
    {
      name: "child folder",
      children: [
        {
          name: "child folder",
          children: [{ name: "hello" }, { name: "wat" }],
        },
        { name: "hello" },
        { name: "wat" },
        {
          name: "child folder",
          children: [{ name: "hello" }, { name: "wat" }],
        },
      ],
    },
  ],
};

export default {
  setup() {
    const start = performance.now();

    // use store
    const layer = useLayerStore();

    // trigger action, get layers from API and put in store (state)
    layer.getLayers();

    layer.getLayerTree();

    let myData = layer.treeData;
    console.log("trees", JSON.stringify(myData), typeof myData);

    const duration = performance.now() - start;
    console.log("LayerList (ms):", duration);
    return {
      // you can return the whole store instance to use it in the template
      layer,
    };
  },

  components: {
    TreeItem,
  },
  data() {
    return {
      treeData,
    };
  },
};
</script>

<template>
  <ul>
    <TreeItem
      style="color: white"
      class="item"
      :model="layer.layerTree"
    ></TreeItem>
  </ul>
</template>

<style>
.item {
  cursor: pointer;
  line-height: 1.5;
}
.bold {
  font-weight: bold;
}
</style>