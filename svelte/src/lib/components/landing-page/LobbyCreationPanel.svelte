<script lang="ts">
	import { lobbyStore } from "$lib/stores/lobbyStore";
	import { PlayerType } from "$lib/types/PlayerType";
	import { goto } from "$app/navigation";
	import { createEventDispatcher, getContext } from "svelte";
	import type { Writable } from "svelte/store";
	const dispatch = createEventDispatcher();
	const playerType = getContext<Writable<PlayerType>>("playerType");
	export let showLobbyCreationPanel = false;
	let numUsers = 1;
	let gameDuration = 15; // in seconds
	let lobbyName = "";
	let lobbyNameIsValid: boolean | null = null;
	let lobbyNameIsEmpty: boolean | null = null;
	let gameModes: string[] = ["Solo", "Multiplayer"];
	let gameMode = gameModes[1]; // Set default gamemode to Multiplayer.

	$: gameModeIsValid = gameMode !== null;

	/**
	 * This function resets the form inputs when the lobby-creation-panel is closed by the user.
	 */
	const resetForm = () => {
		numUsers = 1;
		gameDuration = 10;
		lobbyName = "";
		gameMode = gameModes[1]; // Set to multiplayer.
	};

	/**
	 * This functions handles the submit when pressed.
	 * The submit won't work if the criteria of the lobbyname is not passed.
	 */
	function handleSubmit() {

		if(gameMode === "Solo"){
			goto("solo")
			return;
		}

		if (lobbyNameIsValid && gameMode) {
			playerType.set(PlayerType.Host);

			// Since our url has to stay simple (/play/[pin]) a lobbyStore has been added.
			// Without lobbyStore the url would /play?lobbyName=${lobbyName}&gameDuration=${gameDuration}`
			lobbyStore.set({
				lobbyName,
				gameMode,
				gameDuration
			});

			// Go to the game lobby.
			goto("/play");
		} else if (lobbyName.length === 0) {
			lobbyNameIsEmpty = true;
		}
		if (!gameMode) {
			gameModeIsValid = false;
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
		<div class="panel-header">
			<h2>Provide</h2>

			<button
				id="close-button"
				on:click={resetForm}
				on:click={() => (showLobbyCreationPanel = false)}
				on:click={() => dispatch("close")}>X</button
			>
		</div>

		<div class="panel-content">
			<form class="form" on:submit|preventDefault={handleSubmit}>
				<label for="lobby-name">Name your vessel: </label>
				{#if lobbyNameIsValid === false}
					<p class="error-message">Name can only contain alphabetical characters</p>
				{/if}

				{#if lobbyNameIsEmpty === true}
					<p class="error-message">A vessel needs a name</p>
				{/if}

				<input
					type="text"
					id="lobby-name"
					bind:value={lobbyName}
					class:invalid={lobbyNameIsValid === false}
					placeholder="Enter lobby name"
				/>

				{#if gameModeIsValid === false}
					<p class="error-message">Please select a gamemode</p>
				{/if}
				<label for="gameMode">Game Mode:</label>
				<select id="gameMode" bind:value={gameMode}>
					{#each gameModes as mode (mode)}
						<option>{mode}</option>
					{/each}
				</select>

				<label for="duration">Voting Time: {gameDuration} seconds</label>
				<input type="range" id="duration" min="5" max="120" bind:value={gameDuration} />
				
				<div class="actions">
					<button type="submit" class="button">Create</button>
				</div>

			</form>
		</div>
	</div>
{/if}

<style lang="postcss">
	.panel {
		@apply flex flex-col justify-center items-center bg-dark text-fontcolor text-center p-4 md: p-6;
		width: 100%;
		border-radius: 6px;
		border: 1px solid white;
		row-gap: 20px;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
		max-width: 600px;
	}

	select {
		@apply bg-metal text-fontcolor;
		font-size: 1.5em;
		display: block;
		margin: 0 auto;
	}

	.panel-header {
		@apply flex justify-center w-full relative;
	}

	h2 {
		@apply text-6xl;
	}

	#close-button {
		@apply text-fontcolor text-5xl absolute;
		top: 0px;
		right: 0px;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}

	.panel-content {
		@apply pointer-events-auto flex flex-col justify-center;
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
		row-gap: 20px;
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
		border: 1px solid white;
	}

	.button:hover {
		@apply text-accent;
	}

	label {
		@apply text-fontcolor text-4xl;
	}

	input {
		@apply text-accent text-4xl bg-dark border-1 border-light-300 p-3 text-white;
		margin: 0 auto;
	}

	input,
	.button {
		box-sizing: border-box;
		width: 240px;
	}

	@screen <sm {
		input,
		.actions {
			width: 100%;
		}
	}

	.actions {
		display: flex;
		justify-content: center;
		width: 100%;
	}
</style>
