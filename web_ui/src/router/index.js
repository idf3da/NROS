import Home from "../views/Home.vue";
import Vue from "vue";
import VueRouter from "vue-router";

import store from '../store' // your vuex store

Vue.use(VueRouter);

// eslint-disable-next-line no-unused-vars
const ifNotAuthenticated = (to, from, next) => {
    if (!store.getters.isAuthenticated) {
        next();
        return
    }
    next('/')
};

const routes = [
    {
        path: "/main",
        name: "Home",
        component: Home
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
        path: "/orders",
        name: "Orders",
        //component: () => import("../views/Orders.vue")
    },
    {
        path: "/settings",
        name: "Settings",
        component: () => import("../views/Settings.vue")
    },
    {
        path: "/help",
        name: "Help",
        //component: () => import("../views/Help.vue")
    },
    {
        path: "/map",
        name: "Map",
        component: () => import("../views/Map.vue")
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
