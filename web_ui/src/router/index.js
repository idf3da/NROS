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
	},
	{
		path: "/data_checker",
		redirect: 'data_checker/types',
		name: "DataChecker",
	},
	{
		path: "/data_checker/types",
		name: "DataChecker",
		component: () => import("../views/Types.vue")
	},
	{
		path: "/data_checker/items",
		name: "DataChecker",
		component: () => import("../views/Items.vue")
	},
	{
		path: "/data_checker/groups",
		name: "DataChecker",
		component: () => import("../views/Groups.vue")
	},
	{
		path: "/data_checker/locations",
		name: "DataChecker",
		component: () => import("../views/Locations.vue")
	},
];

const router = new VueRouter({
	mode: "history",
	base: process.env.BASE_URL,
	routes
});

export default router;
