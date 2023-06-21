<script lang="ts">
	import { goto } from "$app/navigation";
	import Board from "$lib/components/Board.svelte";
	import { getContext, onMount, onDestroy } from "svelte";

	import { writable, type Writable } from "svelte/store";
	import { PlayerType } from "$lib/types/PlayerType";
	import { page } from "$app/stores";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "$lib/types/ToastType";
	import Ghost from "$lib/components/Ghost.svelte";
	import { env } from "$env/dynamic/public";
	import HostController from "$lib/components/controllers/HostController.svelte";
	import PlayerController from "$lib/components/controllers/PlayerController.svelte";
	import Icon from "@iconify/svelte";
	import TourGuide from "$lib/components/TourGuide.svelte";

	const playerType: Writable<PlayerType> = getContext("playerType");
	const showMenu = getContext<Writable<boolean>>("showMenu");

	let board: Board;
	let word: string;
	let tick: number | undefined;
	let letterVoted: string;
	let canVote: boolean;
	let players: Record<string, string> = {};
	let tourGuide: TourGuide;
	let roundTime: number;
	let showFinalWord = writable(false);

	$: pin = $page.params.pin;
	$: isHost = $playerType === PlayerType.Host;

	onMount(() => {
		page.subscribe((p) => {
			if ($playerType !== PlayerType.None && p.params.pin != null) {
				fetchGameData();
			}
		});
		showMenu.set(false);
		if ($playerType === PlayerType.None) {
			goto(`/join/${pin}`);
		}
	});

	onDestroy(() => {
		showMenu.set(true);
	});

	function fetchGameData() {
		fetch(`${env.PUBLIC_URL}/games/${$page.params.pin}`)
			.then((response) => response.json())
			.then((responseData) => {
				roundTime = responseData.voting_time;
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

	function noVotesReceived() {
		$toastStore.showToast(ToastType.Error, `No votes received!`);
	}

	/**
	 * Moves the seeker to the targeted letter.
	 * @param letter the letter to move the seeker to.
	 */
	function updateWinningVote(letter: any) {
		board.moveSeekerTargetToLetter(letter.detail.winningVote);
	}

	function startTheTour() {
		if ($playerType === PlayerType.Host) tourGuide.startTourGameHost();
		if ($playerType === PlayerType.Player) tourGuide.startTourGamePlayer();
	}
</script>

<div class="page--game game">
	<div class="game-header">
		<div class="back-to-menu">
			<a id="exit-button" href="/"><Icon icon="formkit:arrowleft" />Exit</a>
		</div>
		{#if $playerType === PlayerType.Host}
			<HostController
				bind:board
				bind:pin
				bind:word
				bind:showFinalWord
				on:tickReceived={setTick}
				on:updateWord={setWord}
				on:joinedReceived={onPlayerJoin}
				on:playerQuit={onPlayerQuit}
				on:winningVoteReceived={updateWinningVote}
				on:noVotesReceived={noVotesReceived}
			/>
		{:else if $playerType === PlayerType.Player}
			<PlayerController
				bind:board
				bind:pin
				bind:word
				bind:letterVoted
				bind:canVote
				bind:showFinalWord
				on:tickReceived={setTick}
				on:updateWord={setWord}
				on:joinedReceived={onPlayerJoin}
				on:playerQuit={onPlayerQuit}
				on:winningVoteReceived={updateWinningVote}
				on:noVotesReceived={noVotesReceived}
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

	<div
		class="spirit-answer"
		class:animate__animated={$showFinalWord}
		class:tada-then-pulse={$showFinalWord}
	>
		{#if word}
			<span class="tracking-0.5em">
				{word}
			</span>
		{:else}
			<span> Waiting for answer... </span>
		{/if}
	</div>

	{#if players}
		<!-- limited to 20 players	 -->
		{#each Object.values(players).slice(0, 20) as player}
			<Ghost>
				<p class="opacity-75">{player}</p>
			</Ghost>
		{/each}
	{/if}

	<div id="board">
		<Board
			bind:timeLeft={tick}
			bind:this={board}
			bind:isHost
			bind:canVote
			{roundTime}
			on:letterClicked={onVoteLetter}
		/>
	</div>

	<button type="button" id="info-button" on:click={startTheTour}>
		<p>
			<Icon icon="ph:question-light" />
		</p>
	</button>
</div>

<TourGuide bind:this={tourGuide} />

<style lang="postcss">
	@import "animate.css";

	.tada-then-pulse {
		animation: tada 2s, pulse 5s 2s forwards;
	}

	.game {
		@apply flex flex-col items-center relative h-full lg: gap-2;
	}

	.game-header {
		@apply flex  md: flex-row justify-center items-center w-full flex-wrap;
		transition: all 0.5s ease-in-out;
	}

	.timer {
		@apply text-fontcolor rounded-lg text-lg px-2 lg: text-3xl;
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
		@apply text-lg lg: text-3xl;
		text-wrap: nowrap;
	}

	#info-button {
		@apply text-fontcolor m-2 absolute;
		text-decoration: none;
		text-align: center;
		bottom: 0;
		font-family: theme(fontFamily.amatic);
		transition: all 0.2s ease-in-out;
		font-size: calc(1em + 1vw); /* Responsive font-size */
	}

	#info-button:hover {
		@apply cursor-pointer;
		border-style: solid;
	}

	#info-button > p {
		transition: all 0.2s ease-in-out;
	}

	#info-button:hover {
		@apply cursor-pointer;
		border-style: solid;
	}

	#info-button:hover > p {
		@apply text-accent;
	}

	#info-button:hover > p {
		transform: scale(1.05);
	}
</style>
