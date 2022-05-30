<template>
  <div class="ownerForm">
    <section>
      <form action="">
        <div class="modal-card">
          <header class="modal-card-head">
            <p class="modal-card-title">Space Details</p>
            <o-icon
              clickable
              native-type="button"
              icon="times"
              @click.native="$emit('close')"
            />
          </header>

          <section class="modal-card-body">
            <o-field class = "space_input"  label="Space ID">
              <o-input
                id="first-name-input"
                v-model="this.spaceDetail.space_sid"
                placeholder="Space SID"
                type="text"
                expanded
              ></o-input>
            </o-field>

            <o-field class = "space_input" label="Space Name">
              <o-input
                id="last-name-input"
                v-model="this.spaceDetail.space_name"
                placeholder="Space Name"
                type="text"
                expanded
              ></o-input>
            </o-field>

            <o-field class = "space_input"  label="Space URL">
              <o-input
                id="space_url-address-input"
                v-model="this.spaceDetail.space_url"
                placeholder="Space URL"
              ></o-input>
            </o-field>

          </section>
          <footer class="modal-card-foot">
            <o-button
              id="submit-space-button"
              class = "space_form_button"
              rounded
              pack="fas"
              icon="home"
              variant="primary"
              @click="
                space.isModalActive = false;
                space.updateMode = 'create';
                this.submitSpace(this.spaceDetail),
                space.selectedSpace = {}; 
                $emit('close')
              "
              >{{space.updateMode == "update"?"Update":"Add"}}</o-button
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

<script>
import { useSpaceStore } from "@/stores/space"; //to instantiate and use the store
import { useSessionStore } from "@/stores/session"; //to instantiate and use the store

export default {
  name: "SpaceForm",

  setup() {
    //need to fix as this is functions are only working on this alone
    //use user
    const space = useSpaceStore();

    //to get layers from API and put in store(state)
    space.getSpaces();
    // console.log(session.uuid)

    return {
      //to return whole store instance to use it in the template, like clean state again
      space,
    };
  },

  data() {
    
    return {
      spaceDetail:
        this.space.updateMode == "update"
          ? this.space.selectedSpace
          : 
          {
            //object to correspond
            space_sid: "",
            space_name: "",
            space_url: "",
            layer_uuid: this.space.currentLayer.uuid,//Based on value of currentLayer
          },
    };
  },

  methods: {
    submitSpace(payload) {
      
      console.log("Submitting",payload);
      //is an button event-listener made inside <template>
      this.space.saveSpace(payload);
      this._initData();
    },
    // initialize state
    _initData() {
      this.space.updateMode = "create";
      this.space.selectedLayer = {};
    },
  },
};
</script>

<style scoped>
.ownerForm {
  width:50vw;
  min-width: 560px;
  max-width: 800px;
  font-family: Verdana, sans-serif;;
  text-transform: uppercase;
}
.modal-card {
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 40px);
  overflow: hidden;
}
@media screen and (min-width: 769px) {
  .modal-card {
    margin: 0 auto;
    max-height: calc(100vh - 40px);
  }
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

.space_input{
  
  font-weight: 100;
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