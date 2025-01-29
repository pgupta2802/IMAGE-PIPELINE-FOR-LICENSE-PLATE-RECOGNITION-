<template>
    <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 class="text-xl font-semibold mb-4">Processing...</h1>
      <div class="mt-10 mb-3">
        <LoadingAnimation />
      </div>
      <p class="text-gray-500 mt-4">Please wait while we process your image.</p>
    </div>
</template>

<script>
    import LoadingAnimation from '../components/LoadingAnimation.vue';
    import { useStore } from '../store/store';
    import { useAccessStore } from '../store/access';
    import upload from '../aws/upload';

    definePageMeta({
        middleware: 'restrict',
    });

    export default {
        async mounted() {
            const store = useStore(); 

            const uploadId = await upload(store.ext, store.image.split(",")[1]);

            try { 
                const success = await store.pollResult(uploadId);
                if (success) {
                    const accessStore = useAccessStore();
                    const path = "/results"
                    accessStore.grantAccess(path); 
                    await navigateTo({ path: path});
                } else {
                    await navigateTo({ path: "/"});
                }
            } catch(e) {
                throw e;
            }
        }
    }
</script>