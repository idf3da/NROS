import Vue from "vue";
import VueRouter from "vue-router";
import MainMenu from "../views/MainMenu.vue";

Vue.use(VueRouter);

const routes = [
	{
		path: "/main",
		name: "MainMenu",
		component: MainMenu
	},
	{
		path: "/about",
		name: "About",
		component: () => import("../views/About.vue")
	},
	{
		path: "/charts",
		name: "Charts",
		component: () => import("../views/Charts.vue")
	},
	{
		path: "/settings",
		name: "Settings",
		component: () => import("../views/Settings.vue")
	}
];

const router = new VueRouter({
	mode: "history",
	base: process.env.BASE_URL,
	routes
});

export default router;
