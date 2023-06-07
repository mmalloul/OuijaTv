<script lang="ts">
	import LobbyCreationPanel from "$lib/components/landing-page/LobbyCreationPanel.svelte";
	import { goto } from "$app/navigation";

	let showLobbyCreationPanel = false;
</script>

<div class="page container">
	{#if !showLobbyCreationPanel}
		<h1>Ouija.tv</h1>

		<h4>
			Unleash the mysteries of the paranormal with Ouija.tv, a cutting-edge application that
			reinvents the traditional Ouija board for the digital age. With a seamless integration of
			Twitch chat, you can engage your viewers in an exciting, interactive experience, where your
			collective input guides the planchette. Solo explorers can engage in a compelling match with
			our sophisticated AI. Whether you're an experienced Ouija player or a curious novice, Ouija.tv
			puts the mystery and excitement of the classic lounge game at your fingertips.
		</h4>

		<div class="top-row">
			<button type="button" class="custom-button" on:click={() => (showLobbyCreationPanel = true)}>
				<p>Host a lobby</p>
			</button>

			<button type="button" class="custom-button" on:click={() => goto("/join")}>
				<p>Join a lobby</p>
			</button>
		</div>
	{/if}

	<LobbyCreationPanel bind:showLobbyCreationPanel />
</div>

<style lang="postcss">
	.container {
		@apply flex flex-col items-center text-center md: justify-center;
	}

	h1 {
		@apply text-fontcolor text-8xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		margin-bottom: 2rem;
	}

	h4 {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		line-height: 1.35em;
		margin-bottom: 3rem;
		font-size: calc(1em + 1vw); /* Responsive font-size */
		overflow: auto; /* Adds scroll when the content overflows */
	}

	.top-row {
		display: flex;
		justify-content: space-between;
		width: 100%;
	}

	.custom-button {
		@apply text-fontcolor text-4xl m-2 border-1;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		padding: 0.75em;
		width: 50%;
		border-color: #dddddd;
		transition: all 0.2s ease-in-out;
		font-size: calc(1em + 1vw); /* Responsive font-size */
		overflow: auto; /* Adds scroll when the content overflows */
	}

	.custom-button > p {
		transition: all 0.2s ease-in-out;
	}

	.custom-button:hover {
		@apply cursor-pointer bg-dark opacity-75;
		border-style: solid;
	}

	.custom-button:hover > p {
		@apply text-accent;
	}

	.custom-button:hover > p {
		transform: scale(1.05);
	}
</style>
