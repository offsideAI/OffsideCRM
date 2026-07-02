<script lang="ts">
  import type { IconComponent } from '$lib/types';
  import { cn } from '$lib/utils/cn';

  // Thin wrapper to render a Lucide icon component with consistent sizing.
  interface Props {
    icon: IconComponent;
    size?: number;
    strokeWidth?: number;
    class?: string;
  }

  let { icon: IconCmp, size = 16, strokeWidth, class: className }: Props = $props();
</script>

<IconCmp {size} {strokeWidth} class={cn('shrink-0', className)} />
