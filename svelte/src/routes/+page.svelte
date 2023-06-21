<script lang="ts">
	import LobbyCreationPanel from "$lib/components/landing-page/LobbyCreationPanel.svelte";
	import { goto } from "$app/navigation";

	let showLobbyCreationPanel = false;
</script>

<div class="page container">
	{#if !showLobbyCreationPanel}
		<div class="home">
			<h1>Ouija.tv</h1>

			<h4 class="text-2xl lg:text-5xl">Unleash the mysteries of the paranormal with Ouija.tv!</h4>

			<div
				class="text-start font-montserrat text-center text-xs text-fontcolor max-w-[50ch] sm:text-base lg:text-lg"
			>
				<p class="md:px-8">
					We reinvented the Ouija board for the digital age:<br />
					<strong>Host</strong> a lobby and <strong>invite</strong> your friends to join your lobby
					as spirits.<br />
				</p>
				<p class="md:px-8 mt-2">
					You can ask them a question, or let them fill out an empty word. The spirits will guide
					the seeker to the letters by voting, and spell out their answer one letter at a time.
				</p>
				<div
					class="flex flex-row items-center justify-center space-x-8 font-amatic text-xl lg:text-3xl"
				>
					<button type="button" class="big-button" on:click={() => (showLobbyCreationPanel = true)}>
						<p>Host a lobby</p>
					</button>

					<button type="button" class="big-button" on:click={() => goto("/join")}>
						<p>Join a lobby</p>
					</button>
				</div>
				<p class="md:px-8 mt-4">
					<strong>Streamers:</strong> With a seamless integration of Twitch chat, you can engage
					your viewers in an exciting, interactive experience, where their collective input guides
					you on your streams!<br />
					<strong>Solo explorers:</strong> Engage in a spiritual session with our sophisticated AI.
				</p>
			</div>
		</div>
	{/if}

	<LobbyCreationPanel bind:showLobbyCreationPanel />
</div>

<style lang="postcss">
	.container {
		@apply flex flex-col items-center;
	}

	.home {
		@apply flex flex-col items-center h-full w-full mt-15 md: mt-50;
	}

	h1 {
		@apply text-fontcolor text-8xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		margin-bottom: 2rem;
	}

	h4 {
		@apply text-fontcolor mb-4 text-center;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		line-height: 1.35em;
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
