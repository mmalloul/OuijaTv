<script lang="ts">
	import { getContext, onMount, onDestroy } from "svelte";
	import type { Writable } from "svelte/store";
	import { openApiCall } from "$lib/functions/apiCall";
	import toast, { Toaster } from "svelte-french-toast";
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import Card from "$lib/components/Card.svelte";
	import spirit1 from "$lib/assets/spirit1.webp";
	import spirit2 from "$lib/assets/spirit2.webp";
	import spirit3 from "$lib/assets/spirit3.webp";
	import spirit4 from "$lib/assets/spirit4.webp";

	let showCards = true,
		showBoard = false,
		showInput = true;
	let seekerX: number;
	let seekerY: number;
	let circleStyle = "";
	let prompt = "";
	let answer = "";
	let name = "";
	let tags = "";
	let sp = 0;

	const showMenu = getContext<Writable<boolean>>("showMenu");

	const letterPositions: Record<string, Vector2> = {};
	class Vector2 {
		constructor(public x: number, public y: number) {}
	}

	function handleGoToQuestion(spirit: number, nm: string, tag: string) {
		(showCards = false), (showBoard = true);
		(name = nm), (sp = spirit), (tags = tag);
	}

	async function ask() {
		if (prompt === "") {
			toast("Just tell me what you want to ask and dont waste my time.", {
				icon: "👻",
				style: "border-radius: 200px; background: #333; color: #fff;",
				duration: 2000
			});
			return;
		} else {
			showInput = false;
			readBoard();
			answer = await openApiCall(prompt, sp);
			printWord(answer);
		}
	}
	function readBoard() {
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

	async function printWord(word: string) {
		const split = word.split("");
		for (let i = 0; i < split.length; i++) {
			await new Promise((resolve) => setTimeout(resolve, 2000));
			targetALetter(split[i]);
		}
		await new Promise((resolve) => setTimeout(resolve, 2000));
		seekerX = 960.5;
		seekerY = 766.5;
		showInput = true;
		return;
	}

	function targetALetter(letter: string) {
		let target = letterPositions[letter.toUpperCase()];
		if (target) {
			seekerX = target.x;
			seekerY = target.y;
		}
	}

	onMount(() => {
		showMenu.set(false);
	});

	onDestroy(() => {
		showMenu.set(true);
	});
</script>

<Toaster />
{#if showCards}
	<div class="page">
		<div>
			<h1 class="awnser">SOLO Summon</h1>
			<div class="subtask">
				As you navigate to the website and click on the Ouija board feature, a sense of apprehension
				washes over you. You know that this virtual board may not be as innocuous as it seems, and
				that you could be inviting something dark and powerful into your life. Select the dark
				spirit that you desire and use him by <b>clicking</b> on the card.
			</div>
		</div>
		<div class="l-container">
			<Card
				spirit="1"
				goToQuestion={handleGoToQuestion}
				name="Sgt. Sabrina"
				backgroundImage={spirit1}
				tag="Friendly, Scary"
				lore="Lorem ipsum dolor, sit amet consectetur adipisicing elit..."
			/>
			<Card
				spirit="2"
				goToQuestion={handleGoToQuestion}
				name="Asta"
				backgroundImage={spirit2}
				tag="Clever, Funny"
				lore="Lorem ipsum dolor, sit amet consectetur adipisicing elit..."
			/>
			<Card
				spirit="3"
				goToQuestion={handleGoToQuestion}
				name="Miko Mana"
				backgroundImage={spirit3}
				tag="Funny, Rich, Clever"
				lore="Lorem ipsum dolor, sit amet consectetur adipisicing elit..."
			/>
			<Card
				spirit="4"
				goToQuestion={handleGoToQuestion}
				name="The Crow"
				backgroundImage={spirit4}
				tag="Dark, Scary"
				lore="Lorem ipsum dolor, sit amet consectetur adipisicing elit..."
			/>
		</div>
	</div>
{/if}

{#if showBoard}
	<div class="page--game flex flex-col items-center">
		<form class="flex">
			<input bind:value={prompt} type="text" placeholder="STATE YOUR INTENTION" />
		</form>
		{#if showInput}
			{#if prompt != ""}
				<button type="button" class="custom-button" on:click={() => ask()}>
					<p>Ask</p>
				</button>
			{/if}
		{/if}

		<div class="char">
			<span class="text-light-50"> Name:</span>
			<span class="te"> {name} <br /></span>
			<span class="text-light-50"> Tags:</span>
			<span class="te"> {tags}</span>
		</div>
		<BoardSvg>
			<circle
				id="Seeker"
				style={circleStyle}
				cx={seekerX}
				cy={seekerY}
				r="76.5"
				stroke="#FFF7E2"
				stroke-width="13"
			/>
		</BoardSvg>
	</div>
{/if}

<style lang="postcss">
	.te {
		@apply text-accent;
	}
	.char {
		@apply text-3xl pt-2;
		font-family: theme(fontFamily.amatic);
		width: 250px;
		text-align: center;
	}
	.l-container {
		display: grid;
		grid-template-columns: repeat(4, 1fr);
		grid-gap: 30px;
		width: 100%;
		padding: 30px;
		justify-content: center;
		@media screen and (max-width: 1150px) {
			grid-template-columns: repeat(2, 2fr);
		}
	}
	.awnser {
		color: white;
		text-align: center;
		font-size: xxx-large;
		margin: 0% auto;
		@apply text-accent;
		font-family: theme(fontFamily.amatic);
	}
	.subtask {
		max-width: 75%;
		text-align: center;
		margin: auto;
		color: white;
		font-size: x-large;
		font-family: theme(fontFamily.amatic);
	}
	input {
		@apply w-full mx-50 w-200  text-center;
		font-family: theme(fontFamily.amatic);
		font-size: 3rem;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
	}
	.custom-button {
		@apply text-fontcolor text-4xl  border-1;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		width: 20%;
		border-color: #dddddd;
		transition: all 0.2s ease-in-out;
	}

	.custom-button > p {
		transition: all 0.2s ease-in-out;
	}

	.custom-button:hover {
		@apply cursor-pointer bg-dark opacity-75;
		border-style: solid;
	}

	.custom-button:hover > p {
		@apply text-accent;
	}

	.custom-button:hover > p {
		transform: scale(1.05);
	}

	circle {
		transition: cx 0.5s, cy 0.5s;
	}
</style>
