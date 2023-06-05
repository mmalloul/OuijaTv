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

	let prompt: string;
	let board: Board;
	let votes: { [key: string]: number } = {};
	let socketController: WebSocketController;
	const playerType: Writable<PlayerType> = getContext("playerType");

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

	onMount(() => {
		console.log($playerType);
	});

	// Update the prompt from websocket so that the PlayerController component gets updated.
	function promptUpdate(event: any) {
		prompt = event.detail.prompt;
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
	function targetWinningVote(letter: any) {
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
		board.resetSeeker();
	}

	function updatePrompt(event: any) {
		prompt = event.detail.word;
		board.allowVoting();
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
		on:winningVoteReceived={targetWinningVote}
		on:wordUpdateReceived={updatePrompt}
		on:tickReceived={updateTick}
	/>

	{#if socketController}
		{#if $playerType === PlayerType.Host}
			<HostController bind:socketController bind:pin bind:lobbyName bind:votingTime bind:gameMode />
		{:else if $playerType === PlayerType.Player}
			<PlayerController bind:socketController bind:pin bind:prompt />
		{:else if $playerType === PlayerType.None}
			{gotoJoinPage()}
		{/if}
	{/if}

	{#if tick}
		{tick}
	{/if}

	<Board bind:this={board} bind:isHost on:letterClicked={onVoteLetter} />
</div>

<style lang="postcss">
</style>
