<script lang="ts">
	import { onMount, createEventDispatcher } from "svelte";
	import { env } from "$env/dynamic/public";
	import { page } from "$app/stores";
	import Icon from "@iconify/svelte";
	import type WebSocketController from "#lib/components/controllers/WebSocketController.svelte";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "#lib/types/ToastType";

	export let socketController: WebSocketController;
	export let pin: string;
	export let lobbyName: string;
	export let votingTime: number;
	export let gameMode: string;

	export let prompt: string;

	// $: socketController && socketController.sendPrompt({ type: "prompt", content: prompt });
	$: host = $page.url.origin;
	$: shareableURL = `${host}/join/${pin}`;

	onMount(() => {
		initSocketForHost();
	});

	function sendPrompt() {
		socketController.sendPrompt({ type: "prompt", content: prompt });
	}

	function initSocketForHost() {
		const url = `${env.PUBLIC_WS_URL}/host?name=${lobbyName}&voting_time=${votingTime}&game_mode=${gameMode}`;
		socketController.initSocket(url);
	}

	function restart() {
		if (confirm("Do you want to restart the game?") === true) {
			prompt = "";
			socketController.sendRestart();
			$toastStore.showToast(ToastType.Success, "Game has been restarted!");
		}
	}

	function copyToClipBoard() {
		navigator.clipboard.writeText(shareableURL);
		$toastStore.showToast(ToastType.Success, "Lobby url has been copied!");
	}
</script>

<form class="flex justify-center">
	<input bind:value={prompt} type="text" placeholder={"STATE YOUR INTENTION"} />
	<button on:click={sendPrompt} class="prompt-button rounded-md" disabled={!prompt}>
		<Icon icon="formkit:arrowright" />
	</button>
</form>

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
<button on:click={restart} class="restart-button p-2 rounded-md absolute left-5 bottom-0">
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
