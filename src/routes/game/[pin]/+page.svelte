<script lang="ts">
	import { onMount } from "svelte";
	import { page } from "$app/stores";
	import { env } from "$env/dynamic/public";
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import toast, { Toaster } from "svelte-french-toast";

	let status = "";
	let messages: string[] = [];

	const placeholderUsername = "USERNAME_NOT_SET";
	let username = placeholderUsername;

	const letterPositions: Record<string, Vector2> = {};

	let seekerX = 0,
		seekerY = 0;
	let targetLetter = "A";

	onMount(() => {
		username = localStorage.getItem("username") || placeholderUsername;
		initBoard();
		initSpiritSocket();
	});

	function initBoard() {
		loadLetterPositions();
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

	function initSpiritSocket() {
		const pin = $page.params.pin;
		const websocket = new WebSocket(`${env.PUBLIC_WS_URL}/join?pin=${pin}&name=${username}`);
		websocket.onclose = () => (status = "game not found");
		websocket.onmessage = ({ data }) => {
			// Wrapped with try-catch, because if websocket sends string instead of JSON it will raise an error.
			// Now every other message that isn't JSON will still be received.
			try {
				let parsedData = JSON.parse(data);

				if (parsedData && parsedData.action === "restart_game") {
					seekerX = 0;
					seekerY = 0;
					toast("The host has restarted the game!", {
						icon: "👻",
						position: "bottom-center",
						style: "border-radius: 200px; background: #333; color: #fff;",
						duration: 3000
					});
				}
			} catch (e) {
				messages = [...messages, data];
				targetALetter(messages[messages.length - 1]);
			}
		};
	}

	function vote(on: string) {

	}

	function targetALetter(letter: string) {
		const target = letterPositions[letter.toUpperCase()];
		seekerX = target.x;
		seekerY = target.y;
	}

	class Vector2 {
		constructor(public x: number, public y: number) {}
	}
</script>

<div id="wrapper" class="absolute-center page--game">
	{status}

	<label>
		<input type="range" bind:value={seekerX} min="0" max="1920" />
		<input type="range" bind:value={seekerY} min="0" max="1080" />
		<input type="text" bind:value={targetLetter} />
		<button on:click={() => vote(targetLetter)}>click</button>
	</label>

	<BoardSvg>
		<circle id="Seeker" cx={seekerX} cy={seekerY} r="76.5" stroke="#FFF7E2" stroke-width="13" />
	</BoardSvg>
</div>

<Toaster />

<style>
	button {
		background-color: aliceblue;
	}

	circle {
		transition: cx 0.5s, cy 0.5s;
	}

	#wrapper {
		height: 75%;
		width: 75%;
	}

	.absolute-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}
</style>
