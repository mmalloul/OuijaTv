<script lang="ts">
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import { onMount, createEventDispatcher } from "svelte";

	const letterPositions: Record<string, Vector2> = {};
	let seekerPos: Vector2;

	const dispatch = createEventDispatcher();

	onMount(() => {
		loadLetterPositions();
		resetSeeker();
	});

	export function resetSeeker() {
		targetLetter("@");
	}

	export function targetLetter(letter: string) {
		let target = letterPositions[letter.toUpperCase()];

		if (target) {
			seekerPos = new Vector2(target.x, target.y);
		}
	}

	function onClickLetter(letterId: string) {
		dispatch("letterClicked", {
			id: letterId
		});
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

	//TODO type
	export function getTargetLetter(votes: any) {
		const target = Object.keys(votes).reduce((a, b) => (votes[a] > votes[b] ? a : b));
		return target;
	}

	class Vector2 {
		constructor(public x: number, public y: number) {}
	}
</script>

<BoardSvg on:click={({ detail: { target } }) => onClickLetter(target.id)}>
	{#if seekerPos && seekerPos.x && seekerPos.y}
		<circle
			id="Seeker"
			cx={seekerPos.x}
			cy={seekerPos.y}
			r="76.5"
			stroke="#FFF7E2"
			stroke-width="13"
		/>
	{/if}
</BoardSvg>

<style lang="postcss">
	circle {
		transition: cx 0.5s, cy 0.5s;
	}
</style>
