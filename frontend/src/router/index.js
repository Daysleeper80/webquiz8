/**
 * Creates the frontend router, with all the routes and rules to 
 * transition between views.
 * 
 * (c) Joao Galamba, 2022
 * $LICENSE(MIT)
 */

import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import PublicView from "../views/PublicView.vue";
import NotFoundView from "../views/NotFoundView.vue";

import { sessionManager } from "../assets/scripts/user-management";

const routes = [
    {
        name: 'root',
        path: '/',
        redirect: '/public',
    },
    {
        name: 'home',
        path: '/home',
        component: HomeView,
        meta: {
            requiresAuth: true,
        },
    },
    {
        name: 'public',
        path: '/public',
        component: PublicView,
        async beforeEnter() {
            if (await sessionManager.isLoggedIn()) {
                return {
                    name: 'home',
                    replace: true,
                };
            }
        },
    },
    {
        name: 'login',
        path: '/login',
        component: LoginView,
        // https://router.vuejs.org/guide/advanced/navigation-guards.html#in-component-guards
        async beforeEnter() {
            if (await sessionManager.isLoggedIn()) {
                return {
                    name: 'home', 
                    replace: true,
                };
            }
        },
        props: true,   // for the returnPath
    },
    {
        name: 'logout',
        path: '/logout',
        async beforeEnter() {
            await sessionManager.logout();
            return {
                name: 'public', 
                replace: true,
            };
        }
    },
    {
        name: 'signup',
        path: '/signup',
        component: SignupView,
        async beforeEnter() {
            if (await sessionManager.isLoggedIn()) {
                return {
                    name: 'home', 
                    replace: true,
                };
            }
        },
    },
    {
        name: "about",
        path: "/about",
        // route level code-splitting
        // this generates a separate chunk (About.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import("../views/AboutView.vue"),
    },
    {
        // https://router.vuejs.org/guide/migration/#removed-star-or-catch-all-routes
        // https://router.vuejs.org/guide/essentials/dynamic-matching.html#catch-all-404-not-found-route
        path: '/:notFoundPathMatch(.*)',
        name: 'not-found',
        component: NotFoundView,
        // props: true,
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

// https://router.vuejs.org/guide/advanced/navigation-guards.html#global-before-guards
router.beforeEach(async function(to) {
    const privateAccess = to.matched.some(routeRecord => routeRecord.meta.requiresAuth);
    if (privateAccess && !await sessionManager.isLoggedIn()) {
        return {
            name: 'login',
            params: { returnPath: to.fullPath },
            replace: true,
        };
    }
});

export default router;
