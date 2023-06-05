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

	let prompt: string;
	let board: Board;
	let votes: { [key: string]: number }= {};
	let socketController: WebSocketController;
	let mostPopularLetter: string;
	const playerType: Writable<PlayerType> = getContext("playerType");

	$: pin = $page.params.pin;
	$: isHost = $playerType === PlayerType.Host;

	onMount(() => {
		console.log($playerType);
	});

	// Update the prompt from websocket so that the PlayerController component gets updated.
	function promptUpdate(event: any) {
		prompt = event.detail.prompt;
	}

	function onVoteLetter(event: any) {
		if ($playerType === PlayerType.Player) {
			const letterId = event.detail.id;
			socketController.sendVote({ type: "vote", content: letterId });
		}
	}

	function sendJoinedToast(event: any) {
		const username = event.detail.username;
		const message = `${username} has joined the game 👻!`;
		$toastStore.showToast(ToastType.Success, message);
	}

	function onVoteReceived(event: any) {
		const allVotes = event.detail.votes;
		votes = Object.assign({}, allVotes);
		updateMostPopularLetter()
	}

	function updateMostPopularLetter()
	{
		const currentMostPopularLetter = getMostPopularLetter()
		if (currentMostPopularLetter !== mostPopularLetter)
		{
			mostPopularLetter = currentMostPopularLetter;
			socketController.broadcastMostPopularLetterChange(mostPopularLetter)
		}
	}

	function targetMostPopularLetter(letter: any) {
		board.moveSeekerToLetter(letter.detail.mostPopularLetter);  
	}

	function getMostPopularLetter() {
		const target = Object.keys(votes).reduce((a, b) => (votes[a] > votes[b] ? a : b));
		return target;
	}

	function joinGame(event: any) {
		pin = event.detail.pin;
		goto(`/testplay/${pin}`);
	}

	function gotoJoinPage() {
		goto(`/join/${pin}`);
	}

	function restart() {
		board.resetSeeker();
	}
</script>

<div class="h-90vh flex flex-col items-center gap-5 pt-10">
	<WebSocketController
		bind:this={socketController}
		on:joinedReceived={sendJoinedToast}
		on:voteReceived={onVoteReceived}
		on:pinReceived={joinGame}
		on:promptReceived={promptUpdate}
		on:restartReceived={restart}
		on:newMostPopularLetterReceived={targetMostPopularLetter}
	/>

	{#if socketController}
		{#if $playerType === PlayerType.Host}
			<HostController bind:socketController bind:pin bind:votes />
		{:else if $playerType === PlayerType.Player}
			<PlayerController bind:socketController bind:pin bind:prompt />
		{:else if $playerType === PlayerType.None}
			{gotoJoinPage()}
		{/if}
	{/if}

	<Board bind:this={board} bind:isHost on:letterClicked={onVoteLetter} />
</div>

<style lang="postcss">
</style>
