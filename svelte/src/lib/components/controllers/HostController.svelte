<script lang="ts">
	import { onMount } from "svelte";
	import { env } from "$env/dynamic/public";
	import { page } from "$app/stores";
	import Icon from "@iconify/svelte";
	import type WebSocketController from "$lib/components/controllers/WebSocketController.svelte";
	import { toastStore } from "$lib/stores/toast";
	import { ToastType } from "$lib/types/ToastType";

	export let socketController: WebSocketController;
	export let pin: string;
	export let lobbyName: string;
	export let votingTime: number;
	export let gameMode: string;
	export let canPrompt = true;

	export let prompt: string;

	$: host = $page.url.origin;
	$: shareableURL = `${host}/join/${pin}`;

	onMount(() => {
		initSocketForHost();
	});

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

	function initSocketForHost() {
		const url = `${env.PUBLIC_WS_URL}/host?name=${lobbyName}&voting_time=${votingTime}&game_mode=${gameMode}`;
		socketController.initSocket(url);
	}

	function restart() {
		if (confirm("Do you want to restart the game?") === true) {
			prompt = "";
			socketController.sendRestart();
		}
	}

	function copyToClipBoard() {
		navigator.clipboard.writeText(shareableURL);
		$toastStore.showToast(ToastType.Success, "Lobby url has been copied!");
	}
</script>

<div class="flex flex-1 flex-grow item-center justify-center">
	<button on:click={restart} class="restart-button rounded-md">
		<Icon icon="mdi:restart" />
	</button>
</div>

<form class="flex flex-1 flex-grow item-center justify-center">
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

<div class="flex flex-1 flex-grow item-center justify-center gap-2 host-options">
	<div class="flex justify-end link-share rounded-lg">
		<span>
			{shareableURL}
		</span>

		<button on:click={copyToClipBoard} class="link-share-button ml-4 px-3 opacity-100">
			<Icon icon="mingcute:copy-line" color="white" width="22" />
		</button>
	</div>
</div>

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
		@apply mx-50 text-center;
		font-family: theme(fontFamily.amatic);
		font-size: 3rem;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
		margin: 0;
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

	.link-share-button:hover {
		@apply cursor-pointer bg-accent opacity-85;
	}

	.restart-button {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		transition: all 0.2s ease-in-out;
	}

	.restart-button:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}
</style>
