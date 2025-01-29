import { defineStore } from 'pinia';
import results from '../aws/results';

export const useStore = defineStore('store', {
  state: () => ({
    result: null,
    image: "",
    ext: ""
  }),
  actions: {
    setImage(image, ext) {
        this.image = image;
        this.ext = ext;
    },
    async pollResult(uploadId) {
        if (!uploadId) {
            throw new Error("No upload ID")
        }
        const maxAttempts = 40;
        const delay = 5000;
        let attempts = 0;

        await new Promise((resolve) => setTimeout(resolve, 30000)); 
        while (attempts < maxAttempts) {
            this.result = await results(uploadId);
            if (this.result) {
                return true;
            }
            attempts++;
            await new Promise((resolve) => setTimeout(resolve, delay)); 
        }
        return false; 
    }
  },
});