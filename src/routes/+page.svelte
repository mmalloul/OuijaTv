<script lang="ts">
	import LobbyCreationPanel from "#lib/components/LandingPage/LobbyCreationPanel.svelte";
	import { goto } from "$app/navigation";

	let showLobbyCreationPanel = false;
</script>

<div class="container">
	<div class="top-row">
		{#if !showLobbyCreationPanel}
			<button type="button" class="custom-button" on:click={() => (showLobbyCreationPanel = true)}>
				<p>Host Game</p>
			</button>
			<button type="button" class="custom-button" on:click={() => goto("/join")}>
				<p>Join Game</p>
			</button>
		{/if}
		<LobbyCreationPanel bind:showLobbyCreationPanel />
	</div>
</div>

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
		width: 100%;
	}

	.custom-button {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		padding: 0.75em;
		width: 50%;
		border: 1px solid white;
		transition: all 0.2s ease-in-out;
	}

	.custom-button > p {
		transition: all 0.2s ease-in-out;
	}

	.custom-button:hover {
		@apply cursor-pointer bg-accent opacity-75;
		transform: scale(1.01);
	}

	.custom-button:hover > p {
		transform: scale(1.05);
	}
</style>
