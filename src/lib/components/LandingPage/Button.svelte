<script>
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
  
    export let title = '';
  </script>
  
  <style lang="postcss">
    .box {
      @apply text-fontcolor text-4xl
      text-decoration: none;
      text-align: center;
      font-family: theme(fontFamily.amatic);
      padding: .75em;
      width: 50%;
      border: 1px solid white;
    }

    .box:hover {
      @apply cursor-pointer bg-accent opacity-75
    }
  </style>
  
  <div class="box" on:click={() => dispatch('click')}>
    {title}
  </div>
  