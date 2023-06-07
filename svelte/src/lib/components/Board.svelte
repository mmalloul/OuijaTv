<script lang="ts">
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import { onMount, createEventDispatcher } from "svelte";

	const letterPositions: Record<string, Vector2> = {};
	const dispatch = createEventDispatcher();

	export let canVote: boolean;
	export let isHost: boolean;

	let seekerPos: Vector2;
	let ownVotePos: Vector2;

	$: if (canVote) {
		resetPlayerSeeker();
	}

	onMount(() => {
		loadLetterPositions();
		resetSeeker();
	});

	export function resetSeeker() {
		moveSeekerToLetter("@");
		showMyVote("@");
	}

	function resetPlayerSeeker() {
		showMyVote("@");
	}

	function getLetterPosition(letter: string) {
		return letterPositions[letter.toUpperCase()];
	}

	export function moveSeekerToLetter(letter: string) {
		let target = getLetterPosition(letter);
		if (target) {
			seekerPos = new Vector2(target.x, target.y);
		}
	}

	function showMyVote(letter: string) {
		let target = getLetterPosition(letter);
		if (target) {
			ownVotePos = new Vector2(target.x, target.y);
		}
	}

	function onClickLetter(letterId: string) {
		if (canVote) {
			dispatch("letterClicked", {
				id: letterId
			});
			showMyVote(letterId);
		}
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

	class Vector2 {
		constructor(public x: number, public y: number) {}
	}
</script>

<BoardSvg
	on:click={({ detail: { target } }) => onClickLetter(target.id.charAt(target.id.length - 1))}
>
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

	{#if !isHost && ownVotePos && ownVotePos.x && ownVotePos.y}
		<circle
			id="MyVote"
			cx={ownVotePos.x}
			cy={ownVotePos.y}
			r="76.5"
			stroke="#FFF7E2"
			stroke-width="13"
			stroke-opacity=".25"
		/>
	{/if}
</BoardSvg>

<style lang="postcss">
	circle {
		transition: cx 0.5s, cy 0.5s;
	}
</style>
