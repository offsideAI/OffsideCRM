export type ToastTone = 'neutral' | 'success' | 'danger' | 'info';

export interface ToastItem {
  id: number;
  message: string;
  tone: ToastTone;
}

class ToastStore {
  items = $state<ToastItem[]>([]);
  #seq = 0;

  push(message: string, tone: ToastTone = 'neutral', duration = 3500): number {
    const id = ++this.#seq;
    this.items.push({ id, message, tone });
    if (duration > 0) setTimeout(() => this.dismiss(id), duration);
    return id;
  }

  dismiss(id: number) {
    this.items = this.items.filter((item) => item.id !== id);
  }
}

export const toasts = new ToastStore();

/** Convenience: `toast('Saved', 'success')`. */
export const toast = (message: string, tone: ToastTone = 'neutral', duration?: number) =>
  toasts.push(message, tone, duration);
