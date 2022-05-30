<script setup>
import { RouterLink, RouterView } from "vue-router";
import HelloWorld from "@/components/HelloWorld.vue";
import TheNavBar from "@/components/TheNavBar.vue";
import StoreTest from "@/components/StoreTest.vue";

import { useSessionStore } from "@/stores/session";

console.log(
  "localStorage...",
  Object(JSON.parse(localStorage.getItem("session")))
);

// use store
const session = useSessionStore();

// get previous stored session from local
if (localStorage.getItem("session") != undefined) {
  let mySession = Object(JSON.parse(localStorage.getItem("session")));
  let payload = {};
  payload.ticket = mySession.session.ticket;
  session.validateSession(payload);
}

// detect state changes
session.$subscribe((mutation, state) => {
  // import { MutationType } from 'pinia'
  mutation.type; // 'direct' | 'patch object' | 'patch function'

  // same as session.$id
  mutation.storeId;

  // only available with mutation.type === 'patch object'
  mutation.payload; // patch object passed to cartStore.$patch()

  // persist the whole state to the local storage whenever it changes
  localStorage.setItem("session", JSON.stringify(state));
});
</script>

<template>
  <div>
    <!-- Navigation Bar -->
    <TheNavBar />

    <!-- View the user is currently in -->
    <div class="content">
      <RouterView />
    </div>
  </div>
</template>

<style>
header {
  /* background-color: aqua; */
  height: 87px;
}
.content {
  margin-top: 87px;
  /* background-color:blue; */
}
body {
  background: linear-gradient(rgb(60, 60, 60), rgb(20, 20, 20), rgb(0, 0, 0))
    no-repeat fixed center;
    margin: 0px;
}
/* @import "@/assets/base.css";

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;

  font-weight: normal;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

a,
.green {
  text-decoration: none;
  color: hsla(160, 100%, 37%, 1);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: hsla(160, 100%, 37%, 0.2);
  }
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  body {
    display: flex;
    place-items: center;
  }

  #app {
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 2rem;
  }

  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
} */
</style>
