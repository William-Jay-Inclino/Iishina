//UI 
<template>
  <div>
    <h1>Layer List</h1>
    <o-button id="add-layer" @click="layerModal({ mode: 'create' })"
      >Add Layer</o-button
    >
    <o-table
      id="layer-table"
      :data="layer.allLayers"
      :bordered="true"
      :striped="true"
      :narrowed="true"
      v-model:selected="layer.selectedLayer"
      focusable
    >
      <o-table-column
        field="layer_name"
        label="Layer"
        width="40"
        numeric
        v-slot="props"
      >
        {{ props.row.layer_name }}
      </o-table-column>

      <o-table-column
        field="uuid"
        label="Action"
        width="40"
        numeric
        v-slot="props"
      >
        <button
          class="edit-button"
          @click="layerModal({ mode: 'update', uuid: props.row.uuid })"
        >
          Edit
        </button>
        <button
          class="delete-button"
          @click="layer.deleteLayer({ uuid: props.row.uuid })"
        >
          Delete
        </button>
        {{ props.row.uuid }}
      </o-table-column>
      <o-table-column
        field="parent_uuid"
        label="Parent"
        width="40"
        numeric
        v-slot="props"
        >{{ props.row.parent_uuid }}</o-table-column
      >
    </o-table>
  </div>
</template>

// Logic Store
<script>
import { useLayerStore } from "@/stores/layer";
import LayerForm from "@/components/layer/LayerForm.vue";

export default {
  setup() {
    const start = performance.now();

    // use store
    const layer = useLayerStore();

    // trigger action, get layers from API and put in store (state)
    layer.getLayers();

    layer.getLayerTree();

    const duration = performance.now() - start;
    console.log("LayerList (ms):", duration);
    return {
      // you can return the whole store instance to use it in the template
      layer,
    };
  },

  data() {
    return {};
  },

  methods: {
    submitLayer(payload) {
      this.layer.saveLayer(payload);
      this.new_layer = "";
    },

    layerModal(payload) {
      console.log("layerModal...", payload);
      if (!!payload.uuid) {
        this.layer.selectedLayer = this.layer.layers.find(
          (item) => item.uuid === payload.uuid
        );
      }
      this.layer.updateMode = payload.mode;
      this.layer.isModalActive = true;
      this.$oruga.modal.open({
        component: LayerForm,
        trapFocus: true,
      });
    },
  },
};
</script>


// CSS
<style>
h1 {
  font-style: "bold";
}
</style>