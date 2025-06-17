import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import installElementPlus from './plugins/element';
import PDFObjectPlugin from 'pdfobject-vue';

const app = createApp(App);
installElementPlus(app);
app.use(router);
app.use(PDFObjectPlugin);
app.mount('#app');
