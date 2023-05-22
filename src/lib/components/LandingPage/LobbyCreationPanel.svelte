<script lang="ts">
	import { env } from "$env/dynamic/public";
	import { createEventDispatcher } from "svelte";
	import { onMount } from "svelte";
	const dispatch = createEventDispatcher();
	export let show = false;
	let numUsers = 1;
	let gameDuration = 30; // in seconds
	let lobbyName = "";
	let lobbyNameIsValid: boolean | null = null;

	let websocket: WebSocket;
	let pin = "";
	let messages: string[] = [];

	onMount(() => {
		websocket = new WebSocket(`${env.PUBLIC_WS_URL}/host`);
		websocket.onmessage = ({ data }) => {
			if (pin) {
				messages = [...messages, data];
			} else {
				pin = data;
			}
		};
	});

	const resetForm = () => {
		numUsers = 1;
		gameDuration = 10;
		lobbyName = "";
	};

	function handleSubmit() {
		if (lobbyNameIsValid) {
			// Handle form submission
		}
	}

	$: {
		if (lobbyName !== "") {
			const regex = /^[a-zA-Z]+$/;
			lobbyNameIsValid = regex.test(lobbyName);
		} else {
			lobbyNameIsValid = null;
		}
	}
</script>

{#if show}
	<div class="panel">
		<div class="panel-content">
			<div class="top-row">
				<h2>Create a lobby</h2>
				<button
					id="close-button"
					on:click={resetForm}
					on:click={() => (show = false)}
					on:click={() => dispatch("close")}>X</button
				>
			</div>
			<form class="form" on:submit|preventDefault={handleSubmit}>
				<label>Name of lobby: {lobbyName}</label>
				{#if lobbyNameIsValid === false}
					<p class="error-message">Name can only contain alphabetical characters</p>
				{/if}
				<input
					type="text"
					id="lobbyName"
					bind:value={lobbyName}
					class:invalid={lobbyNameIsValid === false}
				/>

				<label for="users">Number of users: {numUsers}</label>
				<input type="range" id="users" min="1" max="100" bind:value={numUsers} />

				<label for="duration">Voting Time: {gameDuration} seconds</label>
				<input type="range" id="duration" min="30" max="120" bind:value={gameDuration} />

				<div class="actions">
					<button type="submit" class="button" on:click={() => dispatch("close")}
						><a href="game/{pin}">Create</a></button
					>
				</div>
			</form>
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

	.form {
		@apply pointer-events-auto bg-dark text-fontcolor text-center;
		display: flex;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		flex-direction: column;
		justify-content: center;
		width: 100%;
		border-radius: 6px;
		padding: 16px;
		row-gap: 20px;
	}
	h2 {
		@apply text-6xl;
	}

	#close-button {
		@apply text-fontcolor text-5xl;
		position: absolute;
		right: 1rem;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}

	#close-button:hover {
		@apply text-accent;
	}

	.invalid {
		border: 2px solid red;
		border-radius: 0.25rem;
	}

	.error-message {
		@apply text-accent text-2xl;
	}

	.button {
		@apply text-fontcolor text-4xl;
		text-align: center;
		padding: 0.75rem;
		width: 25%;
		border: 1px solid white;
	}

	.copy-button {
		max-width: 12.5%;
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
		@apply text-accent text-4xl;
		margin: 0 auto;
		color: #fb5012 !important;
	}

	.actions {
		display: flex;
		justify-content: center;
		width: 100%;
	}
</style>
