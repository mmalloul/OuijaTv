<script lang="ts">
	import { goto } from "$app/navigation";
	import Board from "#lib/components/Board.svelte";
	import { getContext, onMount } from "svelte";
	import type { Writable } from "svelte/store";
	import { PlayerType } from "#lib/types/PlayerType";
	import { page } from "$app/stores";
	import HostControllerTest from "#lib/components/controllers/HostControllerTest.svelte";
	import PlayerControllerTest from "#lib/components/controllers/PlayerControllerTest.svelte";

	const playerType: Writable<PlayerType> = getContext("playerType");
	let board: Board;
	let word: string;
	let tick: number;
	let letterVoted: string;
	let canVote: boolean;

	$: pin = $page.params.pin;
	$: isHost = $playerType === PlayerType.Host;

	onMount(() => {
		if ($playerType === PlayerType.None) {
			goto(`/join/${pin}`);
		}
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

<div class="h-90vh flex flex-col items-center gap-5 pt-10">
	{#if $playerType === PlayerType.Host}
		<HostControllerTest
			bind:board
			bind:pin
			bind:word
			on:updateTick={setTick}
			on:updateWord={setWord}
		/>
	{:else if $playerType === PlayerType.Player}
		{console.log($playerType)}

		<PlayerControllerTest
			bind:board
			bind:pin
			bind:word
			bind:letterVoted
			bind:canVote
			on:updateTick={setTick}
			on:updateWord={setWord}
		/>
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

	<Board bind:this={board} bind:isHost bind:canVote on:letterClicked={onVoteLetter} />
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
