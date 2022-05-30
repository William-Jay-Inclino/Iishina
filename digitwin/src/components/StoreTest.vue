//UI 
<template>
  <div>
    <h1>STORE TEST</h1>
  </div>
</template>

// Logic Store
<script>
import { useLayerStore } from "@/stores/layer";
import { useUserStore } from "@/stores/user";
import { useSessionStore } from "@/stores/session";
import { useEventStore } from "@/stores/event";

export default {
  setup() {
    // use store
    const layer = useLayerStore();
    const user = useUserStore();
    const session = useSessionStore();
    const event = useEventStore();

    // trigger action, get layers from API and put in store (state)
    layer.getLayers();
    user.getUsers();
    session.loginUser({ email: "admin@gmail.com", password: "admin123" });
    // session.getSession();

    event.getEvents();

    return {
      // you can return the whole store instance to use it in the template
      layer,
      user,
      session,
    };
  },

  methods: {
    submitLayer(payload) {
      this.layer.saveLayer(payload);
      this.new_layer = "";
    },
  },
};
</script>


// CSS
<style>
h1 {
  font-style: "bold";
}
</style>