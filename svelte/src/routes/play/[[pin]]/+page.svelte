<script lang="ts">
	import { goto } from "$app/navigation";
	import Board from "$lib/components/Board.svelte";
	import { getContext, onMount, onDestroy } from "svelte";
	import type { Writable } from "svelte/store";
	import { PlayerType } from "$lib/types/PlayerType";
	import { page } from "$app/stores";
	import HostController from "$lib/components/controllers/HostController.svelte";
	import PlayerController from "$lib/components/controllers/PlayerController.svelte";

	const playerType: Writable<PlayerType> = getContext("playerType");
	const showMenu = getContext<Writable<boolean>>("showMenu");

	let board: Board;
	let word: string;
	let tick: number;
	let letterVoted: string;
	let canVote: boolean;

	$: pin = $page.params.pin;
	$: isHost = $playerType === PlayerType.Host;

	onMount(() => {
		showMenu.set(false);
		if ($playerType === PlayerType.None) {
			goto(`/join/${pin}`);
		}
	});

	onDestroy(() => {
		showMenu.set(true);
	});

	function onVoteLetter(event: any) {
		letterVoted = event.detail.id; // Bound to PlayerController so that it can send the vote.
	}

	function setWord(event: any) {
		word = event.detail.word; // Bound to Host- and PlayerController so that it can update the word.
	}

	function setTick(event: any) {
		tick = event.detail.tick; // Bound to Host- and PlayerController so that it can update the word.
	}
</script>

<div class="page--game game">
	<div class="game-header">
		{#if $playerType === PlayerType.Host}
			<HostController
				bind:board
				bind:pin
				bind:word
				on:updateTick={setTick}
				on:updateWord={setWord}
			/>
		{:else if $playerType === PlayerType.Player}
			<PlayerController
				bind:board
				bind:pin
				bind:word
				bind:letterVoted
				bind:canVote
				on:updateTick={setTick}
				on:updateWord={setWord}
			/>
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

	<Board bind:this={board} bind:isHost bind:canVote on:letterClicked={onVoteLetter} />
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
