<template>
  <div class="ownerForm">
    <section>
      <form action="">
        <div class="modal-card" style="width: 400px">
          <header class="modal-card-head">
            <p class="modal-card-title">Owner Information</p>
            <o-icon
              clickable
              native-type="button"
              icon="times"
              @click.native="$emit('close')"
            />
          </header>

          <o-upload v-model="file">
            <o-button tag="a" variant="primary">
              <o-icon icon="upload"></o-icon>
              <span>Click to upload</span>
            </o-button>
          </o-upload>
          <section class="modal-card-body">
            <o-field label="First Name">
              <o-input
                id="first-name-input"
                v-model.trim="this.userDetail.first_name"
                placeholder="First Name"
                type="text"
                expanded
                required
              ></o-input>
            </o-field>

            <o-field label="Last Name">
              <o-input
                id="last-name-input"
                v-model.trim="this.userDetail.last_name"
                placeholder="Last Name"
                type="text"
                expanded
                required
              ></o-input>
            </o-field>

            <o-field label="Company">
              <o-input
                id="company-name-input"
                v-model.trim="this.userDetail.company_name"
                placeholder="Company Name"
                type="text"
                expanded
                required
              ></o-input>
            </o-field>

            <o-field label="Spaces">
              <o-select
                id="space-amount-select"
                v-model="this.userDetail.space_amount"
                rounded
                required
              >
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
              </o-select>
            </o-field>

            <o-field label="Email">
              <o-input
                id="email-address-input"
                v-model.trim="this.userDetail.email"
                v-on:change="inputFontCaseChange"
                placeholder="Email Address"
                type="email"
                required
              ></o-input>
            </o-field>

            <o-field label="Password" v-if="this.user.updateMode != 'update'">
              <o-input
                id="password-input"
                v-model.trim="this.userDetail.password"
                type="password"
                placeholder="Password"
                required
                expanded
              >
              </o-input>
            </o-field>
          </section>
          <footer class="modal-card-foot">
            <o-field horizontal>
              <o-button
                id="submit-owner-button"
                rounded
                pack="fas"
                icon="home"
                variant="primary"
                @click="
                  this.submitUser(this.userDetail);
                  user.selectedUser = {};
                  $emit('close');
                "
                >Save</o-button
              >
              <o-button
                id="close-owner"
                rounded
                type="button"
                @click="
                  user.selectedUser = {};
                  $emit('close');
                "
                >Close</o-button
              >

              <o-button
                id="delete-owner"
                rounded
                type="button"
                @click="
                  user.deleteUser({ uuid: this.userDetail.uuid });
                  $emit('close');
                "
                >delete</o-button
              >
            </o-field>
          </footer>
        </div>
      </form>
    </section>
  </div>
</template>

<script>
import { useUserStore } from "@/stores/user"; //to instantiate and use the store

export default {
  name: "OwnerForm",
  props: ["type"],
  setup() {
    //need to fix as this is functions are only working on this alone
    //use user
    const user = useUserStore();

    //to get layers from API and put in store(state)
    user.getUsers();

    return {
      //to return whole store instance to use it in the template, like clean state again
      user,
    };
  },

  data() {
    return {
      userDetail:
        this.user.updateMode == "update"
          ? this.user.selectedUser
          : {
              first_name: "",
              last_name: "",
              company_name: "",
              space_amount: "",
              email: "",
              password: "",
            },
    };
  },

  methods: {
    inputFontCaseChange() {
      this.userDetail.email = this.userDetail.email.toLowerCase();
    },

    submitUser(payload) {
      //is an button event-listener made inside <template>
      console.log("submitUser..", payload);
      this.user.saveUser(payload);
    },
  },
};
</script>

<style scoped>
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
    width: 640px;
  }
}
.modal-card {
  margin: 0 20px;
  max-height: calc(100vh - 160px);
  overflow: auto;
  position: relative;
  width: 100%;
}
.modal-card-foot,
.modal-card-head {
  align-items: center;
  background-color: #f5f5f5;
  display: flex;
  flex-shrink: 0;
  justify-content: flex-start;
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
}
.modal-card-foot .o-button:not(:last-child) {
  margin-right: 0.5em;
}

.o-btn--primary,
.o-btn,
.o-chk__check {
  background-color: rgb(222, 30, 26) !important;
}
</style>