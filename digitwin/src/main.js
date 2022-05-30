import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";

import Oruga from "@oruga-ui/oruga-next";

// Oruga full allows you to use the full capabilities of oruga
// See documentation https://oruga.io/documentation/#configuration
import "@oruga-ui/oruga-next/dist/oruga-full.css";

// import { library, dom } from "@fortawesome/fontawesome-svg-core";
// import { fas } from "@fortawesome/free-solid-svg-icons";
import "@mdi/font/css/materialdesignicons.min.css";
// To implement mdi icons in your component:
// Use o-icon syntax from https://oruga.io/components/Icon.html#examples
// Change pack to "mdi" and icon to any of the icon names in https://pictogrammers.github.io/@mdi/font/6.5.95/
// For example, you will see "F1960 mdi-account-lock-open" from mdi icon names. Just use "account-lock-open"
// <o-icon pack="mdi" icon="account-lock-open" size="large"> </o-icon>

const app = createApp(App);

// connect plugins
app.use(router);
app.use(createPinia());

// oruga components
app.use(Oruga);

// fontawesome;
// library.add(faTrashCan);

app.mount("#app");
