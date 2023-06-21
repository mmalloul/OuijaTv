<script lang="ts">
	import { onDestroy, onMount } from "svelte";
	import type { IntroJs } from "intro.js";

	export let showTwitchDiv: boolean;
	let intro: IntroJs;

	onMount(async () => {
		const { default: IntroJs } = await import("intro.js");
		await import("intro.js/introjs.css");

		intro = IntroJs();

		intro.onexit(() => {
			showTwitchDiv = false;
		});

		intro.oncomplete(() => {
			showTwitchDiv = false;
		});
	});

	onDestroy(() => {
		if (intro) {
			intro.exit();
		}
	});

	export function startTourLobbyCreationPanel() {
		showTwitchDiv = true;

		intro.setOptions({
			showProgress: true,
			exitOnEsc: true,
			overlayOpacity: 0.65,
			steps: [
				{
					element: ".lobby-name-tour",
					intro: "First, think of a name for your lobby.",
					position: "right"
				},
				{
					element: ".voting-time-tour",
					intro: "Next choose the amount of time between each voting round here.",
					position: "right"
				},
				{
					element: ".game-mode-tour",
					intro:
						"Now choose your game mode! Either play multiplayer (compatible with Twitch chat) or go on a solo adventure and ask commune with an AI spirit.",
					position: "right"
				},

				{
					element: ".twitch-tour",
					intro:
						"Finally, if you are streaming, you can enable twitch integration to let your viewers vote directly from your chat. Enter the name of your twitch channel. Viewers can join your game by typing !play and vote with commands like !a or !b and !goodbye.",
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
					intro: "This is the board. It shall be used by the spirits to communicate with you."
				},
				{
					element: "#Seeker",
					intro:
						"This is the seeker. It will move towards the character that has the most popular vote among the spirits."
				},
				{
					element: "#prompt",
					intro:
						"You decide what to ask the spirits! You can ask them any question, or ask them to spell out a missing word in a sentence.",
					position: "left"
				},
				{
					element: ".prompt-button",
					intro:
						"When you're ready, click on this button to send your question to the spirits. The spirits can only start voting once a question has been asked!",
					position: "right"
				},
				{
					element: ".timer",
					intro:
						"Once the question has been asked, the clock will start ticking. At the end of each round, the most popular letter shall be added to the answer.",
					position: "left"
				},
				{
					element: ".spirit-answer > span",
					intro: "The answer will be built up letter by letter and shown here.",
					position: "bottom"
				},
				{
					element: ".restart-button",
					intro:
						"Restart the game by pressing this button. Warning: This resets all the current progress of this game.",
					position: "right"
				},
				{
					element: ".link-share",
					intro: "Share this link with others so they can join your lobby as spirits!",
					position: "top"
				},
				{
					element: "#exit-button",
					intro:
						"You can quit the game here. As you are the host, the lobby shall be closed at that point.",
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
					intro: "This is the board. It shall be used by the spirits to communicate with you."
				},
				{
					element: "#Seeker",
					intro:
						"This is the seeker. It will move towards the character that has the most popular vote among the spirits."
				},
				{
					element: "#MyVote",
					intro:
						"The secondary seeker (with a lower opacity) is your personal seeker, it shows you what you personally voted on. You can only vote once per round!"
				},
				{
					element: ".prompt",
					intro:
						"The host will ask you a question, it is your task to answer them! You can only start voting once a question has been asked.",
					position: "left"
				},
				{
					element: ".timer",
					intro:
						"Once the question has been asked, the clock will start ticking. At the end of each round, the most popular letter shall be added to the answer.",
					position: "left"
				},
				{
					element: ".spirit-answer > span",
					intro: "The answer will be built up letter by letter and shown here.",
					position: "bottom"
				},
				{
					element: "#exit-button",
					intro: "You can leave the game by pressing the exit button.",
					position: "right"
				},
				{
					intro:
						"Now wait for the host to ask you a question and communicate with them as a spirit! 👻"
				}
			]
		});

		intro.start();
	}
</script>
