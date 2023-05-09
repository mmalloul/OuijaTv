<script lang="ts">
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import { onMount } from "svelte";

	let seekerX = 0,
		seekerY = 0;

	interface CircleProps {
		pos: Vector2;
		r: string;
	}

	class Vector2 {
		constructor(public x: number, public y: number) {}
	}

	const letterPositions: Record<string, Vector2> = {};

	let targetLetter = "A";

	onMount(() => {
		const circleElements = document.querySelectorAll<SVGCircleElement>("circle");

		circleElements.forEach((element) => {
			const id = element.id;
			let x = element.attributes.getNamedItem("cx")?.value;
			let y = element.attributes.getNamedItem("cy")?.value;
			if (x && y) {
				letterPositions[id.charAt(id.length - 1)] = new Vector2(parseFloat(x), parseFloat(y));
			}
		});

		console.log(letterPositions[targetLetter]);
	});

	function targetALetter(letter: string) {
		var target = letterPositions[letter.toUpperCase()];
		seekerX = target.x;
		seekerY = target.y;
	}
</script>

<div id="wrapper" class="absolute-center page--game">
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
