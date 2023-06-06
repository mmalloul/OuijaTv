<script lang="ts">
	import { onMount } from "svelte";
	import { env } from "$env/dynamic/public";
	import type WebSocketController from "#lib/components/controllers/WebSocketController.svelte";

	export let socketController: WebSocketController;
	export let pin: string;
	export let prompt: string;
	let username: string;

	onMount(() => {
		initSocketForPlayer(pin);
		username = localStorage.getItem("username") || "";
	});

	function initSocketForPlayer(pin: string) {
		const url = `${env.PUBLIC_WS_URL}/join?pin=${pin}&username=${
			localStorage.getItem("username") ?? "anonymous"
		}`;
		socketController.initSocket(url);
	}
</script>

<form class="flex">
	{#if prompt}
		<span class="prompt">
			{prompt}
		</span>
	{:else}
		<span class="prompt">
			WAIT TO BE CALLED UPON...
		</span>
	{/if}
</form>

<div class="flex gap-2 player-options">
	<div class="flex justify-end player-info rounded-lg">
		<span>
			username: {username}
		</span>
	</div>
</div>

<style lang="postcss">
	.prompt {
		@apply w-full mx-50 w-200 outline-0 text-center;
		font-family: theme(fontFamily.amatic);
		font-size: 3rem;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
	}

	p,
	h1 {
		color: white;
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
