<script lang="ts">
	import { onMount } from "svelte";
	import { page } from "$app/stores";
	import { env } from "$env/dynamic/public";
	import BoardSvg from "$lib/components/BoardSVG.svelte";

	let status = "";
	let messages: string[] = [];

	const letterPositions: Record<string, Vector2> = {};

	let seekerX = 0,
		seekerY = 0;
	let targetLetter = "A";

	onMount(() => {
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
		const websocket = new WebSocket(`${env.PUBLIC_WS_URL}/join?pin=${pin}`);
		websocket.onclose = () => (status = "game not found");
		websocket.onmessage = ({ data }) => {
			if (status) {
				messages = [...messages, data];
			} else {
				status = "connected!";
			}
			targetALetter(messages[messages.length - 1]);
		};
	}

	function targetALetter(letter: string) {
		console.log("targeting " + letter);
		var target = letterPositions[letter.toUpperCase()];
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
		<button on:click={() => targetALetter(targetLetter)}>click</button>
	</label>

	<BoardSvg>
		<circle id="Seeker" cx={seekerX} cy={seekerY} r="76.5" stroke="#FFF7E2" stroke-width="13" />
	</BoardSvg>
</div>

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
