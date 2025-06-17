import { createRouter, createWebHistory } from 'vue-router';
import CipherForm from './views/CipherForm.vue';
import HomePage from './views/HomePage.vue';
import ReboundAnalysis from './views/ReboundAnalysis.vue';
import BitSbox from './views/BitSbox.vue';
import BitAlgorithm from './views/BitAlgorithm.vue';
import ByteMDS from './views/ByteMDS.vue';
import ByteAlgorithm from './views/ByteAlgorithm.vue'
import DiffCollision from './views/DifferentialCollision.vue';
import MitmAnalysis from './views/MitMAnalysis.vue';

// import UserLogin from './components/UserLogin.vue';  // 导入 UserLogin 组件

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomePage
    },
    {
        path: '/cipherForm',
        name: 'CipherForm',
        component: CipherForm,
    },
    {
        path: '/rebound-analysis',
        name: 'ReboundAnalysis',
        component: ReboundAnalysis,
    },
    {
        path: '/bit-sbox',
        name: 'BitSbox',
        component: BitSbox,
    },
    {
        path: '/bit-algorithm',
        name: 'BitAlgorithm',
        component: BitAlgorithm,
    },
    {
        path: '/byte-algorithm',
        name: 'ByteAlgorithm',
        component: ByteAlgorithm,
    },
    {
        path: '/byte-mds',
        name: 'ByteMDS',
        component: ByteMDS,
    },
    {
        path: '/diff-collision',
        name: 'DiffCollision',
        component: DiffCollision,
    },
    {
        path: '/mitm-analysis',
        name: 'MitmAnalysis',
        component: MitmAnalysis,
    }

    // {
    //     path: '/login',
    //     name: 'UserLogin',
    //     component: UserLogin,
    // },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
