import Vue from "vue";
import App from "./App.vue";
import vuetify from "./plugins/vuetify";
import router from "./router";
import { ChartPlugin } from "@syncfusion/ej2-vue-charts";

Vue.use(ChartPlugin);
Vue.config.productionTip = false;

new Vue({
	vuetify,
	router,
	render: h => h(App)
}).$mount("#app");
