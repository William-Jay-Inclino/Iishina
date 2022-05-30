//UI 
<template>
  <div>
    <iframe
      :id="space.id"
      :src="this.spaceSrc"
      :width="space.width"
      :height="space.height"
      loading="eager"
      frameborder="0"
      allowfullscreen="true"
    >
    </iframe>
  </div>
</template>

// Logic
<script>
import { useMpStore } from "@/stores/mp";
export default {
  props: {
    space: {
      id: String,
      width: Number,
      height: Number,
    },
  },

  setup() {
    const start = performance.now();

    // reference to MP SDK
    let mpSdk = {};

    // use store
    const mp = useMpStore();

    // trigger action, get layers from API and put in store (state)

    const duration = performance.now() - start;
    console.log("Space3d (ms):", duration);
    return {
      // you can return the whole store instance to use it in the template
      mp,
    };
  },

  mounted() {
    this.getMpSdk();
  },

  // https://my.matterport.com/show/?m=qSGGhhjTYbN
  data() {
    return {};
  },

  methods: {
    async loadedMpSdk() {
      // IMPORTANT: set context to have access to THIS inside callback
      let self = this;

      const showcase = document.getElementById(self.space.id);
      const showcaseWindow = showcase.contentWindow;
      try {
        // connect to 3D Space instance
        let sdk;
        sdk = await showcaseWindow.MP_SDK.connect(showcaseWindow);

        // create this instance (there can be multiple)
        let mpSdk = {};
        mpSdk[self.space.id] = sdk;

        // add to mpSdk pool
        self.mpSdk = { ...self.mpSdk, ...mpSdk };
        console.log("mpSdk loaded...", self.mpSdk);

        // === now CONNECTED to the 3D Space and DO THINGS! ===
        // ex: get MP tags
        self.getMpTags(self.space.id);

        // do more things ...
      } catch (e) {
        console.error(e);
        return;
      }
    },

    getMpSdk() {
      let self = this;
      console.log("getMpSdk...");
      const showcase = document.getElementById(self.space.id);

      // use arrow function to have access to this
      showcase.addEventListener("load", () => {
        // handle when loaded
        this.loadedMpSdk();
      });
    },

    getMpTags(sid) {
      let self = this;
      console.log("getMpTags...");

      self.mpSdk[sid].Mattertag.getData()
        .then(function (mattertags) {
          // Mattertag data retreival complete.
          if (mattertags.length > 0) {
            console.log("mattertags...", mattertags);
            self.mp.setTags(mattertags);
          }
        })
        .catch(function (error) {
          // Mattertag data retrieval error.
        });
    },
  },
  computed: {
    spaceSrc() {
      return (
        "/bundle/showcase.html?m=" +
        this.space.id +
        "&applicationKey=a3ae8341bd8f44899eba16df86307d7d"
      );
    },
  },
};
</script>


// CSS
<style scoped>
.layer_form {
  width: 50vw;
  min-width: 560px;
  max-width: 800px;
  font-family: Verdana, sans-serif;
  text-transform: uppercase;
}

h1 {
  font-style: "bold";
}

.modal-card {
  margin: 20px 20px;
  max-height: calc(100vh - 160px);
  overflow: auto;
  position: relative;
}

.modal-card-foot,
.modal-card-head {
  align-items: center;
  background-color: #f5f5f5;
  display: flex;
  flex-shrink: 0;
  justify-content: flex-end;
  padding: 20px;
  position: relative;
}
.modal-card-head {
  border-bottom: 1px solid #dbdbdb;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
}
.modal-card-body {
  -webkit-overflow-scrolling: touch;
  background-color: #fff;
  flex-grow: 1;
  flex-shrink: 1;
  overflow: auto;
  padding: 20px;
}
.modal-card-foot {
  border-bottom-left-radius: 6px;
  border-bottom-right-radius: 6px;
  border-top: 1px solid #dbdbdb;
}
.modal-card-title {
  color: #363636;
  flex-grow: 1;
  flex-shrink: 0;
  font-size: 1.5rem;
  line-height: 1;
  margin: 0;
  font-weight: 800;
}
.modal-card-foot .o-button:not(:last-child) {
  margin-right: 0.5em;
}

.o-btn--primary,
.o-btn,
.o-chk__check {
  background-color: rgb(222, 30, 26) !important;
}

.space_form_button {
  margin: 0px 10px;
}
</style>