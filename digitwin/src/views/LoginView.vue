<template>
  <section class = "loginField">
    
    <!-- <img src="../assets/iishina.png"> -->

    <o-field class = "field-name" label="Email">
    <o-input id = "log-in-email" v-model="email" maxlength="30"></o-input>
    </o-field>

    <o-field class = "field-name" label="Password">
    <o-input id = "log-in-password" type="password" v-model="password" password-reveal> </o-input>
    </o-field>
    <!-- Oruga implementation of icon -->
    <!-- <o-icon pack="mdi" icon="account-lock-open" size="large" variant = "primary"> </o-icon> -->
    
    <o-button id = "log-in-btn" class = "log-btn" rounded  @click="login()" >Log In</o-button>
  </section>
</template>

<script>
import { useSessionStore } from "@/stores/session";
import { ref } from 'vue'

export default {
  setup() {
    var start = performance.now();
    // use store
    const session = useSessionStore();
    // trigger action, get layers from API and put in store (state)
    // session.getSession();
    var duration = performance.now() - start;

    console.log("Login Page(ms): ", duration);
    return {
      // you can return the whole store instance to use it in the template
      session,
    };
  },

  data() {
    return {
      email: "",
      password: "",
    };
  },

  methods: {
    login() {
      console.log("Username and password is: ", this.email, this.password);
      this.session.loginUser({
        "email": this.email,
        "password": this.password,
      }).then((result) => {
        console.log("User Logged in. Redirecting...")
        if (localStorage.getItem("session") != undefined) { //Get session from local storage and see if login is successful
          let mySession = Object(JSON.parse(localStorage.getItem("session")));
          let payload = {};
          payload.ticket = mySession.session.ticket;
          if (payload.ticket != undefined){
            this.$router.push('/space');
          }else{
            console.log(" Redirecting Failed. Ticket undefined")
          }
        }else{
          console.log(" Redirecting Failed. Session undefined")
        }
      })
      
    }
  }
}
</script>

<style>
.loginField{
  width: 400px;
  /* background-color: aqua; */
  padding: 50px;
  margin:auto;
  margin-top:20vh;
  background-color: rgb(0,0,0,0.1);
  border-radius: 30px;
}

.field-name{
  padding-bottom: 10px;
}

.field-name .o-field__label{
  color:white;
  font-family: Verdana, sans-serif;
  font-weight: bold;
  text-transform: uppercase;
  padding-bottom: 10px;
}

.loginField .log-btn{
    background-color: rgb(222,30,26);
    border: 0px;
    color: white;
    font-family: Verdana, sans-serif;;
    text-transform: uppercase;
    font-weight: 50px;
    font-size: 12px;
    width: 300px;
    height: 35px;
    margin-top:30px;
}
</style>