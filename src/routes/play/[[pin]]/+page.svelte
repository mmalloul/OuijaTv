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
	import items from "#lib/types/MenuItems";

	class Vector2 {
		constructor(public x: number, public y: number) {}
	}

	const playerState: Writable<PlayerState> = getContext("playerState");
	const letterPositions: Record<string, Vector2> = {};

	let prompt: string = "";
	let username: string;
	let socket: WebSocket;
	let seekerX: number;
	let seekerY: number;
	let votes: object = {};

	onMount(() => {
		username = localStorage.getItem("username") ?? "anonymous";

		switch ($playerState) {
			case PlayerState.Host:
				socket = new WebSocket(`${env.PUBLIC_WS_URL}/host`);
				socket.onmessage = ({ data }) => {
					const parsed = JSON.parse(data);

					switch (parsed["type"]) {
						case "pin":
							goto(`play/${parsed["content"]}`);
							break;
						case "connect":
							const message = `${parsed["username"]} has joined the game 👻!`;
							toast.success(message, {
								position: "bottom-center",
								style: "border-radius: 200px; background: #333; color: #fff; f"
							});
						case "votes":
							votes = Object.assign({}, parsed["content"]);
							targetALetter(getTargetLetter());
							break;
						default:
							break;
					}
				};
				break;

			case PlayerState.Player:
				socket = new WebSocket(`${env.PUBLIC_WS_URL}/join?pin=${pin}&name=${username}`);

				socket.onmessage = ({ data }) => {
					const parsed = JSON.parse(data);

					switch (parsed["type"]) {
						case "prompt":
							prompt = parsed["content"];
							break;
						default:
							break;
					}
				};

				break;

			case PlayerState.None:
				goto(`/join/${pin}`);
				break;

			default:
				break;
		}

		loadLetterPositions();
	});

	function vote(on: string) {
		if ($playerState === PlayerState.Player) {
			socket.send(JSON.stringify({ type: "vote", content: on }));
		}
	}

	function getTargetLetter() {
		const target = Object.keys(votes).reduce((a, b) => (votes[a] > votes[b] ? a : b));
		return target;
	}

	function loadLetterPositions() {
		const circleElements = document.querySelectorAll<SVGCircleElement>("circle");
		circleElements.forEach((element) => {
			const id = element.id;

			let x = element.attributes.getNamedItem("cx")?.value;
			let y = element.attributes.getNamedItem("cy")?.value;
			if (x && y) {
				letterPositions[id.charAt(id.length - 1)] = new Vector2(parseFloat(x), parseFloat(y));
			}
		});
	}

	function restart() {
		if (confirm("Do you want to restart the game?") === true) {
			prompt = "";
			socket.send(JSON.stringify({ type: "restart" }));
			toast.success("Game has been restarted!", {
				position: "bottom-center",
				style: "border-radius: 200px; background: #333; color: #fff; f"
			});
		}
	}

	function targetALetter(letter: string) {
		let target = letterPositions[letter.toUpperCase()];

		if (target) {
			seekerX = target.x;
			seekerY = target.y;
		}
	}

	function copyToClipBoard() {
		navigator.clipboard.writeText(shareableURL);
		toast.success("Lobby url has been copied!", {
			position: "bottom-center",
			style: "border-radius: 200px; background: #333; color: #fff; f"
		});
	}

	$: socket &&
		socket.readyState == socket.OPEN &&
		socket.send(JSON.stringify({ type: "prompt", content: prompt }));

	$: pin = $page.params.pin;
	$: host = $page.url.origin;
	$: shareableURL = `${host}/join/${pin}`;
</script>

<Toaster />

<div class="absolute left-0 top-30 text-white grid grid-cols-4 opacity-50">
	{#each Object.entries(votes) as [letter, count]}
		<span>{letter}: {count}</span>
	{/each}
</div>

{#if $playerState === PlayerState.Host || $playerState === PlayerState.Player}
	{@const isHost = $playerState == PlayerState.Host}
	<div class="h-90vh flex flex-col items-center gap-5 pt-10">
		<form class="flex">
			<input
				bind:value={prompt}
				disabled={!isHost}
				type="text"
				placeholder={isHost ? "STATE YOUR INTENTION" : "WAIT TO BE CALLED UPON..."}
			/>
		</form>

		<BoardSvg on:click={({ detail: { target } }) => vote(target.id)}>
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
					<Icon icon="mingcute:copy-line" color="white" width="22" />
				</button>
			</div>
		</div>
		<button on:click={restart} class="restart-button p-2 rounded-md absolute left-5 bottom-0">
			<Icon icon="mdi:restart" />
		</button>
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

	.submit-button:hover {
		@apply cursor-pointer bg-indigo-500 opacity-75;
		transform: scale(1.01);
	}

	circle {
		transition: cx 0.5s, cy 0.5s;
	}
</style>
