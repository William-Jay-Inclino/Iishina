import { defineStore } from "pinia";
import axios from "axios";

const apiURL = import.meta.env.VITE_API_URL + "/v1";
console.log("apiURL...", apiURL);

const api = axios.create({
  baseURL: apiURL,
  mode: "cors",
  credentials: "include",
  headers: {
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/json",
  },
});

export const useUserStore = defineStore("user", {
  // arrow function recommended for full type inference
  state: () => {
    return {
      // all these properties will have their type inferred automatically
      users: [],

      // proxy to selected active user in List
      selectedUser: {},

      isModalActive: false,
      updateMode: "create",
    };
  },

  // filters or format state
  getters: {
    allUsers: (state) => state.users,

    // needs to implement filter by role
    usersWithRole: (state) => (userRole) => {
      state.users;
    },
  },

  // events that can be triggered, get data from external API and store in the State
  actions: {
    async getUsers() {
      this.users = await (await api.get("/users.json/")).data.data;
    },

    async saveUser(payload) {
      console.log("saveUser...", payload);
      if (payload.uuid !== undefined) {
        const user = await (
          await api.put("/users/" + payload.uuid + ".json/", payload)
        ).data.data;

        // find the index of item to update
        const idx = this.users.findIndex((item) => item.uuid == payload.uuid);
        console.log("index...", idx);

        // replace update the item at index
        this.users.splice(idx, 1, user);
      } else {
        const user = await (await api.post("/users.json/", payload)).data.data;

        this.users.push(user);
      }
    },

    async deleteUser(payload) {
      const response = await api.delete("/users/" + payload.uuid);
      console.log("deleteUser...", response.data);

      // record was actually deleted
      if (response.status == 200) {
        this.users = this.users.filter((item) => item.uuid != payload.uuid);
      }
    },

    setSelectedUser(payload) {
      this.setSelectedUser = payload;
    },
  },
});
