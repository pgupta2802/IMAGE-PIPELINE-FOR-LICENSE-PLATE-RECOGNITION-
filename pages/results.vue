<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-4">
    <nav class="text-sm text-gray-500 mb-4">
      <nuxt-link to="/">Home</nuxt-link> › <span class="font-medium">License Plate Recognition Results</span>
    </nav>
    <h1 class="text-3xl font-bold text-gray-800 mb-6">License Plate Recognition Results</h1>

    <!--Results-->
    <div class="items-center flex flex-col">
      <div class="w-36 h-36 mb-3">
        <img class="object-cover w-full h-full object-cover rounded-md" :src="image"/>
      </div>

      <div class="overflow-hidden rounded-lg border border-slate-300 shadow-lg">
        <table class="table-auto w-full text-left text-sm">
          <thead class="bg-purple-500 text-white">
            <tr>
              <th class="table-header">Field</th>
              <th class="table-header">Result</th>
            </tr>
          </thead>
          <tbody>
            <tr class="table-row">
              <td class="table-row-first-cell">License Plate</td>
              <td class="table-row-cell">{{ result.plate }}</td>
            </tr>
            <tr class="table-row">
              <td class="table-row-first-cell">Region</td>
              <td class="table-row-cell">{{  result.region.trim() === "" ? "N/A" : result.region }}</td>
            </tr>
            <tr class="table-row">
              <td class="table-row-first-cell">Confidence</td>
              <td class="table-row-cell">{{ result.confidence.toFixed(2) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
</div>
</template>

<style scoped>
  .table-header {
    @apply px-4 py-2 font-medium;
  }

  .table-row {
    @apply odd:bg-white even:bg-slate-100;
  }

  .table-row-cell {
    @apply px-4 py-3;
  }

  .table-row-first-cell {
    @apply table-row-cell font-medium text-purple-500
  }
</style>

<script>
import { useStore } from '../store/store';

definePageMeta({
  middleware: 'restrict',
});

export default {
  computed: {
    result() {
      const store = useStore();
        return store.result;
    },
    image() {
      const store = useStore();
      return store.image;
    }
  }
}
</script>

