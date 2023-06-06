<script lang="ts">
	import { goto } from "$app/navigation";
	import Board from "#lib/components/Board.svelte";
	import WebSocketController from "#lib/components/controllers/WebSocketController.svelte";
	import { getContext, onMount } from "svelte";
	import type { Writable } from "svelte/store";
	import { PlayerType } from "#lib/types/PlayerType";
	import { page } from "$app/stores";
	import HostController from "#lib/components/controllers/HostController.svelte";
	import PlayerController from "#lib/components/controllers/PlayerController.svelte";
	import { toastStore } from "#lib/stores/toast";
	import { ToastType } from "#lib/types/ToastType";
	import { lobbyStore } from "#lib/stores/lobbyStore";
	import { env } from "$env/dynamic/public";

	let prompt: string;
	let word: string;
	let board: Board;
	let socketController: WebSocketController;
	let winningVote: string;
	const playerType: Writable<PlayerType> = getContext("playerType");
	let canPrompt: boolean;

	let tick: number;
	let lobbyName: string;
	let votingTime: number;
	let gameMode: string;

	$: pin = $page.params.pin;
	$: isHost = $playerType === PlayerType.Host;
	$: lobbyStore.subscribe((value) => {
		lobbyName = value.lobbyName;
		gameMode = value.gameMode;
		votingTime = value.gameDuration;
	});

	// Update the prompt from websocket so that the PlayerController component gets updated.
	function promptUpdate(event: any) {
		prompt = event.detail.prompt;
		if ($playerType === PlayerType.Player) {
			if (prompt !== "") {
				$toastStore.showToast(ToastType.Success, "Voting has started!");
			}
			board.allowVoting();
		}
	}

	/**
	 * Function that sends vote to the websocket with the target id.
	 * @param event The event that contains the voted letter from the player.
	 */
	function onVoteLetter(event: any) {
		if ($playerType === PlayerType.Player) {
			const letterId = event.detail.id;
			socketController.sendVote({ type: "vote", content: letterId });
		}
	}

	/**
	 * Send toast to notify host that a player joined.
	 * @param event the event with the username that has joined.
	 */
	function sendJoinedToast(event: any) {
		const username = event.detail.username;
		const message = `${username} has joined the game 👻!`;
		$toastStore.showToast(ToastType.Success, message);
	}

	/**
	 * Moves the seeker (for host and player) to the targeted letter.
	 * @param letter the letter to move the seeker to.
	 */
	function updateWinningVote(letter: any) {
		winningVote = letter.detail.winningVote;
		console.log(winningVote);

		board.moveSeekerToLetter(letter.detail.winningVote);
	}

	function joinGame(event: any) {
		pin = event.detail.pin;
		goto(`/play/${pin}`);
	}

	function gotoJoinPage() {
		goto(`/join/${pin}`);
	}

	function restart() {
		prompt = "";
		word = "";
		board.resetSeeker();
		$toastStore.showToast(ToastType.Success, "Game has been restarted!");
	}

	function checkAnswer(event: any) {
		if (winningVote === "!") {
			prompt = "";
		} else {
			updateWord(event);
		}
		canPrompt = true;
	}

	function updateWord(event: any) {
		word = event.detail.word;
		if ($playerType === PlayerType.Player) {
			board.allowVoting();
		}
	}

	function updateTick(event: any) {
		tick = event.detail.tick;
	}
</script>

<div class="h-90vh flex flex-col items-center gap-5 pt-10">
	<WebSocketController
		bind:this={socketController}
		on:joinedReceived={sendJoinedToast}
		on:pinReceived={joinGame}
		on:promptReceived={promptUpdate}
		on:restartReceived={restart}
		on:winningVoteReceived={updateWinningVote}
		on:wordUpdateReceived={checkAnswer}
		on:tickReceived={updateTick}
	/>

	{#if socketController}
		{#if $playerType === PlayerType.Host}
			<HostController
				bind:socketController
				bind:pin
				bind:lobbyName
				bind:votingTime
				bind:gameMode
				bind:prompt
				bind:canPrompt
			/>
		{:else if $playerType === PlayerType.Player}
			<PlayerController bind:socketController bind:pin bind:prompt />
		{:else if $playerType === PlayerType.None}
			{gotoJoinPage()}
		{/if}
	{/if}

	{#if word}
		<span class="word">
			{word}
		</span>
	{/if}

	<div class="flex gap-2 justify-end voting-timer rounded-lg">
		{#if tick}
			<span class="timer">Voting ends in: {tick}</span>
		{:else}
			<span class="timer">Voting will start soon...</span>
		{/if}
	</div>

	<Board bind:this={board} bind:isHost on:letterClicked={onVoteLetter} />
</div>

<style lang="postcss">
	.timer {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}

	.final-word {
		@apply text-accent text-10xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}

	.voting-timer {
		@apply opacity-50;
		border: 1px solid white;
		margin: 0 1rem 1rem 0;
		text-align: center;
		padding: 0 10px;
		position: absolute;
		right: 1.5rem;
	}

	.word {
		@apply text-accent text-4xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}
</style>
