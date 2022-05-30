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

export const useMpStore = defineStore("mp", {
  // arrow function recommended for full type inference
  state: () => {
    return {
      // 3D Space to render
      space: {
        uuid: "",
        space_sid: "qSGGhhjTYbN",
        space_url: "",
      },

      // all these properties will have their type inferred automatically
      tags: [],
    };
  },

  // filters or format state
  getters: {
    allTags: (state) => state.tags,

    // 3D space source path
    spaceSrc: (state) =>
      "/bundle/showcase.html?m=" +
      state.space.space_sid +
      "&applicationKey=a3ae8341bd8f44899eba16df86307d7d",
  },

  // events that can be triggered, get data from external API and store in the State
  actions: {
    setSpace(payload) {
      this.space = payload;
    },
    setTags(payload) {
      console.log("setTags ...", payload);

      // this.tags is key : value, so use spread operator to update
      // let tags = {};
      // tags[id] = payload;

      this.tags.push(...payload);
    },
  },
});
