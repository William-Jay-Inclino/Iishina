import { defineStore } from "pinia";
import axios from "axios";
import { isObject } from "@vue/shared";
// import { faBatteryThreeQuarters } from "@fortawesome/free-solid-svg-icons";

const apiURL = import.meta.env.VITE_API_URL + "/v1";
console.log("apiURL...", apiURL);

const api = axios.create({
  baseURL: apiURL,
});

export const useLayerStore = defineStore("layer", {
  // arrow function recommended for full type inference
  state: () => {
    return {
      // all these properties will have their type inferred automatically
      layers: [],

      // layer tree (this is compatible to TreeItem,vue)
      tree: [],

      // selected active layer
      selectedLayer: {},

      // current layer for filter
      currentLayer: {},

      // layer modal state
      isModalActive: false,

      // create or update
      updateMode: "create",
    };
  },

  // filters or format state
  getters: {
    allLayers: (state) =>
      state.layers.sort((a, b) => {
        let an = a.layer_name.toLowerCase();
        let bn = b.layer_name.toLowerCase();

        if (an < bn) {
          return -1;
        }

        if (an > bn) {
          return 1;
        }

        return 0;
      }),

    layerTree: (state) => state.tree,
    //Get Current Layer
    getCurrentLayer: (state) => state.currentLayer,
    //Get Filtered Layers based on Current Layer
    allLayersInCurrentLayer: (state) =>
      state.layers.filter(function (data) {
        return data.parent_uuid == state.currentLayer.uuid;
      })
    ,
    getParentLayer: (state) =>
      state.layers.filter(function (data) {
        return data.uuid == state.currentLayer.parent_uuid;
      })
    ,
  },

  // events that can be triggered, get data from external API and store in the Stage
  actions: {
    async getLayers() {
      this.layers = await (await api.get("/layers.json/")).data.data;
    },

    async getLayerTree() {
      try {
        let res = await (await api.get("/trees.json/")).data.data;
        // console.log("TREE", JSON.stringify(res));

        // map data to format usable for TreeItem
        let mynodes = {};
        var getNodes = (node) => {
          let my_nodes = {};
          Object.keys(node).forEach((key, index) => {
            let item = node[key];

            let node_children = [];
            if (Object.keys(item).includes("children") == true) {
              let children = item["children"];
              console.log(children);
              children.forEach((child) => {
                console.log("child", child);
                node_children.push(getNodes(child)); my_nodes = {
                  name: item.data.layer_name,
                  uuid: item.data.uuid,
                  data: item.data,
                  children: node_children,
                };
              });
            } else {
              my_nodes = {
                name: item.data.layer_name,
                uuid: item.data.uuid,
                data: item.data,
              };
            }
          });
          return my_nodes;
        };

        this.tree = getNodes(res);
      } catch (e) {
        console.log(e)
        // In cases where layer list is empty and there is no layer
        // Create root layer
        this.saveLayer({
          layer_name: "root",
        })
      }
    },

    async saveLayer(payload) {
      console.log("saveLayer...", payload, payload.uuid);
      if (!!payload.uuid) {
        const layer = await (
          await api.put("/layers/" + payload.uuid + ".json/", payload)
        ).data.data;

        // find the index of item to update
        const idx = this.layers.findIndex((item) => item.uuid == payload.uuid);
        console.log("index...", idx);

        // replace update the item at index
        this.layers.splice(idx, 1, layer);
      } else {
        const layer = await (
          await api.post("/layers.json/", payload)
        ).data.data;
        this.layers.unshift(layer);
      }
    },

    async deleteLayer(payload) {
      const response = await api.delete("/layers/" + payload.uuid);
      console.log("deleteLayer...", response.data);

      // record was actually deleted
      if (response.status == 200) {
        this.layers = this.layers.filter((item) => item.uuid != payload.uuid);
      }
    },

    async setCurrentLayer(payload) {
      this.currentLayer = payload;
    }
  },
});
