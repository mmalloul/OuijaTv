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
	import Icon from "@iconify/svelte";
	import Ghost from "$lib/components/Ghost.svelte";

	let showCards = true,
		showBoard = false;
	let canPrompt = true;
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
			readBoard();
			answer = await openApiCall(prompt, sp);
			canPrompt = false;
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
		seekerY = 800.5;
		canPrompt = true;
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
			<div class="back-to-menu">
				<a href="/"><Icon icon="formkit:arrowleft" />Exit</a>
			</div>
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
				lore="Sgt. Sabrina is an enigmatic character, embodying a unique combination of friendliness and an underlying sense of fear. With an inviting smile that conceals a chilling aura, she effortlessly navigates between approachability and an unsettling presence. Her interactions leave a lasting impact, as she effortlessly blends warmth with an eerie undertone. One moment, she's your confidant, offering a comforting presence, and the next, she reveals a disconcerting glimpse into the unknown. Sgt. Sabrina is an enigmatic force that simultaneously attracts and unnerves those around her."
			/>
			<Card
				spirit="2"
				goToQuestion={handleGoToQuestion}
				name="Asta"
				backgroundImage={spirit2}
				tag="Clever, Funny"
				lore="Asta, the legendary Japanese samurai, is renowned for his remarkable wit and cleverness. Armed with his razor-sharp katana and a quick tongue, he effortlessly blends intelligence and humor into his every move. Asta's sharp mind allows him to outsmart opponents and navigate intricate situations with ease, all while weaving in a dose of his unique brand of humor. Whether through a clever retort or a well-timed jest, Asta never fails to bring laughter to those around him. His charisma and wit make him an unforgettable companion on any adventure, leaving a trail of laughter in his wake."
			/>
			<Card
				spirit="3"
				goToQuestion={handleGoToQuestion}
				name="Miko Mana"
				backgroundImage={spirit3}
				tag="Funny, Rich, Clever"
				lore="Miko, the enchanting heiress of untold wealth, possesses a captivating blend of humor, opulence, and sharp intellect. Adorned in extravagant gowns, she graces the realm with her radiant presence. With a mischievous glimmer in her eyes, Miko effortlessly employs her clever wit to turn any situation into a comedic spectacle. Her wealth enables her to procure lavish items and fund daring escapades, while her quick thinking and cunning mind ensure that she stays one step ahead of any challenge. Miko's charismatic charm and unparalleled sense of humor make her the life of every extravagant gathering, leaving a trail of laughter and awe in her opulent wake."
			/>
			<Card
				spirit="4"
				goToQuestion={handleGoToQuestion}
				name="The Crow"
				backgroundImage={spirit4}
				tag="Dark, Scary"
				lore="The Crow, a malevolent presence cloaked in darkness, strikes fear into the hearts of all who dare to cross his path. With his ominous aura and chilling gaze, he embodies the essence of terror. The Crow moves stealthily, lurking in the shadows with an uncanny ability to strike without warning. His actions are shrouded in darkness, leaving a trail of haunting whispers and foreboding silence in his wake. The mere mention of his name sends shivers down spines, and his dark presence leaves a lasting impression on those unfortunate enough to encounter him. The Crow is the embodiment of fear itself, a relentless and terrifying force that preys on the souls of the unwary."
			/>
		</div>
	</div>
{/if}

{#if showBoard}
	<div class="page--game flex flex-col items-center">
		<div class="game-header">
			<form class="flex">
				<div class="back-to-menu">
					<a href="/"><Icon icon="formkit:arrowleft" />Exit</a>
				</div>
				<input
					bind:value={prompt}
					type="text"
					placeholder="STATE YOUR INTENTION"
					disabled={!canPrompt}
				/>
				<button type="button" class="custom-button" on:click={() => ask()}>
					<p>Ask</p>
				</button>
			</form>
		</div>

		<Ghost>
			<p class="opacity-75">
				<span class="text-light-50"> Name:</span>
				<span class="te"> {name} <br /></span>
				<span class="text-light-50"> Tags:</span>
				<span class="te"> {tags}</span>
			</p>
		</Ghost>

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
	.game-header {
		@apply flex  md: flex-row justify-center items-center w-full flex-wrap;
		transition: all 0.5s ease-in-out;
	}
	.te {
		@apply text-accent;
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
		@apply w-full mx-10 w-200  text-center;
		font-family: theme(fontFamily.amatic);
		font-size: 2rem;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
	}
	.custom-button {
		@apply text-fontcolor text-4xl  border-1 rounded-md;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		width: 20%;
		border-color: #dddddd;
		transition: all 0.2s ease-in-out;
	}

	.back-to-menu {
		@apply font-amatic text-center text-fontcolor flex flex-1 flex-grow;
	}

	.back-to-menu a {
		@apply flex justify-center items-center px-2 rounded-md  text-lg lg: text-3xl;
		transition: all 0.2s ease-in-out;
		text-decoration: none;
	}

	.back-to-menu a:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
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
