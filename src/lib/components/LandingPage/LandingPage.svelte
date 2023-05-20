<script>
  import Box from './Box.svelte';
	import LobbyList from './LobbyList.svelte';
  
    let lobbies = []; // The list of lobbies.
  
    const joinLobby = () => {
      // your logic to join a lobby
    }
  
    const createLobby = () => {
      // your logic to create a lobby
    }
  </script>
  
  <style lang="postcss">
    .container {
      position: absolute;
      top: 50%;
      left: 50%;
      max-width: 50%;
      transform: translate(-50%, -50%);
	  }
    .top-row {
      display: flex;
      justify-content: space-between;
      width:100%;
    }
  </style>
  
  <div class="container">
    <div class="top-row">
      <Box title="Host game" on:click={createLobby} />
      <Box title="Join game" on:click={joinLobby} />
    </div>
    <LobbyList></LobbyList> 
  </div>