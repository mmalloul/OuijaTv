<script lang="ts">
  	import { env } from "$env/dynamic/public";
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
    export let show = false;
    export let link = '';
    let numUsers = 1;
    let gameDuration = 1; // in minutes
  
    const generateLink = () => {
      link = `${env.PUBLIC_WS_URL}/host`; 
    }
  
    const copyLink = () => {
      navigator.clipboard.writeText(link);
    }
</script>
  
<style lang="postcss">
    .lobby-creation-panel {
        position: fixed;
        top: 0;
        bottom: 0;
        right: 0;
        left: 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .panel-content {
        @apply pointer-events-auto bg-dark text-fontcolor opacity-95 text-center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 100%;
        border-radius: 6px;
        padding: 16px;
        border: 1px solid white;
        row-gap: 20px;
    }

    h2 {
        @apply text-3xl
    }
    
    #close-button {
      display: flex;
      justify-content: flex-end;
    } 
    
    #close-button:hover {
      @apply text-accent
    }

    .button {
      @apply text-fontcolor text-4xl
      text-decoration: none;
      text-align: center;
      font-family: theme(fontFamily.amatic);
      padding: .75rem;
      width: 25%;
      border: 1px solid white;
    }

    .button:hover {
      @apply bg-accent
    }

    input {
      @apply text-fontcolor
      margin:0 auto;
    }

    .actions {
      display: flex;
      justify-content: center;
      width:100%;
    }
</style>
  
{#if show}
  <div class="lobby-creation-panel">
    <div class="panel-content">
        <button id="close-button" on:click={() => (show = false)} on:click={() => dispatch('close')}>X</button>
        <h2>Create a lobby</h2>
        <label for="users">Number of users: {numUsers}</label>
        <input type="range" id="users" min="1" max="10" bind:value={numUsers}>
  
        <label for="duration">Game Duration: {gameDuration} minutes</label>
        <input type="range" id="duration" min="1" max="120" bind:value={gameDuration}>
        
        <div class="actions">
          <button class="button" on:click={() => dispatch("close")}>Create</button>
          <button class="button" on:click={generateLink}>Copy Link</button>
          {#if link}
          <div>
            <input type="text" readonly value={link}>
            <button on:click={copyLink}>Copy Link</button>
          </div>
          {/if}
        </div>
    </div>
  </div>
{/if}



  