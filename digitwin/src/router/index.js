import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginView from "@/views/LoginView.vue";
import SpaceListView from "@/views/SpaceListView.vue";
import OwnerListView from "@/views/OwnerListView.vue";
import LayerListView from "@/views/LayerListView.vue";
import StoreTest from "@/components/StoreTest.vue";
import LayerTreeView from "@/views/LayerTreeView.vue";
import Space3DView from "@/views/Space3dView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: LoginView,
    },
    {
      path: "/space",
      name: "space List",
      component: SpaceListView,
    },

    {
      path: "/space/3d",
      name: "space 3D",
      // component: Space3DView,
      component: () => import("../views/Space3dView.vue"),
    },

    {
      path: "/owner",
      name: "Owner List",
      component: OwnerListView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/layer",
      name: "layer",
      component: LayerListView,
    },

    {
      path: "/layer/tree",
      name: "tree",
      component: LayerTreeView,
    },

    {
      path: "/store",
      name: "store",
      component: StoreTest,
    },
  ],
});

export default router;
