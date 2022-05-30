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

export const useEventStore = defineStore("event", {
  // arrow function recommended for full type inference
  state: () => {
    return {
      // all these properties will have their type inferred automatically
      events: [],

      // proxy to selected active event
      selectedEvent: {},
    };
  },

  // filters or format state
  getters: {
    allEvents: (state) =>
      state.events.sort((a, b) => {
        let an = a.event_name.toLowerCase();
        let bn = b.event_name.toLowerCase();

        if (an < bn) {
          return -1;
        }

        if (an > bn) {
          return 1;
        }

        return 0;
      }),

    eventsInCurrentSpace: (state) =>
      state.events.filter(
        (item) => item.space_uuid == state.selectedSpace.uuid
      ),
  },

  // events that can be triggered, get data from external API and store in the State
  actions: {
    async getEvents() {
      this.events = await (await api.get("/events.json/")).data.data;
    },

    async saveEvent(payload) {
      console.log("saveEvent...", payload);
      if (!!payload.uuid) {
        const event = await (await api.put("/events.json/", payload)).data.data;

        // find the index of item to update
        const idx = this.events.findIndex((item) => (item.uuid = payload.uuid));
        console.log("index...", idx);

        // replace update the item at index
        this.events.splice(idx, 1, event);
      } else {
        const event = await (
          await api.post("/events.json/", payload)
        ).data.data;
        console.log(this.event);
        this.events.push(event); //temporary, originally this.events.unshift(event);
      }
    },

    async deleteEvent(payload) {
      const response = await api.delete("/events/" + payload.uuid);
      console.log("deleteUser...", response.data);

      // record was actually deleted
      if (response.status == 200) {
        this.events = this.events.filter((item) => item.uuid != payload.uuid);
      }
    },

    setSelectedEvent(payload) {
      this.selectedEvent = payload;
    },
  },
});
