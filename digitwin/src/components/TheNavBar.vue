<template>
  <header class="nav-bar">
    <!-- Iishina Logo -->
    <div id="nav-logo" class="product-name" @click="$router.push('/')">
      <img src="../assets/iishina.png" />
    </div>
    <!-- Product Name -->
    <div id="nav-home" class="product-name name" @click="$router.push('/')">
      TWIN
    </div>

    <section class="nav-buttons">
      <div v-if="session.isLoggedIn" class="buttons">
        <o-button
          id="nav-profile"
          class="transparent-btn"
          variant="primary"
          inverted
          >Profile</o-button
        >
        <o-button
          id="nav-space-events"
          class="transparent-btn"
          variant="primary"
          inverted
          >Space Events</o-button
        >
        <!-- <o-button
          id="nav-space-list"
          class="transparent-btn"
          @click="$router.push('owner/space')"
          variant="primary"
          inverted
          >Space List</o-button
        > -->
        <!-- <o-button
          id="nav-owner-list"
          class="transparent-btn"
          @click="$router.push('owner')"
          variant="primary"
          inverted
          >Owner List</o-button
        > -->
        <o-button
          id="nav-about-us"
          class="transparent-btn"
          variant="primary"
          inverted
          >About Us</o-button
        >
        <!-- <o-button
          id="nav-log-out"
          class="log-btn"
          @click="logOutUser()"
          variant="info"
          rounded
          >Log Out</o-button
        > -->

        <o-select
          v-if="session.isLoggedIn"
          id="user-menu-select"
          @change="onChange()"
          rounded
          v-model="selectedProfile"
        >
          <option value="0">
            {{
              session.auth_user.first_name + " " + session.auth_user.last_name
            }}
          </option>
          <option value="1">Space List</option>
          <option value="2">Owner List</option>
          <option value="3">Library</option>
          <option value="4">Account</option>
          <option value="5" @click="logOutUser()">Logout</option>
        </o-select>
      </div>
      <div v-else class="buttons">
        <o-button
          id="nav-space-events"
          class="transparent-btn"
          @click="$router.push('/')"
          variant="primary"
          inverted
          >Space Events</o-button
        >
        <o-button
          id="nav-about-us"
          class="transparent-btn"
          variant="primary"
          inverted
          >About Us</o-button
        >
        <o-button
          id="nav-log-in"
          class="log-btn"
          @click="$router.push('/')"
          variant="info"
          rounded
          >Log In</o-button
        >
      </div>

      <div></div>
    </section>
  </header>
</template>

<script>
import { useSessionStore } from "@/stores/session";
export default {
  setup() {
    var start = performance.now();
    // use store
    const session = useSessionStore();
    //populate locar session using action in useSessionStore
    // session.getSession();
    // use isLoggedIn getter function and save it as a var

    // trigger action, get layers from API and put in store (state)

    var duration = performance.now() - start;

    console.log("TheNavBar(ms): ", duration);
    return {
      // you can return the whole store instance to use it in the template
      session,
    };
  },

  data() {
    return {
      // layer: [],
      selectedProfile: 0,
    };
  },

  methods: {
    onChange() {
      console.log("onChange trigger " + this.selectedProfile);
      if (this.selectedProfile == 1) {
        this.$router.push("/space");
      } else if (this.selectedProfile == 2) {
        this.$router.push("/owner");
      } else if (this.selectedProfile == 3) {
        this.$router.push("/library");
      } else if (this.selectedProfile == 4) {
        this.$router.push("/account");
      } else if (this.selectedProfile == 5) {
        this.logOutUser();
      }
    },
    logOutUser() {
      if (localStorage.getItem("session") != undefined) {
        let mySession = Object(JSON.parse(localStorage.getItem("session")));
        let payload = {};
        payload.ticket = mySession.session.ticket;

        this.session.logoutUser(payload.ticket);
        this.$router.push("/");
        this.selectedProfile = 0;
      }
    },
  },
};
</script>
<style>
#profile-select {
  background-color: rgb(222, 30, 26);
  color: white;
  opacity: 1;
  border: none;
}
.nav-bar {
  display: inline;
  justify-content: center;
  position: absolute !important;
  top: 0px !important;
  left: 0px !important;
  width: 100vw;
  height: 87px;
  overflow: hidden;
  backdrop-filter: blur(3px);
}

.product-name {
  display: inline;
  float: left;
  color: white;
  font-size: 40px;
  font-family: Verdana, sans-serif;
  font-weight: bold;
}

.name {
  padding-top: 15px;
  padding-left: 10px;
}

.nav-buttons {
  float: right;
  color: #f2f2f2;
  text-align: center;
  text-decoration: none;
  font-size: 17px;
  margin: auto;
  padding: 30px 0;
  padding-right: 15px;
}

.nav-buttons .transparent-btn {
  background-color: rgb(0, 0, 0, 0);
  border: 0px;
  color: white;
  font-family: Verdana, sans-serif;
  text-transform: uppercase;
  font-size: 12px;
  width: 10vw;
  max-width: 150px;
  min-width: 120px;
  font-weight: bold;
}

.nav-buttons .log-btn {
  background-color: rgb(222, 30, 26);
  color: white;
  font-family: Verdana, sans-serif;
  text-transform: uppercase;
  font-size: 12px;
  width: 150px;
  font-weight: 50px;
}
</style>