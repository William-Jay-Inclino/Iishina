//UI 
<template>
  <div class = "layer_form">
    <section>
      <form action="">
        <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title" >{{ layer.updateMode }} layer</p>
        <o-icon
          clickable
          native-type="button"
          icon="times"
          @click.native="$emit('close')"
        />
      </header>
      <o-field class = "modal-card-body" label="Layer Name">
        <o-input v-model="this.layerDetail.layer_name"></o-input>
      </o-field>
      <footer class="modal-card-foot">
        <o-button
          id="submit-space-button"
          class = "space_form_button"
          rounded
          pack="fas"
          icon="home"
          variant="primary"
          @click="
            layer.isModalActive = false;
            layer.updateMode = 'create';
            this.submitLayer(this.layerDetail),
            layer.selectedLayer = {};
            $emit('close')"
          >{{layer.updateMode == "update"?"Update":"Add"}}</o-button
        >
        <o-button
          id="close-owner-button"
          class = "space_form_button"
          rounded
          type="button"
          @click="$emit('close')"
          >Close</o-button
        >
      </footer>
      
        </div>
      </form>
    </section>
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
          : 
          { 
            layer_name: "" ,
            parent_uuid: this.layer.getCurrentLayer.uuid,
          },
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
<style scoped>
.layer_form {
  width:50vw;
  min-width: 560px;
  max-width: 800px;
  font-family: Verdana, sans-serif;;
  text-transform: uppercase;
}

h1 {
  font-style: "bold";
}

.modal-card {
  margin: 20px 20px;
  max-height: calc(100vh - 160px);
  overflow: auto;
  position: relative;
}

.modal-card-foot,
.modal-card-head {
  align-items: center;
  background-color: #f5f5f5;
  display: flex;
  flex-shrink: 0;
  justify-content: flex-end;
  padding: 20px;
  position: relative;
}
.modal-card-head {
  border-bottom: 1px solid #dbdbdb;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
}
.modal-card-body {
  -webkit-overflow-scrolling: touch;
  background-color: #fff;
  flex-grow: 1;
  flex-shrink: 1;
  overflow: auto;
  padding: 20px;
}
.modal-card-foot {
  border-bottom-left-radius: 6px;
  border-bottom-right-radius: 6px;
  border-top: 1px solid #dbdbdb;
}
.modal-card-title {
  color: #363636;
  flex-grow: 1;
  flex-shrink: 0;
  font-size: 1.5rem;
  line-height: 1;
  margin: 0;
  font-weight: 800;
}
.modal-card-foot .o-button:not(:last-child) {
  margin-right: 0.5em;
}

.o-btn--primary,
.o-btn,
.o-chk__check {
  background-color: rgb(222, 30, 26) !important;
}

.space_form_button {
margin:0px 10px
}
</style>