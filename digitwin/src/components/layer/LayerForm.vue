//UI 
<template>
  <div>
    <o-modal :active.sync="layer.isModalActive">
      <h1>Layer Form {{ layer.updateMode }}</h1>
      <p>( {{ this.layerDetail.parent_uuid }} )</p>

      <o-field label="Layer Name">
        <o-input v-model="this.layerDetail.layer_name"></o-input>
        <o-button
          id="submit-button"
          @click="
            layer.isModalActive = false;
            layer.updateMode = 'create';
            this.submitLayer(this.layerDetail);
            layer.selectedLayer = {};
            $emit('close');
          "
          >Submit</o-button
        >
      </o-field>
    </o-modal>
  </div>
</template>

// Logic Store
<script>
import { useLayerStore } from "@/stores/layer";

export default {
  setup() {
    // use store
    const layer = useLayerStore();

    return {
      // you can return the whole store instance to use it in the template
      layer,
    };
  },

  data() {
    return {
      layerDetail:
        this.layer.updateMode == "update"
          ? this.layer.selectedLayer
          : { layer_name: "", parent_uuid: this.layer.selectedLayer.uuid },
    };
  },

  methods: {
    submitLayer(payload) {
      this.layer.saveLayer(payload);
      this._initData();
    },

    // initialize state
    _initData() {
      this.layer.updateMode = "create";
      this.layer.selectedLayer = {};
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