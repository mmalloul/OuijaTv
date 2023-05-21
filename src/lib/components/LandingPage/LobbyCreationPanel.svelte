<script lang="ts">
	import { env } from "$env/dynamic/public";
	import { createEventDispatcher } from "svelte";
	const dispatch = createEventDispatcher();
	export let show = false;
	export let link = "";
	let numUsers = 1;
	let gameDuration = 10; // in minutes

	const generateLink = () => {
		link = `${env.PUBLIC_WS_URL}/host`;
	};

	const copyLink = () => {
		navigator.clipboard.writeText(link);
	};
</script>

{#if show}
	<div class="panel">
		<div class="panel-content">
			<div class="top-row">
        <h2>Create a lobby</h2>
				<button id="close-button" on:click={() => (show = false)} on:click={() => dispatch("close")}
					>X</button
				>
			</div>

			<label for="users">Number of users: {numUsers}</label>
			<input type="range" id="users" min="1" max="100" bind:value={numUsers} />

			<label for="duration">Game Duration: {gameDuration} minutes</label>
			<input type="range" id="duration" min="10" max="120" bind:value={gameDuration} />

			<div class="actions">
				<button class="button" on:click={() => dispatch("close")}><p>Create</p></button>
			</div>
		</div>
	</div>
{/if}

<style lang="postcss">
	.panel {
		position: absolute;
		top: 50%;
		left: 50%;
    width: 75%;
		transform: translate(-50%, -50%);
	}

  .top-row {
		display: flex;
		justify-content: center;
		width: 100%;
	}

  .panel-content {
		@apply pointer-events-auto bg-dark text-fontcolor text-center;
		display: flex;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		flex-direction: column;
		justify-content: center;
		width: 100%;
		border-radius: 6px;
		padding: 16px;
		border: 1px solid white;
		row-gap: 20px;
	}

	h2 {
		@apply text-6xl;
	}

	#close-button {
		position: absolute;
    right: 1rem;
    
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}

	#close-button:hover {
		@apply text-accent;
	}

	.button {
		@apply text-fontcolor text-4xl;
		text-align: center;
		padding: 0.75rem;
		width: 25%;
		border: 1px solid white;
	}

	.button:hover {
		@apply bg-accent;
	}

  .button > p {
    transition: all 0.2s ease-in-out;
  }

  .button:hover > p {
    transform: scale(1.05);
  }

	label {
		@apply text-fontcolor text-4xl;
	}

	input {
		margin: 0 auto;
	}

	.actions {
		display: flex;
		justify-content: center;
		width: 100%;
	}
</style>
