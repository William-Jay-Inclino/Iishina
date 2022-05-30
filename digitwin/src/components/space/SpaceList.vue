<template>
  <div class = "space_list">
    <!--added style margin to move the button to the right-->
    <div class = "space_header">
      
      <o-button
        class = "space_header_button"
        id="add-owner-button"
        size="medium"
        variant="primary"
        @click="formLayer({ mode: 'create' })"
      >
        Add Layer
      </o-button>
      <o-button
        class = "space_header_button"
        id="add-owner-button"
        size="medium"
        variant="primary"
        @click="formSpace({ uuid: '' })"
      >
        Add Space
      </o-button>
    </div>
    <div class = "space_table">
    <!-- Implement nested buttons for layer tree -->
    {{layer.getCurrentLayer.name == undefined? layer.getCurrentLayer.layer_name:layer.getCurrentLayer.name}}
    <!-- Layer List View -->
    <o-table
      :data="layer.allLayersInCurrentLayer"
      :border="true"
      :striped="true"
      :narrowed="false"
      :v-model:selected="layer.selectedLayer"
    >
      <o-table-column
        field="last_name"
        label= "Name"
        just
        numeric
        v-slot="props"
        @click="formLayer({ mode: 'update', uuid: props.row.uuid })"
      >
        <o-icon pack="mdi" icon="folder" size="medium"> </o-icon> {{ props.row.layer_name }}
      </o-table-column>

      <o-table-column v-slot="props"  position="right" >
        <div>
          <o-button
            class = "list_button"
            id="edit-button"
            size="small"
            rounded
            v-on:click="formLayer({ mode: 'update', uuid: props.row.uuid })"
            ><o-icon pack="mdi" icon="pencil-outline" size="small"> </o-icon
          ></o-button>
          
          <o-button
            class = "list_button"
            id="edit-button"
            size="small"
            rounded
            v-on:click="
              layer.setCurrentLayer(props.row);
              space.setCurrentLayer(props.row);
            "
            ><o-icon pack="mdi" icon="arrow-right-thin" size="medium"> </o-icon
          ></o-button>
        </div>
      </o-table-column>
    </o-table>
    <!-- Space List View under branch-->
    <o-table
      :data="space.allSpacesInCurrentLayer"
      :v-model:selected="space.selectedSpace"
    >
      <o-table-column
        field="last_name"
        just
        numeric
        v-slot="props"
      >
        <o-icon pack="mdi" icon="floor-plan" size="medium"> </o-icon> {{ props.row.space_name }}
      </o-table-column>

      <o-table-column v-slot="props"  position="right" >
        <div>
          <o-button
            class = "list_button"
            id="edit-button"
            size="small"
            rounded
            v-on:click="formSpace({ mode: 'update', uuid: props.row.uuid })"
            ><o-icon pack="mdi" icon="pencil-outline" size="small"> </o-icon
          ></o-button>
        </div>
      </o-table-column>
    </o-table>
    </div>
  </div>
</template>

<script>
import { useSpaceStore } from "@/stores/space"; //to instantiate and use the store
import { useLayerStore } from "@/stores/layer";
import SpaceForm from "@/components/space/SpaceForm.vue";
import LayerForm from "@/components/space/LayerForm.vue";

export default {
  setup() {
    //need to fix as this is functions are only working on this alone
    const space = useSpaceStore();
    const layer = useLayerStore();

    //to get layers from API and put in store(state)
    layer.getLayerTree().then((results)=>{
      console.log("Filtering based on",layer.tree);
      layer.setCurrentLayer(layer.tree)
      space.setCurrentLayer(layer.tree)
    });
    space.getSpaces().then((results)=>{
      console.log("Spaces",space.allSpaces);
    })
    layer.getLayers().then((results)=>{
      console.log("Layers",layer.allLayers);
    })
     
    return {
      //to return whole store instance to use it in the template, like clean state again
      space,
      layer,
    };
  },

  data() {
   return {
      // visibleLayers: [],
      // visibleSpaces: []
    };
  },


  methods: {
    formSpace(data) {
      console.log("spaceModal...", data);
      if (!!data.uuid) {
        this.space.selectedSpace = this.space.spaces.find(
          (item) => item.uuid === data.uuid
        );
      }
      this.space.updateMode = data.mode;
      this.space.isModalActive = true;
      this.$oruga.modal.open({
        // parent is only for Vue2. in Vue 3 omit this option
        component: SpaceForm,
        trapFocus: true,
        props: { data },
      });
    },
    formLayer(data) {
      console.log("layerModal...", data);
      if (!!data.uuid) {
        this.layer.selectedLayer = this.layer.layers.find(
          (item) => item.uuid === data.uuid
        );
      }
      this.layer.updateMode = data.mode;
      this.layer.isModalActive = true;
      this.$oruga.modal.open({
        // parent is only for Vue2. in Vue 3 omit this option
        component: LayerForm,
        trapFocus: true,
        props: { data },
      });
    },
    goToHome() {
      this.$router.push("/"); //to redirect to another page
    },
    getLayerbyParent(data,parent_uuid) {
      return data.filter(
          function(data){ return data.parent_uuid == parent_uuid }
      );
    },
    getSpacebyParent(data,layer_uuid) {
      return data.filter(
          function(data){ return data.layer_uuid == layer_uuid }
      );
    },
  },
};
</script>
<style scoped>
.space_list{
  font-family: Verdana, sans-serif;;
  text-transform: uppercase;
}

.space_header{
  display: block;
  background-color: aqua;
}

.space_header_button{
  margin-right: 0.5em;
  float: right;
}

.space_table{
  margin:auto;
  padding-top:50px
}

.o-btn--primary,
.o-btn,
.o-chk__check {
  background-color: rgb(222, 30, 26) !important;
}

.list_button {
  min-width:40px;
  min-height:40px;
  margin-left:10px
}

.table_row {
  background-color: aqua;
  height:100%;
  width:100%;
  position:absolute;
}
</style>