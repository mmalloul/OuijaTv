<script lang="ts">
	import { onMount } from "svelte";
	import type { IntroJs } from "intro.js";

	let intro: IntroJs;

	onMount(async () => {
		const { default: IntroJs } = await import("intro.js");
		await import("intro.js/introjs.css");

		intro = IntroJs();
	});

	export function startTourLobbyCreationPanel() {
		intro.setOptions({
			showProgress: true,
			exitOnEsc: true,
			overlayOpacity: 0.65,
			steps: [
				{
					element: "#lobby-name",
					intro: "First think of a name for your lobby.",
					position: "right"
				},
				{
					element: "#gameMode",
					intro:
						"Choose your game mode! Either play multiplayer integrated with Twitch or go on a solo adventure against a AI spirit.",
					position: "right"
				},
				{
					element: "#duration",
					intro: "Decide the amount of voting time for each round!",
					position: "right"
				}
			]
		});

		intro.start();
	}

	export function startTourGameHost() {
		intro.setOptions({
			showProgress: true,
			exitOnEsc: true,
			overlayOpacity: 0.65,
			disableInteraction: true,
			steps: [
				{
					intro: "Welcome to the Ouija board!",
					position: "right"
				},
				{
					element: "#board",
					intro: "The board shall be used by the spirits to communicate with the host."
				},
				{
					element: "#Seeker",
					intro: "The seeker will move based on the current winning vote."
				},
				{
					element: "#prompt",
					intro: "As a host you decide what to ask to the spirits!",
					position: "left"
				},
				{
					element: ".prompt-button",
					intro:
						"When you're ready, you can send the question to the spirits. The spirits can only start voting once a question has been asked!",
					position: "right"
				},
				{
					element: ".timer",
					intro:
						"Once the question has been sent the clock will start ticking for each voting round. At the end of each round the most popular letter shall be picked.",
					position: "left"
				},
				{
					element: ".spirit-answer",
					intro: "The chosen letters for each round will be displayed here.",
					position: "bottom"
				},
				{
					element: ".restart-button",
					intro:
						"You can restart the game by pressing this button, which shall reset all the current progress.",
					position: "right"
				},
				{
					element: ".link-share",
					intro: "Share this lobby with other players to play with!",
					position: "left"
				},
				{
					element: "#exit-button",
					intro: "By exiting the game as a host the lobby shall be closed.",
					position: "right"
				},
				{
					intro: "Now start communicating with the spirits! 👻"
				}
			]
		});

		intro.start();
	}

	export function startTourGamePlayer() {
		intro.setOptions({
			showProgress: true,
			exitOnEsc: true,
			overlayOpacity: 0.65,
			disableInteraction: true,
			steps: [
				{
					intro: "Welcome to the Ouija board!",
					position: "right"
				},
				{
					element: "#board",
					intro:
						"The board shall be used by you and the other spirits to communicate with the host. The seeker will move around based on the votes."
				},
				{
					element: "#Seeker",
					intro:
						"The bold seeker is the seeker for the game that everybody sees, this will move based on the current winning vote."
				},
				{
					element: "#MyVote",
					intro:
						"The seeker with a lower opacity is your seeker which will showcase what you voted on. You can only vote once per round!"
				},
				{
					element: ".prompt",
					intro:
						"The host will ask you a question for you to answer! You can only start voting once a question has been asked!",
					position: "left"
				},
				{
					element: ".timer",
					intro:
						"Once the question has been sent the clock will start ticking for each voting round. At the end of each round the most popular letter shall be picked.",
					position: "left"
				},
				{
					element: ".spirit-answer",
					intro: "The chosen letters for each round will be displayed here.",
					position: "bottom"
				},
				{
					element: "#exit-button",
					intro: "You can leave the game by pressing the exit button.",
					position: "right"
				},
				{
					intro: "Now start communicating with the host as a spirit! 👻"
				}
			]
		});

		intro.start();
	}
</script>
