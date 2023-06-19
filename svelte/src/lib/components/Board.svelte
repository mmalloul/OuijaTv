<script lang="ts">
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import { onMount, createEventDispatcher } from "svelte";

	const letterPositions: Record<string, Vector2> = {};
	const dispatch = createEventDispatcher();

	export let canVote: boolean;
	export let isHost: boolean;
	export let timeLeft: number | undefined;
	export let roundTime: number;

	let seekerPos: Vector2;
	let seekerTarget: Vector2;
	let ownVotePos: Vector2;

	const seekerWalkRadius = 20;
	const timeBetweenTicks = 200;
	const movementStep = 10;

	$: if (canVote) {
		resetPlayerSeeker();
	}

	onMount(() => {
		loadLetterPositions();
		resetSeeker();
		seekerPos = structuredClone(seekerTarget);

		const interval = setInterval(() => {
			onTick();
		}, timeBetweenTicks);

		// Clean up the interval when the component is unmounted
		return () => {
			clearInterval(interval);
		};
	});

	function onTick() {
		moveSeeker();
	}

	function moveSeeker() {
		// Check if seekerPos is in seekerWalkRadius of targetPos
		// If so, move seekerPos by a random integer between -movementStep and movementStep
		// If not, move seekerPos towards targetPos by movementStep
		let distance = Math.sqrt(
			Math.pow(seekerPos.x - seekerTarget.x, 2) + Math.pow(seekerPos.y - seekerTarget.y, 2)
		);

		if (distance < seekerWalkRadius) {
			// Move randomly
			seekerPos.x += randIntBetweenExclusive(-movementStep, movementStep);
			seekerPos.y += randIntBetweenExclusive(-movementStep, movementStep);
		} else {
			// Linearly interpolate seekerPos towards seekerTarget by timeLeft / 15
			let timeLeftFactor = timeLeft ? (roundTime - timeLeft) / roundTime : 1;
			seekerPos.x += (seekerTarget.x - seekerPos.x) * timeLeftFactor;
			seekerPos.y += (seekerTarget.y - seekerPos.y) * timeLeftFactor;
		}
	}

	function randIntBetweenExclusive(min: number, max: number) {
		return Math.floor(Math.random() * (max - min) + min);
	}

	export function resetSeeker() {
		moveSeekerTargetToLetter("@");
		showMyVote("@");
	}

	function resetPlayerSeeker() {
		showMyVote("@");
	}

	function getLetterPosition(letter: string) {
		return letterPositions[letter.toUpperCase()];
	}

	export function moveSeekerTargetToLetter(letter: string) {
		let target = getLetterPosition(letter);
		if (target) {
			seekerTarget = new Vector2(target.x, target.y);
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
