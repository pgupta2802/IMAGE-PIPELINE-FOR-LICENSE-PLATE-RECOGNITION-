<template>
    <div class="grid grid-cols-4 gap-20 -ml-10 -mt-10">
        <div class="relative">
            <div class="base-circle border-2 border-gray-300"></div>
            <div
                class="coloured-spin border-2 border-purple-200">
            </div>
        </div>

        <div class="relative">
            <div class="base-circle border-4 border-gray-300"></div>
            <div
                class="coloured-spin border-4 border-purple-400">
            </div>
        </div>

        <div class="relative">
            <div class="base-circle border-8 border-gray-300"></div>
            <div
                class="coloured-spin border-8 border-purple-600">
            </div>
        </div>
        <div class="relative">
            <div class="base-circle border-[16px] border-gray-300"></div>
            <div
                class="coloured-spin border-[16px] border-purple-800">
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'LoadingAnimation',
    };
</script>

<style scoped>
    .coloured-spin {
        @apply w-14 h-14 rounded-full animate-spin absolute border-t-transparent border-solid;
    }
    .base-circle {
        @apply w-14 h-14 rounded-full absolute border-solid;
    }
</style>