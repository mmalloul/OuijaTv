<script lang="ts">
	import { onMount, createEventDispatcher } from "svelte";
	import { env } from "$env/dynamic/public";
	import WebSocketController from "$lib/components/controllers/WebSocketController.svelte";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "$lib/types/ToastType";
	import type Board from "$lib/components/Board.svelte";
	const dispatch = createEventDispatcher();

	export let pin: string;
	export let board: Board;
	export let word: string;
	export let letterVoted: string;
	export let canVote = false;

	let socketController: WebSocketController;
	let username: string;
	let prompt: string;

	// This reactive statement checks whether a letter has been voted on the board by the player.
	$: {
		if (letterVoted) {
			onVoteLetter(letterVoted);
		}
	}

	onMount(() => {
		initSocketForPlayer(pin);
		username = localStorage.getItem("username") || "";
	});

	/**
	 * Initialize the WebSocket for the player and send pin and username.
	 * @param pin
	 */
	function initSocketForPlayer(pin: string) {
		const url = `${env.PUBLIC_WS_URL}/join?pin=${pin}&username=${
			localStorage.getItem("username") ?? "anonymous"
		}`;
		socketController.initSocket(url);
	}

	// Update the prompt from websocket so that the PlayerController component gets updated.
	function promptUpdate(event: any) {
		prompt = event.detail.prompt;
		if (prompt !== "") {
			$toastStore.showToast(ToastType.Success, "Voting has started!");
			canVote = true;
		}
	}

	/**
	 * Function that resets the board seeker, prompt word and canVote for player.
	 * This function is triggered by restart message from server
	 */
	function restart() {
		board.resetSeeker();
		prompt = "";
		canVote = false;

		// Send event to parent to reset word.
		dispatch("updateWord", {
			word: ""
		});

		$toastStore.showToast(ToastType.Success, "Game has been restarted!");
	}

	/**
	 * Moves the seeker to the targeted letter.
	 * @param letter the letter to move the seeker to.
	 */
	function updateWinningVote(letter: any) {
		board.moveSeekerToLetter(letter.detail.winningVote);
	}

	/**
	 * Every voting round that ends triggers this function.
	 * Updates the word if majority did NOT vote on Goodbye.
	 * If majority did vote on goodbye reset prompt.
	 * @param event the word that's sent after a voting round ended.
	 */
	function updateWord(event: any) {
		let newWord = event.detail.word;

		if (newWord === "!") {
			prompt = "";
		} else if (newWord !== "" && newWord !== "A") {
			// The "A" is temporarily because no logic in backend when nothing voted. Now it just sends "A" from backend when nothing voted.
			word = newWord;
			canVote = true;
		}
	}

	function updateTick(event: any) {
		dispatch("updateTick", {
			// Send event to parent for countdown timer.
			tick: event.detail.tick
		});
	}

	/**
	 * If player clicked on a letter and is allowed to vote send vote to server.
	 * Set voting to false after because only 1 vote per voting round is allowed.
	 * @param letterId
	 */
	function onVoteLetter(letterId: string) {
		if (canVote) {
			socketController.sendVote({ type: "vote", content: letterId });
			canVote = false;
		}
	}
</script>

<WebSocketController
	bind:this={socketController}
	on:joinedReceived
	on:playerQuit
	on:promptReceived={promptUpdate}
	on:restartReceived={restart}
	on:winningVoteReceived={updateWinningVote}
	on:wordUpdateReceived={updateWord}
	on:tickReceived={updateTick}
/>

<div class="flex flex-1 flex-grow item-center justify-center">
	{#if prompt}
		<span class="prompt">
			{prompt}
		</span>
	{:else}
		<span class="prompt"> WAIT TO BE CALLED UPON... </span>
	{/if}
</div>

<div class="flex gap-2 player-options">
	<div class="flex justify-end player-info rounded-lg">
		<span>
			username: {username}
		</span>
	</div>
</div>

<style lang="postcss">
	.prompt {
		@apply w-full text-center;
		font-family: theme(fontFamily.amatic);
		font-size: 3rem;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
	}

	.player-options {
		position: absolute;
		bottom: 0;
		right: 1.5rem;
	}

	.player-info {
		@apply opacity-50;
		border: 1px solid white;
		margin: 0 0 1rem 0;
		text-align: center;
		padding-left: 10px;
	}

	.player-info > span {
		@apply text-fontcolor text-4xl py-2 px-6;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		font-size: 1.55rem;
	}
</style>
