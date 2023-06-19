<script lang="ts">
	import { onMount, createEventDispatcher } from "svelte";
	import { env } from "$env/dynamic/public";
	import WebSocketController from "$lib/components/controllers/WebSocketController.svelte";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "$lib/types/ToastType";
	import type Board from "$lib/components/Board.svelte";
	import { goto } from "$app/navigation";
	import ExitButton from "../ExitButton.svelte";
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

		resetCountdown();

		$toastStore.showToast(ToastType.Success, "Game has been restarted!");
	}

	function resetCountdown() {
		dispatch("tickReceived", {
			// Send event to parent for countdown timer.
			tick: undefined
		});
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
		} else if (newWord !== "") {
			// The "A" is temporarily because no logic in backend when nothing voted. Now it just sends "A" from backend when nothing voted.
			word = newWord;
			canVote = true;
		}
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


	
	const exitGame = async (): Promise<void> => {
		$toastStore.showToast(ToastType.Success, "You have left the game");
		socketController.closeSocket();
		await goto("/");
	}

	async function exitReceived() {
		$toastStore.showToast(ToastType.Success, "Host has stopped the game");
		socketController.closeSocket();
		await goto("/");
	}
</script>

<WebSocketController
	bind:this={socketController}
	on:joinedReceived
	on:playerQuit
	on:promptReceived={promptUpdate}
	on:restartReceived={restart}
	on:winningVoteReceived
	on:wordUpdateReceived={updateWord}
	on:tickReceived
	on:stopCountdownReceived={restart}
	on:noVotesReceived
	on:exitReceived={exitReceived}
/>

<ExitButton onExit={exitGame} />

<div class="flex flex-1 flex-grow item-center justify-center">
	{#if prompt}
		<span class="prompt">
			{prompt}
		</span>
	{:else}
		<span class="prompt"> WAIT TO BE CALLED UPON... </span>
	{/if}
</div>

<div class="player-options">
	<div class="player-info">
		<span>
			username: {username}
		</span>
	</div>
</div>

<style lang="postcss">
	.back-to-menu {
		@apply font-amatic text-center text-fontcolor flex flex-1 flex-grow;
	}

	.back-to-menu a {
		@apply flex justify-center items-center px-2 rounded-md  text-lg lg: text-3xl;
		transition: all 0.2s ease-in-out;
		text-decoration: none;
	}

	.back-to-menu a:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}

	.prompt {
		@apply w-full text-center font-amatic text-lg lg: text-3xl;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
	}

	.player-options {
		@apply absolute gap-2 bottom-0 right-6;
	}

	.player-info {
		@apply opacity-50 text-center flex gap-2 flex justify-end rounded-lg;
		border: 1px solid white;
		margin: 0 0 1rem 0;
	}

	.player-info > span {
		@apply text-fontcolor text-lg py-1 px-2 lg:text-3xl py-2 px-6;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		font-size: 1.55rem;
	}
</style>
