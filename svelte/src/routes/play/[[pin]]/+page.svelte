<script lang="ts">
	import { goto } from "$app/navigation";
	import Board from "$lib/components/Board.svelte";
	import WebSocketController from "$lib/components/controllers/WebSocketController.svelte";
	import { getContext, onMount, onDestroy } from "svelte";
	import type { Writable } from "svelte/store";
	import { PlayerType } from "$lib/types/PlayerType";
	import { page } from "$app/stores";
	import HostController from "$lib/components/controllers/HostController.svelte";
	import PlayerController from "$lib/components/controllers/PlayerController.svelte";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "$lib/types/ToastType";
	import { lobbyStore } from "$lib/stores/lobbyStore";

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
		canPrompt = true;
		board.resetSeeker();
		$toastStore.showToast(ToastType.Success, "Game has been restarted!");
	}

	function checkAnswer(event: any) {
		if (winningVote === "!") {
			prompt = "";
			canPrompt = true;
		} else {
			updateWord(event);
		}
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

	let showMenu = getContext<Writable<boolean>>("showMenu");

	onMount(() => {
		showMenu.set(false);
	});

	onDestroy(() => {
		showMenu.set(true);
	});
</script>

<div class="page--game game">
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

	<div class="game-header">
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

		<div class="voting-timer flex flex-1 flex-grow item-center justify-center">
			{#if tick}
				<span class="timer">Voting ends in: {tick}</span>
			{:else}
				<span class="timer">Voting will start soon...</span>
			{/if}
		</div>
	</div>

	<div class="word flex item-center justify-center">
		{#if word}
			<span class="text-6xl tracking-0.5em">
				{word}
			</span>
		{:else}
			<span class="text-6xl"> Waiting for answer... </span>
		{/if}
	</div>

	<Board bind:this={board} bind:isHost on:letterClicked={onVoteLetter} />
</div>

<style lang="postcss">
	.game {
		@apply flex flex-col items-center justify-center h-full gap-4;
	}

	.game-header {
		@apply flex flex-col md: flex-row justify-center items-center w-full flex-wrap;
		transition: all 0.5s ease-in-out;
	}

	.timer {
		@apply text-fontcolor text-4xl rounded-lg p-3;
		text-decoration: none;
		border: 1px solid white;
		font-family: theme(fontFamily.amatic);
		text-wrap: nowrap;
	}

	.voting-timer {
		@apply opacity-50;
		text-align: center;
	}

	.word {
		@apply text-accent text-4xl;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}
</style>
