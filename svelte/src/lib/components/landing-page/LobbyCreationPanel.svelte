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
	export let showLobbyCreationPanel = false;

	let tourGuide: TourGuide;
	let gameDuration = 15; // in seconds
	let lobbyName = "";
	let twitchChannel: string | null = null;
	let isTwitchInputVisible = false;
	let lobbyNameIsValid: boolean;
	let gameModeIsValid: boolean;
	let isGameModeMultiplayer: boolean;
	let twitchChannelIsValid: boolean;
	let formIsValid = true;
	let gameModes: string[] = ["Solo", "Multiplayer"];
	let soloGameMode: string = gameModes[0];
	let multiplayerGameMode: string = gameModes[1];
	let gameMode = multiplayerGameMode; // Set default gamemode to Multiplayer

	const dispatch = createEventDispatcher();
	const playerType = getContext<Writable<PlayerType>>("playerType");

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
	 * This reactive statement checks if the game mode is multiplayer.
	 */
	$: isGameModeMultiplayer = gameMode === multiplayerGameMode;

	/**
	 * This function checks if the game mode is valid.
	 */
	function validateGameMode() {
		gameModeIsValid = gameModes.includes(gameMode);
	}

	/**
	 * This function checks if the twitch channel is valid.
	 */
	function validateTwitchChannel() {
		twitchChannelIsValid =
			twitchChannel !== null && twitchChannel.length >= 4 && twitchChannel.length <= 25;
	}

	/**
	 * This function checks if the lobby name is valid.
	 */
	function validateLobbyName() {
		const alphaDigitsWhitespace = /^(?=.*\S)[a-zA-Z0-9 ]+$/;
		return (lobbyNameIsValid =
			alphaDigitsWhitespace.test(lobbyName) && lobbyName.length >= 4 && lobbyName.length <= 25);
	}

	/**
	 * This function checks if the twitch channel is valid.
	 */
	function checkTwitchChannel() {
		return isTwitchInputVisible && twitchChannelIsValid ? true : !isTwitchInputVisible;
	}

	/**
	 * This reactive statement validates the form inputs.
	 */
	$: {
		if (lobbyName && gameMode === soloGameMode) {
			validateLobbyName();
			validateGameMode();

			formIsValid = lobbyNameIsValid && gameModeIsValid;
		} else if (lobbyName && twitchChannel && gameMode === multiplayerGameMode) {
			validateLobbyName();
			validateGameMode();
			validateTwitchChannel();

			formIsValid = lobbyNameIsValid && gameModeIsValid && checkTwitchChannel();
		} else {
			validateLobbyName();
			validateGameMode();
			validateTwitchChannel();

			formIsValid = lobbyNameIsValid && gameModeIsValid && checkTwitchChannel();
		}
	}

	// Since our url has to stay simple (/play/[pin]) a lobbyStore has been added.
	// Without lobbyStore the url would /play?lobbyName=${lobbyName}&gameDuration=${gameDuration}`
	function handleSubmit() {
		if (formIsValid) {
			if (gameMode === soloGameMode) {
				goto("solo");
			}

			playerType.set(PlayerType.Host);

			const lobbyData: LobbyData = {
				lobbyName,
				gameMode,
				gameDuration,
				twitchChannel
			};

			lobbyStore.set(lobbyData);

			goto("/play");
		}
	}
</script>

{#if showLobbyCreationPanel}
	<div class="panel">
		<div class="panel-header">
			<button type="button" id="info-button" on:click={startTheTour}>
				<p>
					<Icon icon="charm:help" />
				</p>
			</button>

			<h2>Provide</h2>

			<button
				class="close-button"
				id="close-button"
				on:click={() => {
					resetForm();
					showLobbyCreationPanel = false;
					dispatch("close");
				}}
			>
				<p>
					<Icon icon="zondicons:close-outline" />
				</p>
			</button>
		</div>

		<div class="panel-content">
			<form class="create-form" on:submit|preventDefault={handleSubmit} novalidate>
				<div class="flex flex-col gap-2">
					<div class="flex flex-col">
						<label for="lobby-name">Name your vessel:</label>

						<span class:invisible={lobbyNameIsValid} class="error-message">
							Alphabetical and numeric characters only (between 4 and 25 characters)
						</span>
					</div>

					<input
						type="text"
						id="lobby-name"
						bind:value={lobbyName}
						placeholder="Enter lobby name"
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label for="duration">Voting Time: {gameDuration} seconds</label>

					<input
						class="!w-3/4"
						type="range"
						id="duration"
						min="5"
						max="120"
						bind:value={gameDuration}
					/>
				</div>

				<div class="flex flex-col gap-2">
					<label for="gameMode">Game Mode:</label>

					<div id="gameMode">
						<Dropdown bind:selection={gameMode} bind:options={gameModes} />
					</div>
				</div>

				<div class:invisible={!isGameModeMultiplayer} class="flex flex-col gap-2">
					<div class="flex justify-center gap-2">
						<label for="toggleInput">Twitch integration:</label>

						<input
							class="twitch-toggle"
							type="checkbox"
							id="toggleInput"
							bind:checked={isTwitchInputVisible}
							disabled={!isGameModeMultiplayer}
						/>
					</div>

					<div class:opacity-30={!isTwitchInputVisible}>
						<div class="flex flex-col">
							<label for="channel-name">Channel Name:</label>

							<span
								class:invisible={twitchChannelIsValid || !isTwitchInputVisible}
								class="error-message"
							>
								Twitch channel not valid (between 4 and 25 characters)
							</span>
						</div>

						<input
							type="text"
							id="channel-name"
							bind:value={twitchChannel}
							placeholder="Enter Twitch Channel Name"
							disabled={!isTwitchInputVisible}
						/>
					</div>
				</div>

				<div class="actions">
					<button type="submit" class="big-button" disabled={!formIsValid}>Create</button>
				</div>
			</form>
		</div>
	</div>

	<TourGuide bind:this={tourGuide} />
{/if}

<style lang="postcss">
	.panel {
		@apply flex flex-col font-amatic items-center text-fontcolor text-center h-full w-full mt-15 md: justify-center;
		max-width: 600px; // max-width of the lobbycreation panel
	}

	.panel-header {
		@apply flex justify-center items-center w-full relative;
	}

	.panel-content {
		@apply pointer-events-auto flex flex-col justify-center w-full;
	}

	.create-form {
		@apply flex flex-col pointer-events-auto text-fontcolor text-center w-full gap-2 md: gap-6 md:p-4;
	}

	h2 {
		@apply text-lg md: text-5xl;
	}

	.close-button {
		@apply absolute top-0 right-0 m-2 text-fontcolor text-lg md: text-3xl;
		text-decoration: none;
		text-align: center;
		transition: all 0.2s ease-in-out;
	}

	.close-button:hover {
		@apply text-accent;
	}

	.close-button:hover > p {
		@apply text-accent;
	}

	.close-button:hover > p {
		transform: scale(1.05);
	}

	.big-button {
		@apply text-lg md: text-4xl;
	}

	.error-message {
		@apply !text-red-500 text-lg md:text-2xl;
	}

	.twitch-toggle {
		margin: 0;
		width: 50px;
	}

	label {
		@apply text-fontcolor text-lg md: text-4xl;
	}

	input {
		@apply text-accent border-light-300 p-3 text-white w-full text-lg md: text-4xl;
		margin: 0 auto;
	}

	.actions {
		@apply flex items-center justify-center w-full;
	}

	#info-button {
		@apply absolute top-0 left-0 m-2 text-fontcolor text-lg md: text-3xl;
		text-decoration: none;
		text-align: center;
		transition: all 0.2s ease-in-out;
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
