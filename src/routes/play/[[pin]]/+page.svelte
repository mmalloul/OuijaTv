<script lang="ts">
	import { goto } from "$app/navigation";
	import { env } from "$env/dynamic/public";
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import { getContext, onMount } from "svelte";
	import { page } from "$app/stores";
	import type { Writable } from "svelte/store";
	import { PlayerState } from "#lib/types/PlayerState";
	import toast, { Toaster } from "svelte-french-toast";
	import Icon from "@iconify/svelte";

	const playerState: Writable<PlayerState> = getContext("playerState");
	let username: string;
	let socket: WebSocket;
	let seekerX: number;
	let seekerY: number;

	onMount(() => {
		username = localStorage.getItem("username") ?? "anonymous";

		switch ($playerState) {
			case PlayerState.Host:
				socket = new WebSocket(`${env.PUBLIC_WS_URL}/host`);
				socket.onmessage = ({ data }) => {
					// pin
					goto(`play/${data}`);
					socket.onmessage = ({ data }) => {
						console.log(data);
					};
				};
				break;

			case PlayerState.Player:
				socket = new WebSocket(`${env.PUBLIC_WS_URL}/join?pin=${pin}&name=${username}`);
				break;

			case PlayerState.None:
				goto(`/join/${pin}`);
				break;

			default:
				break;
		}
	});

	function restart() {
		if (confirm("Do you want to restart the game?") === true) {
			socket.send(JSON.stringify({ action: "restart_game" }));
			toast.success("Game has been restarted!", {
				position: "bottom-center",
				style: "border-radius: 200px; background: #333; color: #fff; f"
			});
		}
	}

	function copyToClipBoard() {
		navigator.clipboard.writeText(shareableURL);
		toast.success("Lobby url has been copied!", {
			position: "bottom-center",
			style: "border-radius: 200px; background: #333; color: #fff; f"
		});
	}

	$: pin = $page.params.pin;
	$: host = $page.url.origin;
	$: shareableURL = `${host}/join/${pin}`;
</script>

<Toaster />

{#if $playerState === PlayerState.Host || $playerState === PlayerState.Player}
	<div class="h-90vh flex flex-col items-center gap-5 pt-10">
		{#if $playerState == PlayerState.Host}
			<form class="flex">
				<input type="text" placeholder="STATE YOUR INTENTION" />
			</form>
		{/if}

		<BoardSvg>
			{#if seekerX && seekerY}
				<circle id="Seeker" cx={seekerX} cy={seekerY} r="76.5" stroke="#FFF7E2" stroke-width="13" />
			{/if}
		</BoardSvg>
	</div>
	{#if $playerState == PlayerState.Host && pin}
		<div class="flex gap-2 host-options">
			<div class="flex justify-end link-share rounded-lg">
				<span>
					{shareableURL}
				</span>
				<button on:click={copyToClipBoard} class="link-share-button ml-4 px-3 opacity-100">
					<Icon icon="mingcute:copy-line" color="white" width="25"/>
				</button>
			</div>
			<button on:click={restart} class="restart-button bg-red-600 rounded-lg px-10">
				<p>Restart</p>
			</button>
		</div>
	{/if}
{/if}

<style lang="postcss">
	input {
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

	.absolute-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	.host-options {
		position: absolute;
		bottom: 0;
		right: 0;
	}

	.link-share {
		@apply opacity-50;
		border: 1px solid white;
		margin: 0 0 1rem 0;
		text-align: center;
		padding-left: 10px;
	}

	.link-share > span {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
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
		@apply cursor-pointer bg-accent opacity-75;
		transform: scale(1.03);
	}

	.restart-button > p {
		transition: all 0.2s ease-in-out;
	}

	.restart-button:hover > p {
		transform: scale(1.02);
	}

	.submit-button:hover {
		@apply cursor-pointer bg-indigo-500 opacity-75;
		transform: scale(1.01);
	}
</style>
