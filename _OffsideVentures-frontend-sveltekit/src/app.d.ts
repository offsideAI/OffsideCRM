// See https://svelte.dev/docs/kit/types#app.d.ts
declare global {
  namespace App {
    // interface Error {}
    interface Locals {
      user: import('$lib/types').CurrentUser | null;
    }
    // interface PageData {}
    interface PageState {}
    // interface Platform {}
  }
}

export {};
