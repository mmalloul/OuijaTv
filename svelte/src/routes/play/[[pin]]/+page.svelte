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
	let votes: { [key: string]: number } = {};
	let socketController: WebSocketController;
	const playerType: Writable<PlayerType> = getContext("playerType");

	//TODO: should happen in host-only code
	let mostPopularLetter: string;

	$: pin = $page.params.pin;
	$: isHost = $playerType === PlayerType.Host;

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

	//TODO: should happen in host-only code
	function onVoteReceived(event: any) {
		const allVotes = event.detail.votes;
		votes = Object.assign({}, allVotes);
		updateMostPopularLetter();
	}

	//TODO: should happen in host-only code
	function updateMostPopularLetter() {
		const currentMostPopularLetter = getMostVotedLetter();
		if (currentMostPopularLetter !== mostPopularLetter) {
			mostPopularLetter = currentMostPopularLetter;
			socketController.broadcastWinningVote(mostPopularLetter);
		}
	}

	/**
	 * Moves the seeker (for host and player) to the targeted letter.
	 * @param letter the letter to move the seeker to.
	 */
	function targetWinningVote(letter: any) {
		board.moveSeekerToLetter(letter.detail.winningVote);
	}

	/**
	 * Function that retrieves the most voted letter from the dictionary with letters and votes.
	 */
	function getMostVotedLetter() {
		const target = Object.keys(votes).reduce((a, b) => (votes[a] > votes[b] ? a : b));
		return target;
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
</script>

<div class="h-90vh flex flex-col items-center gap-5 pt-10">
	<WebSocketController
		bind:this={socketController}
		on:joinedReceived={sendJoinedToast}
		on:voteReceived={onVoteReceived}
		on:pinReceived={joinGame}
		on:promptReceived={promptUpdate}
		on:restartReceived={restart}
		on:winningVoteReceived={targetWinningVote}
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
