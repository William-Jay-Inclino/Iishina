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

export const useSpaceStore = defineStore("space", {
  // arrow function recommended for full type inference
  state: () => {
    return {
      // all these properties will have their type inferred automatically
      spaces: [],

      // proxy to selected active user in List
      selectedSpace: {},

      // layer uuid used to filter and select all spaces with this layer_uuid
      currentLayer: {},

      // layer modal state
      isModalActive: false,

      // create or update
      updateMode: "create",
    };
  },

  // filters or format state
  getters: {
    allSpaces: (state) =>
      state.spaces.sort((a, b) => {
        let an = a.space_sid + a.space_name.toLowerCase();
        let bn = b.space_sid + b.space_name.toLowerCase();

        if (an < bn) {
          return -1;
        }

        if (an > bn) {
          return 1;
        }

        return 0;
      }),

    // needs to implement filter by role
    usersWithRole: (state) => (userRole) => {
      state.spaces;
    },
    allSpacesInCurrentLayer: (state) =>
      state.spaces.filter(function (data) {
        return data.layer_uuid == state.currentLayer.uuid;
      }),
  },

  // events that can be triggered, get data from external API and store in the State
  actions: {
    async getSpaces() {
      this.spaces = await (await api.get("/spaces.json/")).data.data;
    },

    async saveSpace(payload) {
      console.log("saveSpace...", payload);
      if (!!payload.uuid) {
        const space = await (await api.put("/spaces.json/", payload)).data.data;

        // find the index of item to update
        const idx = this.spaces.findIndex((item) => (item.uuid = payload.uuid));
        console.log("index...", idx);

        // replace update the item at index
        this.spaces.splice(idx, 1, space);
      } else {
        const space = await (
          await api.post("/spaces.json/", payload)
        ).data.data;
        console.log(this.space);
        this.spaces.push(space); //temporary, originally this.spaces.unshift(space);
      }
    },

    async deleteSpace(payload) {
      const response = await api.delete("/spaces/" + payload.uuid);
      console.log("deleteUser...", response.data);

      // record was actually deleted
      if (response.status == 200) {
        this.spaces = this.spaces.filter((item) => item.uuid != payload.uuid);
      }
    },

    setSelectedSpace(payload) {
      this.selectedSpace = payload;
    },

    setCurrentLayer(payload) {
      this.currentLayer = payload;
    },
  },
});
