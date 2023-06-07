<script lang="ts">
	import { goto } from "$app/navigation";
	import Board from "$lib/components/Board.svelte";
	import { getContext, onMount, onDestroy } from "svelte";
	import type { Writable } from "svelte/store";
	import { PlayerType } from "$lib/types/PlayerType";
	import { page } from "$app/stores";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "$lib/types/ToastType";
	import Ghost from "$lib/components/Ghost.svelte";
	import { env } from "$env/dynamic/public";
	import HostController from "$lib/components/controllers/HostController.svelte";
	import PlayerController from "$lib/components/controllers/PlayerController.svelte";
	import Icon from "@iconify/svelte";

	const playerType: Writable<PlayerType> = getContext("playerType");
	const showMenu = getContext<Writable<boolean>>("showMenu");

	let board: Board;
	let word: string;
	let tick: number;
	let letterVoted: string;
	let canVote: boolean;
	let players: Record<string, string> = {};

	$: pin = $page.params.pin;
	$: isHost = $playerType === PlayerType.Host;

	onMount(() => {
		if ($playerType !== PlayerType.None && $page.params.pin != null) {
			fetchAllPlayers();
		}
		showMenu.set(false);
		if ($playerType === PlayerType.None) {
			goto(`/join/${pin}`);
		}
	});

	onDestroy(() => {
		showMenu.set(true);
	});

	function fetchAllPlayers() {
		fetch(`${env.PUBLIC_URL}/games/${$page.params.pin}`)
			.then((response) => response.json())
			.then((responseData) => {
				let playerData = responseData.players;
				playerData.forEach((player: { pid: string; name: string }) => {
					addPlayer(player.pid, player.name);
				});
				refreshPlayerDict();
			})
			.catch((error) => {
				console.error("Error:", error);
			});
	}

	function onPlayerJoin(event: any) {
		const pid = event.detail.pid;
		if (players[pid] == undefined) {
			const username = event.detail.username;
			const message = `${username} has joined the game 👻!`;
			addPlayer(pid, username);
			refreshPlayerDict();
			sendToast(message);
		}
	}

	function onPlayerQuit(event: any) {
		const pid = event.detail.pid;
		const message = `${players[pid]} has left the game 👋!`;

		delete players[pid];
		refreshPlayerDict();

		sendToast(message);
	}

	function addPlayer(pid: string, name: string) {
		players[pid] = name;
	}

	function refreshPlayerDict() {
		players = structuredClone(players);
	}

	function sendToast(message: string) {
		$toastStore.showToast(ToastType.Success, message);
	}

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
		<div class="back-to-menu">
			<a href="/"><Icon icon="formkit:arrowleft" />Exit</a>
		</div>
		{#if $playerType === PlayerType.Host}
			<HostController
				bind:board
				bind:pin
				bind:word
				on:updateTick={setTick}
				on:updateWord={setWord}
				on:joinedReceived={onPlayerJoin}
				on:playerQuit={onPlayerQuit}
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
				on:joinedReceived={onPlayerJoin}
				on:playerQuit={onPlayerQuit}
			/>
		{/if}

		<div class="voting-timer">
			{#if tick}
				<span class="timer">Voting ends in: {tick}</span>
			{:else}
				<span class="timer">Voting will start soon...</span>
			{/if}
		</div>
	</div>

	<div class="spirit-answer">
		{#if word}
			<span class="tracking-0.5em">
				{word}
			</span>
		{:else}
			<span> Waiting for answer... </span>
		{/if}
	</div>

	{#if players}
		{#each Object.values(players) as player}
			<Ghost>
				<p class="opacity-75">{player}</p>
			</Ghost>
		{/each}
	{/if}
	<Board bind:this={board} bind:isHost bind:canVote on:letterClicked={onVoteLetter} />
</div>

<style lang="postcss">
	.game {
		@apply flex flex-col items-center gap-4 relative h-full;
	}

	.game-header {
		@apply flex  md: flex-row justify-center items-center w-full flex-wrap;
		transition: all 0.5s ease-in-out;
	}

	.back-to-menu {
		@apply font-amatic text-center text-fontcolor flex flex-1 flex-grow;
	}

	.back-to-menu a {
		@apply flex justify-center items-center p-2 rounded-md  text-xl md: text-3xl;
		transition: all 0.2s ease-in-out;
		text-decoration: none;
	}

	.back-to-menu a:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}

	.timer {
		@apply text-fontcolor rounded-lg p-3 text-xl md: text-3xl;
		text-decoration: none;
		border: 1px solid white;
		font-family: theme(fontFamily.amatic);
		text-wrap: nowrap;
	}

	.voting-timer {
		@apply opacity-50 text-center flex flex-1 flex-grow items-center justify-center md: justify-end;
	}

	.spirit-answer {
		@apply text-accent flex items-center justify-center;
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}

	.spirit-answer span {
		@apply text-xl md:text-4xl;
		text-wrap: nowrap;
	}
</style>
