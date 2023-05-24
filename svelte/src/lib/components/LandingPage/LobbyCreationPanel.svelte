<script lang="ts">
	import { PlayerState } from "#lib/types/PlayerState";
	import { goto } from "$app/navigation";
	import { createEventDispatcher, getContext } from "svelte";
	import type { Writable } from "svelte/store";
	const dispatch = createEventDispatcher();
	const playerState = getContext<Writable<PlayerState>>("playerState");
	export let showLobbyCreationPanel = false;
	let numUsers = 1;
	let gameDuration = 30; // in seconds
	let lobbyName = "";
	let lobbyNameIsValid: boolean | null = null;
	let lobbyNameIsEmpty: boolean | null = null;

	/**
	 * This function resets the form inputs when the lobby-creation-panel is closed by the user.
	 */
	const resetForm = () => {
		numUsers = 1;
		gameDuration = 10;
		lobbyName = "";
	};

	/**
	 * This functions handles the submit when pressed.
	 * The submit won't work if the criteria of the lobbyname is not passed.
	 */
	function handleSubmit() {
		if (lobbyNameIsValid) {
			// Go to the game lobby.
			playerState.set(PlayerState.Host);
			goto("/play");
		} else if (lobbyName.length === 0) {
			lobbyNameIsEmpty = true;
		}
	}

	/**
	 * This is a reactive statement, which means it constantly checks if the input for lobbyname has changed.
	 * If it has changed it will check the requirements for the lobbyname.
	 */
	$: {
		if (lobbyName !== "") {
			const regex = /^[a-zA-Z]+$/;
			lobbyNameIsValid = regex.test(lobbyName);
			lobbyNameIsEmpty = false;
		} else {
			lobbyNameIsValid = null;
		}
	}
</script>

{#if showLobbyCreationPanel}
	<div class="panel mt-5">
		<div class="panel-content">
			<div class="top-row">
				<h2>Provide</h2>
				<button
					id="close-button"
					on:click={resetForm}
					on:click={() => (showLobbyCreationPanel = false)}
					on:click={() => dispatch("close")}>X</button
				>
			</div>
			<form class="form" on:submit|preventDefault={handleSubmit}>
				<label id="lobby-name">Name your vessel: </label>
				{#if lobbyNameIsValid === false}
					<p class="error-message">Name can only contain alphabetical characters</p>
				{/if}

				{#if lobbyNameIsEmpty === true}
					<p class="error-message">A vessel needs a name</p>
				{/if}

				<input
					type="text"
					aria-labelledby="lobby-name"
					bind:value={lobbyName}
					class:invalid={lobbyNameIsValid === false}
				/>

				<label for="users">Minimum number of spirits: {numUsers}</label>
				<input type="range" id="users" min="1" max="100" bind:value={numUsers} />

				<label for="duration">Voting Time: {gameDuration} seconds</label>
				<input type="range" id="duration" min="30" max="120" bind:value={gameDuration} />

				<div class="actions">
					<button type="submit" class="button">Create</button>
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
		@apply text-accent text-4xl bg-dark border-1 border-light-300 p-3 text-white;
		margin: 0 auto;
	}

	.actions {
		display: flex;
		justify-content: center;
		width: 100%;
	}
</style>
