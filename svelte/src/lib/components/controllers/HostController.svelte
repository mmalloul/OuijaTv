<script lang="ts">
	import { onMount, createEventDispatcher } from "svelte";
	import { env } from "$env/dynamic/public";
	import { page } from "$app/stores";
	import Icon from "@iconify/svelte";
	import WebSocketController from "$lib/components/controllers/WebSocketController.svelte";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "$lib/types/ToastType";
	import { goto } from "$app/navigation";
	import type Board from "$lib/components/Board.svelte";
	import { lobbyStore } from "$lib/stores/lobbyStore";
	import ExitButton from "$lib/components/ExitButton.svelte";
	import type { Writable } from "svelte/store";
	const dispatch = createEventDispatcher();

	export let pin: string;
	export let board: Board;
	export let word: string;
	export let showFinalWord: Writable<boolean>;

	let socketController: WebSocketController;
	let prompt: string;
	let canPrompt = true;
	let lobbyName: string;
	let votingTime: number;
	let gameMode: string;
	let twitchChannel: string | null;
	let hideSubmit = false;

	$: host = $page.url.origin;
	$: shareableURL = `${host}/join/${pin}`;
	$: lobbyStore.subscribe((value) => {
		// This retrieves the data filled in from LobbyCreationPanel
		lobbyName = value.lobbyName;
		gameMode = value.gameMode;
		votingTime = value.gameDuration;
		twitchChannel = value.twitchChannel;
	});

	onMount(() => {
		initSocketForHost();
	});

	/**
	 * Init socket for Host, send the lobbyName, VotingTime and GameMode.
	 */
	function initSocketForHost() {
		const twitchChannelParam =
			twitchChannel && twitchChannel.trim().length > 0 ? `&twitch_channel=${twitchChannel}` : "";
		const url = `${env.PUBLIC_WS_URL}/host?name=${lobbyName}&voting_time=${votingTime}&game_mode=${gameMode}${twitchChannelParam}`;
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

		if ($showFinalWord) {
			$toastStore.showToast(ToastType.Error, "You should restart the game first!");
		}

		if (canPrompt && prompt && prompt !== "") {
			socketController.sendPrompt({ type: "prompt", content: prompt });
			canPrompt = false;
			hideSubmit = true;
			$toastStore.showToast(ToastType.Success, "Question sent to spirits👻");
		}
	}

	function copyToClipBoard() {
		navigator.clipboard.writeText(shareableURL);
		$toastStore.showToast(ToastType.Success, "Lobby url has been copied!");
	}

	/**
	 * When Game has been created in backend and PIN has been sent, join the game.
	 * @param event event with the PIN.
	 */
	function joinGame(event: any) {
		pin = event.detail.pin;
		goto(`/play/${pin}`);
	}

	/**
	 * Function that sends restart to server when restart button is pressed.
	 */
	function onRestartButton() {
		if (confirm("Do you want to restart the game?")) {
			showFinalWord.set(false);
			socketController.sendRestart();
		}
	}

	/**
	 * When restart has been sent by backend the frontend ui gets reset for host.
	 */
	function restart() {
		canPrompt = true;
		prompt = "";
		hideSubmit = false;

		dispatch("updateWord", {
			word: ""
		});

		resetCountdown();

		board.resetSeeker();
		$toastStore.showToast(ToastType.Success, "Game has been restarted!");
	}

	function resetCountdown() {
		dispatch("tickReceived", {
			// Send event to parent for countdown timer.
			tick: undefined
		});
	}

	/**
	 * When server sends WORD update update the word if GOODBYE isn't voted as Majority.
	 * @param event the event with the word.
	 */
	function updateWord(event: any) {
		let newWord = event.detail.word;
		if (newWord === "!") {
			$toastStore.showToast(ToastType.Success, "Game ended, restart or stop the game!");
			showFinalWord.set(true);
		} else {
			dispatch("updateWord", {
				word: newWord
			});
		}
	}

	const exitGame = async (): Promise<void> => {
		if (confirm("Do you want to stop the game?")) {
			$toastStore.showToast(ToastType.Success, "You have stopped the game");
			socketController.closeSocket();
			goto("/");
		}
	};
</script>

<WebSocketController
	bind:this={socketController}
	on:joinedReceived
	on:playerQuit
	on:pinReceived={joinGame}
	on:restartReceived={restart}
	on:winningVoteReceived
	on:wordUpdateReceived={updateWord}
	on:tickReceived
	on:stopCountdownReceived={restart}
	on:noVotesReceived
/>

<ExitButton onExit={exitGame} />

<div class="restart-button">
	<button on:click={onRestartButton}>
		Restart <Icon icon="mdi:restart" />
	</button>
</div>

<form class="prompt-question">
	<input
		bind:value={prompt}
		id="prompt"
		type="text"
		placeholder={"STATE YOUR INTENTION"}
		disabled={!canPrompt}
	/>
	{#if !hideSubmit}
		<button on:click={sendPrompt} class="prompt-button">
			Submit <Icon icon="formkit:arrowright" />
		</button>
	{/if}
</form>

<div class="link-share">
	<div class="link-share-container">
		<span>
			{shareableURL}
		</span>

		<button on:click={copyToClipBoard} class="link-share-button">
			<Icon icon="mingcute:copy-line" color="white" width="22" />
		</button>
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

	.prompt-question {
		@apply flex flex-1 flex-grow items-center justify-center gap-2;
	}

	.prompt-button {
		@apply flex justify-center items-center text-fontcolor p-2 rounded-md text-lg lg: text-3xl;
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
		@apply px-4 py-2 text-center text-lg lg: text-4xl;
		font-family: theme(fontFamily.amatic);
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
		margin: 0;
	}

	.link-share {
		@apply absolute bottom-0 right-6 flex flex-1 flex-grow items-center justify-center gap-2;
	}

	.link-share-container {
		@apply opacity-50 flex justify-end rounded-lg;
		border: 1px solid white;
		margin: 0 0 1rem 0;
	}

	.link-share-container > span {
		@apply text-fontcolor font-amatic text-center p-1 text-lg lg:text-3xl p-2;
		text-decoration: none;
	}

	.link-share-button {
		@apply opacity-100 p-2;
		background-color: #3e3f3b;
		border-radius: 0 7px 7px 0;
	}

	.link-share-button:hover {
		@apply cursor-pointer bg-accent opacity-85;
	}

	.restart-button {
		@apply absolute bottom-0 left-6 flex flex-1 flex-grow items-center justify-center;
		margin: 0 0 1rem 0;
	}

	.restart-button button {
		@apply flex justify-center items-center text-fontcolor p-2 rounded-md text-lg lg:text-3xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		transition: all 0.2s ease-in-out;
	}

	.restart-button button:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}
</style>
