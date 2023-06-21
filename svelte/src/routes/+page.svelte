<script lang="ts">
	import LobbyCreationPanel from "$lib/components/landing-page/LobbyCreationPanel.svelte";
	import { goto } from "$app/navigation";

	let showLobbyCreationPanel = false;
</script>

<div class="page container">
	{#if !showLobbyCreationPanel}
		<div class="home">
			<h1>Ouija.tv</h1>

			<h4>Unleash the mysteries of the paranormal with Ouija.tv!</h4>

			<div class="content">
				<div class="flex flex-col gap-2">
					<p class="md:px-8">
						We reinvented the Ouija board for the digital age:<br />
						<strong>Host</strong> a lobby and <strong>invite</strong> your friends to join your
						lobby as spirits.<br />
					</p>

					<p class="md:px-8 mt-2">
						You can ask them a question, or let them fill out an empty word. The spirits will guide
						the seeker to the letters by voting, and spell out their answer one letter at a time.
					</p>
				</div>
				<div class="button-container">
					<button type="button" class="big-button" on:click={() => (showLobbyCreationPanel = true)}>
						<p>Host a lobby</p>
					</button>

					<button type="button" class="big-button" on:click={() => goto("/join")}>
						<p>Join a lobby</p>
					</button>
				</div>

				<div class="flex flex-col md:flex-row">
					<div>
						<h4>Streamers</h4>

						<p class="md:px-8">
							Through a seamless integration with Twitch chat, you have the incredible opportunity
							to engage your viewers in a dynamic and interactive journey. As you navigate the Ouija
							board, their collective input becomes a driving force, guiding you to the letters that
							spell out their messages.
						</p>
					</div>

					<div>
						<h4>Solo Explorers</h4>

						<p class="md:px-8">
							In this unique game mode called "Solo," you can connect with different AI characters.
							Engage in intriguing conversations and experience the uncanny as these AI entities
							respond through the mystical Ouija board. Choose your character, seek wisdom, explore,
							and unleash your imagination.
						</p>
					</div>
				</div>
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
		@apply flex flex-col items-center h-full w-full mt-15 md:justify-center;
		max-width: 800px; // max-width home content
	}

	h1 {
		@apply text-fontcolor text-8xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		margin-bottom: 2rem;
	}

	h4 {
		@apply text-fontcolor mb-4 text-center text-2xl lg:text-5xl font-amatic;
		text-decoration: none;
		line-height: 1.35em;
	}

	.content {
		@apply flex flex-col gap-6 font-montserrat text-center text-xs text-fontcolor sm:text-base lg:text-lg;
	}

	.top-row {
		display: flex;
		justify-content: space-between;
		width: 100%;
	}

	.button-container {
		@apply flex flex-row items-center justify-center space-x-8 font-amatic text-xl lg:text-3xl;
	}
</style>
