import { defineStore } from "pinia";
import axios from "axios";

const apiURL = import.meta.env.VITE_API_URL + "/cas";
console.log("apiURL...", apiURL);

const api = axios.create({
  baseURL: apiURL,
});

export const useSessionStore = defineStore("session", {
  // arrow function recommended for full type inference
  state: () => {
    return {
      // all these properties will have their type inferred automatically
      session: {},
    };
  },

  // filters or format state
  getters: {
    auth_user: (state) => state.session.auth.user,
    uuid: (state) => state.session.auth.user.uuid,

    isLoggedIn: (state) =>
      typeof state.session.auth !== "undefined" ? true : false,

    userRole: (state) => state.session.auth.user_groups[1],
  },

  // events that can be triggered, get data from external API and store in the Stage
  actions: {
    async validateSession(payload) {
      console.log("validateSession...", payload);
      var response = (await api.get("/validate.json/" + payload.ticket)).data;
      // console.log(response);

      if (response.status == "success") {
        const sessionData = await response.data;
        this.session = sessionData;
      } else {
        this.session = {};
        console.log("status: ", response.status);
        console.log(response.message);
      }
    },

    async loginUser(payload) {
      console.log("loginUser...", payload);
      var loginResponse = (await api.post("/tickets.json/", payload)).data;
      if (loginResponse.status === "success") {
        const sessionData = await loginResponse.data;
        console.log(sessionData);
        this.session = sessionData;
        console.log(JSON.stringify(this.session));
      } else {
        console.log("status: ", loginResponse.status);
        console.log(loginResponse.message);
      }
    },

    async logoutUser(payload) {
      console.log("logoutUser...", payload);
      var response = (await api.delete("/tickets.json/" + payload.ticket)).data;
      console.log(response);

      if (response.status == "success") {
        this.session = {};
      } else {
        console.log("status: ", response.status);
        console.log(response.message);
      }
    },
  },
});
