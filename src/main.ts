import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { i18n } from './i18n'
import { restoreSession } from './store'
import './style.css'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import en from 'element-plus/es/locale/lang/en'

/* 先恢复登录态（读 localStorage token 并校验），再挂载应用，路由守卫才能正确放行 */
restoreSession().finally(() => {
  const app = createApp(App)
  app.use(router)
  app.use(i18n)
  app.use(ElementPlus, { locale: i18n.global.locale.value === 'zh' ? zhCn : en })
  app.mount('#app')
})
