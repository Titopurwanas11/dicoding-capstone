import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ScrapeView from '../views/ScrapeView.vue'
import AnalyzeView from '../views/AnalyzeView.vue'
import HRRankView from '../views/HRRankView.vue'
import SemanticSearchView from '../views/SemanticSearchView.vue'
import ClusterView from '../views/ClusterView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/jobseeker/scrape', component: ScrapeView },
  { path: '/jobseeker/analyze', component: AnalyzeView },
  { path: '/hr/rank', component: HRRankView },
  { path: '/jobseeker/search', component: SemanticSearchView },
  { path: '/hr/cluster', component: ClusterView }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
