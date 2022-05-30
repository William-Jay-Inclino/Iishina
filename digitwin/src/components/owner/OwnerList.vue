<template>
  <div>
    <p>Owner List</p>
    <!--added style margin to move the button to the right-->
    <o-button
      id="add-owner-button"
      size="medium"
      variant="primary"
      @click="
        user.selectedUser = {};
        ownerModal({ mode: 'create', uuid: '' });
      "
      style="margin-left: auto; display: block"
    >
      Add Owner
    </o-button>
    <o-table
      :data="user.allUsers"
      :bordered="true"
      :striped="true"
      :narrowed="true"
      v-model:selected="user.selectedUser"
      focusable
    >
      <o-table-column
        field="first_name"
        label="First Name"
        width="40"
        numeric
        v-slot="props"
      >
        {{ props.row.first_name }}
      </o-table-column>

      <o-table-column
        field="last_name"
        label="Last Name"
        numeric
        v-slot="props"
      >
        {{ props.row.last_name }}
      </o-table-column>

      <o-table-column field="uuid" v-slot="props">
        <div>
          <o-button
            id="user-space-button"
            size="small"
            rounded
            v-on:click="goToHome()"
          >
            <o-icon pack="mdi" icon="cube-outline" size="small"> </o-icon>
          </o-button>

          <!--icon is still not working, might need to import the materials-->
          <o-button
            id="library-button"
            size="small"
            rounded
            v-on:click="goToHome()"
            ><o-icon pack="mdi" icon="bookshelf" size="small"> </o-icon
          ></o-button>

          <o-button
            id="edit-button"
            size="small"
            rounded
            v-on:click="ownerModal({ mode: 'update', uuid: props.row.uuid })"
            ><o-icon pack="mdi" icon="pencil-outline" size="small"> </o-icon
          ></o-button>
        </div>
      </o-table-column>
    </o-table>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user"; //to instantiate and use the store

import OwnerForm from "@/components/owner/OwnerForm.vue";

export default {
  setup() {
    //need to fix as this is functions are only working on this alone
    const user = useUserStore();

    //to get layers from API and put in store(state)
    user.getUsers();

    return {
      //to return whole store instance to use it in the template, like clean state again
      user,
    };
  },

  data() {},
  methods: {
    ownerModal(payload) {
      console.log("userModal...", payload);
      if (!!payload.uuid) {
        this.user.selectedUser = this.user.users.find(
          (item) => item.uuid === payload.uuid
        );
      }
      this.user.updateMode = payload.mode;
      this.user.isModalActive = true;
      this.$oruga.modal.open({
        component: OwnerForm,
        trapFocus: true,
      });
    },
    goToHome() {
      this.$router.push("/"); //to redirect to another page
    },
  },
};
</script>
<style scoped>
.searchButton {
  margin-bottom: 6px;
}
.OwnerList__styled {
  background: white;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}
.headerText {
  font-size: 25px;
  position: relative;
  left: 80px;
}
.o-btn--primary,
.o-btn,
.o-chk__check {
  color: white;
  background-color: rgb(222, 30, 26) !important;
}
</style>