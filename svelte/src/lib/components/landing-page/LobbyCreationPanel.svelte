<script lang="ts">
	import { lobbyStore } from "$lib/stores/lobbyStore";
	import { PlayerType } from "$lib/types/PlayerType";
	import { goto } from "$app/navigation";
	import { createEventDispatcher, getContext } from "svelte";
	import type { Writable } from "svelte/store";
	import Dropdown from "$lib/components/Dropdown.svelte";
	import TourGuide from "$lib/components/TourGuide.svelte";
	import Icon from "@iconify/svelte";
	import type { LobbyData } from "$lib/types/LobbyData";
	const dispatch = createEventDispatcher();
	const playerType = getContext<Writable<PlayerType>>("playerType");
	export let showLobbyCreationPanel = false;
	let tourGuide: TourGuide;
	let gameDuration = 15; // in seconds
	let lobbyName = "";
	let twitchChannel = "";
	let isTwitchInputVisible = false;
	let lobbyNameIsValid: boolean;
	let lobbyNameIsEmpty: boolean;

	let gameModes: string[] = ["Solo", "Multiplayer"];
	let gameMode = gameModes[1]; // Set default gamemode to Multiplayer.
	$: gameModeIsValid = gameModes.includes(gameMode);
	$: isGameModeMultiplayer = gameMode === gameModes[1];

	$: twitchChannelIsValid = twitchChannel.length >= 4 && twitchChannel.length <= 25;

	$: lobbyNameIsEmpty = lobbyName == "";
	/**
	 * This is a reactive statement, which means it constantly checks if the input for lobbyname has changed.
	 * If it has changed it will check the requirements for the lobbyname.
	 */

	$: {
		if (!lobbyNameIsEmpty) {
			const regex = /^(?=.*\S)[a-zA-Z0-9 ]+$/;
			lobbyNameIsValid = regex.test(lobbyName);
		}
	}

	function startTheTour() {
		tourGuide.startTourLobbyCreationPanel();
	}

	/**
	 * This function resets the form inputs when the lobby-creation-panel is closed by the user.
	 */
	const resetForm = () => {
		gameDuration = 10;
		lobbyName = "";
		gameMode = gameModes[1]; // Set to multiplayer.
	};

	/**
	 * This functions checks if the twitch option is being used and if its valid.
	 */
	function checkTwitchChannel() {
		return isTwitchInputVisible && twitchChannelIsValid ? true : !isTwitchInputVisible;
	}

	/**
	 * This functions handles the submit when pressed.
	 * The submit won't work if the criteria of the lobbyname is not passed.
	 */
	function handleSubmit() {
		if (gameMode === "Solo") {
			goto("solo");
		} else {
			if (lobbyNameIsValid && gameMode) {
				playerType.set(PlayerType.Host);

				// Since our url has to stay simple (/play/[pin]) a lobbyStore has been added.
				// Without lobbyStore the url would /play?lobbyName=${lobbyName}&gameDuration=${gameDuration}`
		if (lobbyNameIsValid && gameMode && checkTwitchChannel()) {
			playerType.set(PlayerType.Host);

			const lobbyData: LobbyData = {
				lobbyName,
				gameMode,
				gameDuration
			};

			if (isTwitchInputVisible) {
				lobbyData.twitchChannel = twitchChannel;
			}

			lobbyStore.set(lobbyData);

			goto("/play");
		}
	}
</script>

{#if showLobbyCreationPanel}
	<div class="panel mt-5">
		<div class="panel-header">
			<button type="button" id="info-button" on:click={startTheTour}
				><p><Icon icon="ph:question-light" /></p></button
			>
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
				<div class="flex flex-col gap-2">
					<label for="lobby-name">Name your vessel: </label>
					{#if lobbyNameIsValid === false}
						<p class="error-message">Name can only contain alphabetical and numeric characters</p>
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
				</div>

				<div class="flex flex-col gap-2">
					{#if gameModeIsValid === false}
						<p class="error-message">Please select a gamemode</p>
					{/if}

					<label for="gameMode">Game Mode:</label>

					<div id="gameMode">
						<Dropdown bind:selection={gameMode} bind:options={gameModes} />
					</div>
				</div>

				{#if isGameModeMultiplayer}
					<div class="flex flex-col gap-2">
						<div class="flex justify-center">
							<label for="toggleInput">Twitch:</label>

							<input
								class="twitch-toggle"
								type="checkbox"
								id="toggleInput"
								bind:checked={isTwitchInputVisible}
							/>
						</div>

						{#if isTwitchInputVisible}
							<label for="lobby-name">Twitch Channel: </label>

							{#if twitchChannelIsValid === false}
								<p class="error-message">Twitch channel not valid:</p>
							{/if}

							<input
								type="text"
								id="channel-name"
								bind:value={twitchChannel}
								class:invalid={twitchChannelIsValid === false}
								placeholder="Enter Twitch Channel Name"
							/>
						{/if}
					</div>
				{/if}
				<div class="flex flex-col gap-2">
					<label for="duration">Voting Time: {gameDuration} seconds</label>
					<input type="range" id="duration" min="5" max="120" bind:value={gameDuration} />
				</div>

				<div class="actions">
					<button type="submit" class="big-button">Create</button>
				</div>
			</form>
		</div>
	</div>
	<TourGuide bind:this={tourGuide} />
{/if}

<style lang="postcss">
	.big-button {
		@apply w-50 text-4xl;
	}

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
		@apply pointer-events-auto flex flex-col justify-center w-32vh;
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

	.twitch-toggle {
		margin: 0;
		width: 50px;
	}

	label {
		@apply text-fontcolor text-4xl;
	}

	input {
		@apply text-accent text-4xl bg-dark border-1 border-light-300 p-3 text-white;
		margin: 0 auto;
	}

	input {
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

	#info-button {
		@apply text-fontcolor m-2 absolute;
		text-decoration: none;
		text-align: center;
		top: 0px;
		left: 0px;
		font-family: theme(fontFamily.amatic);
		transition: all 0.2s ease-in-out;
		font-size: calc(1em + 1vw); /* Responsive font-size */
	}

	#info-button:hover {
		@apply cursor-pointer bg-dark opacity-75;
		border-style: solid;
	}

	#info-button > p {
		transition: all 0.2s ease-in-out;
	}

	#info-button:hover {
		@apply cursor-pointer bg-dark opacity-75;
		border-style: solid;
	}

	#info-button:hover > p {
		@apply text-accent;
	}

	#info-button:hover > p {
		transform: scale(1.05);
	}
</style>
