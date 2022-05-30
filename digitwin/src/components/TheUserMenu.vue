<template>
  <div class="user-menu">
    <o-button
      id="user-menu-button"
      @click="click"
      size="medium"
      variant="danger"
      slot="trigger"
      class="userMenu"
      ><o-icon pack="mdi" icon="account-outline" size="medium"> </o-icon
    ></o-button>
    <div v-if="isActive">
      <!--&& userRole = 'admin'-->
      <router-link to="/space" class="linkList" id="space-list-user-menu"
        >Space List</router-link
      >
      <router-link to="/owner" class="linkList" id="owner-list-user-menu"
        >Owner List</router-link
      >
      <router-link to="/" class="linkList" id="library-user-menu"
        >Library</router-link
      >
      <router-link to="/" class="linkList" id="account-user-menu"
        >Account</router-link
      >
      <router-link to="/" class="linkList" @click="logout" id="logout-user-menu"
        >Logout</router-link
      >
    </div>

    <!--<div v-else="isActive">
      //&& userRole = 'normalUser'
      <router-link to="/space" class="link-list">Space List</router-link>
      <router-link to="/" class="link-list">Library</router-link>
      <router-link to="/" class="link-list">Account</router-link>
      <router-link to="/" class="link-list" @click="logout">Logout</router-link>
    </div> -->
  </div>
</template>

<script>
import { useSessionStore } from "../stores/session";

export default {
  setup() {
    var start = performance.now();
    // use store
    const session = useSessionStore();
    //populate local session using action in useSessionStore
    return {
      // you can return the whole store instance to use it in the template
      session,
    };
  },

  data() {
    return {
      isActive: false, //variable if menu is active or not
    };
  },

  methods: {
    click() {
      this.isActive = !this.isActive; //is used to toggle for the dropdown
    },
    logout() {
      console.log("User is Logged Out");
    },
    //to logout user
    logOutUser() {
      if (localStorage.getItem("session") != undefined) {
        let mySession = Object(JSON.parse(localStorage.getItem("session")));
        let payload = {};
        payload.ticket = mySession.session.ticket;

        this.session.logoutUser(payload.ticket);
        this.$router.push("/");
      }
    },
  },
};
</script>

<style scooped>
.user-menu{
  display: block;
  position: relative;
  height:auto;
  padding-left: 20px;
  padding-top: 70px;
  overflow: auto;
  font-family: Verdana, Geneva, Tahoma, sans-serif;
}
.userMenu{
  position: absolute;
  left: 0;
  top: 0;
  width: 8%;
  z-index: 1;
  opacity: 100;
  cursor: pointer;
  height: 40px;
}
.userMenu:hover,
.userMenu:focus{
  background: #EA4C46;
  transition: background 0.45s;
}

.linkList:hover,
.linkList:focus {
  background: #F07470;
  transition: background 0.5s;
}

.linkList:checked {
  visibility: hidden;
  opacity: 0;
}

.linkList:not(:checked){
  opacity: 1;
  transition: opacity 0.3s ease-in-out;
}

.linkList{
  padding-left: 0;
  padding-top: 10px;
  padding-bottom: 5px;
  width: 8%;
  background: #990000;
  margin-bottom: 12px;
  text-align: center;
  color: white;
  float:left;
  clear:left;
  transition: all 0.4s ease-out;
  border-radius: 5px;
  text-decoration: none;
}
</style>