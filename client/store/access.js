import { defineStore } from 'pinia';

export const useAccessStore = defineStore('access', {
    state: () => ({
      pageAccess: {}
    }),
    actions: {
        grantAccess(page) {
            this.pageAccess[page] = true;
        },
        revokeAccess(page) {
            this.pageAccess[page] = false;
        },
        revokeAllAccess() {
            this.pageAccess = {}
        }
    }
  });