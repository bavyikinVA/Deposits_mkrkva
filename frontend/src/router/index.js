import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import CatalogPage from '../pages/CatalogPage.vue'
import CalculatorPage from '../pages/CalculatorPage.vue'

const routes = [
    { path: '/', name: 'home', component: HomePage },
    { path: '/catalog', name: 'catalog', component: CatalogPage },
    { path: '/calculator', name: 'calculator', component: CalculatorPage }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior() {
        return { top: 0 }
    }
})

export default router