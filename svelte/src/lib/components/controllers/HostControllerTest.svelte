<script lang="ts">
	import { onMount } from "svelte";
	import { env } from "$env/dynamic/public";
	import { page } from "$app/stores";
	import Icon from "@iconify/svelte";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "#lib/types/ToastType";
	import WebSocketController from "#lib/components/controllers/WebSocketController.svelte";
	import { goto } from "$app/navigation";
	import type Board from "../Board.svelte";
	import { createEventDispatcher } from "svelte";
	import { lobbyStore } from "#lib/stores/lobbyStore";
	const dispatch = createEventDispatcher();

	export let pin: string;
	export let board: Board;
	export let word: string;

	let socketController: WebSocketController;
	let prompt: string;
	let canPrompt = true;
	let lobbyName: string;
	let votingTime: number;
	let gameMode: string;

	$: host = $page.url.origin;
	$: shareableURL = `${host}/join/${pin}`;
	$: lobbyStore.subscribe((value) => { // This retrieves the data filled in from LobbyCreationPanel
		lobbyName = value.lobbyName;
		gameMode = value.gameMode;
		votingTime = value.gameDuration;
	});

	onMount(() => {
		initSocketForHost();
	});

	/**
	 * Init socket for Host, send the lobbyName, VotingTime and GameMode.
	*/
	function initSocketForHost() {
		const url = `${env.PUBLIC_WS_URL}/host?name=${lobbyName}&voting_time=${votingTime}&game_mode=${gameMode}`;
		socketController.initSocket(url);
	}

	/**
	 * Host sends prompt whether the prompt is not empty and if allowed to prompt.
	 * Host can't prompt when round has started.
	 */
	function sendPrompt() {
		if (prompt == "" || !prompt) {
			$toastStore.showToast(ToastType.Error, "You should enter a question!");
		}

		if (canPrompt && prompt && prompt !== "") {
			socketController.sendPrompt({ type: "prompt", content: prompt });
			canPrompt = false;
			$toastStore.showToast(ToastType.Success, "Question sent to spirits👻");
		}
	}

	function copyToClipBoard() {
		navigator.clipboard.writeText(shareableURL);
		$toastStore.showToast(ToastType.Success, "Lobby url has been copied!");
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
	 * When Game has been created in backend and PIN has been sent, join the game.
	 * @param event event with the PIN.
	 */
	function joinGame(event: any) {
		pin = event.detail.pin;
		goto(`/testplay/${pin}`);
	}

	/**
	 * Function that sends restart to server when restart button is pressed.
	 */
	function onRestartButton() {
		if (confirm("Do you want to restart the game?") === true) {
			socketController.sendRestart();
		}
	}

	/**
	 * When restart has been sent by backend the frontend ui gets reset for host.
	*/
	function restart() {
		canPrompt = true;
		prompt = "";

		dispatch("updateWord", {
			word: ""
		});

		board.resetSeeker();
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
	 * When server sends WORD update update the word if GOODBYE isn't voted as Majority.
	 * @param event the event with the word.
	 */
	function updateWord(event: any) {
		let newWord = event.detail.word;
		if (newWord === "!") {
			prompt = "";
			canPrompt = true;
		} else {
			dispatch("updateWord", {
				word: newWord
			});
		}
	}

	function updateTick(event: any) {
		dispatch("updateTick", {
			tick: event.detail.tick
		});
	}
</script>

<WebSocketController
	bind:this={socketController}
	on:joinedReceived={sendJoinedToast}
	on:pinReceived={joinGame}
	on:restartReceived={restart}
	on:winningVoteReceived={updateWinningVote}
	on:wordUpdateReceived={updateWord}
	on:tickReceived={updateTick}
/>

<form class="flex justify-center">
	<input
		bind:value={prompt}
		type="text"
		placeholder={"STATE YOUR INTENTION"}
		disabled={!canPrompt}
	/>
	<button on:click={sendPrompt} class="prompt-button rounded-md">
		<Icon icon="formkit:arrowright" />
	</button>
</form>

{#if word}
	<span class="word">
		{word}
	</span>
{/if}

<div class="flex gap-2 host-options">
	<div class="flex justify-end link-share rounded-lg">
		<span>
			{shareableURL}
		</span>
		<button on:click={copyToClipBoard} class="link-share-button ml-4 px-3 opacity-100">
			<Icon icon="mingcute:copy-line" color="white" width="22" />
		</button>
	</div>
</div>
<button on:click={onRestartButton} class="restart-button p-2 rounded-md absolute left-5 bottom-0">
	<Icon icon="mdi:restart" />
</button>

<style lang="postcss">
	.prompt-button {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		transition: all 0.2s ease-in-out;
	}

	.prompt-button:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}

	input {
		@apply w-full mx-50 w-150 outline-0 text-center;
		font-family: theme(fontFamily.amatic);
		font-size: 3rem;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
		margin: 0;
	}

	p,
	h1 {
		color: white;
	}

	.absolute-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	.host-options {
		position: absolute;
		bottom: 0;
		right: 1.5rem;
	}

	.link-share {
		@apply opacity-50;
		border: 1px solid white;
		margin: 0 0 1rem 0;
		text-align: center;
		padding-left: 10px;
	}

	.link-share > span {
		@apply text-fontcolor text-4xl py-2 px-6;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		font-size: 1.55rem;
	}

	.link-share-button {
		background-color: #3e3f3b;
		border-radius: 0 7px 7px 0;
	}

	.link-share-button > img {
		color: white;
	}

	.link-share-button:hover {
		@apply cursor-pointer bg-accent opacity-85;
	}

	.submit-button,
	.restart-button {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		transition: all 0.2s ease-in-out;
	}

	.restart-button {
		margin: 0 1rem 1rem 0;
	}

	.restart-button:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}

	.restart-button > p {
		transition: all 0.2s ease-in-out;
	}

	.restart-button:hover > p {
		transform: scale(1.02);
	}
</style>
