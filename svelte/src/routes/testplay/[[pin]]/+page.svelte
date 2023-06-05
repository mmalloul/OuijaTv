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
	let votes: object = {};
	let socketController: WebSocketController;
	const playerType: Writable<PlayerType> = getContext("playerType");

	$: pin = $page.params.pin;

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
			board.targetLetter(letterId);
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
		board.targetLetter(board.getTargetLetter(votes));
	}

	function joinGame(event: any) {
		pin = event.detail.pin;
		goto(`/testplay/${pin}`);
	}

	function gotoJoinPage() {
		goto(`/join/${pin}`);
	}

	function restart() {
		//TODO
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
	/>

	{#if socketController}
		{#if $playerType === PlayerType.Host}
			<HostController bind:socketController bind:pin />
		{:else if $playerType === PlayerType.Player}
			<PlayerController bind:socketController bind:pin bind:prompt />
		{:else if $playerType === PlayerType.None}
			{gotoJoinPage()}
		{/if}
	{/if}

	<!-- The temporary panel with amount of votes for each letter. -->
	<div class="absolute left-0 top-30 text-white grid grid-cols-4 opacity-50">
		{#each Object.entries(votes) as [letter, count]}
			<span>{letter}: {count}</span>
		{/each}
	</div>

	<Board bind:this={board} on:letterClicked={onVoteLetter} />
</div>

<style lang="postcss">
</style>
