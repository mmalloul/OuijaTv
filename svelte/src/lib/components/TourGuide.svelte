<script lang="ts">
	import { onMount } from "svelte";
	import type { IntroJs } from "intro.js";

	let intro: IntroJs;

	onMount(async () => {
		const { default: IntroJs } = await import("intro.js");
		await import("intro.js/introjs.css");

		intro = IntroJs();
	});

	export function startTour() {
		intro.setOptions({
            showProgress: true,
			exitOnEsc: true,
			overlayOpacity: 0.65,

			steps: [
				{
					element: "#lobby-name",
					intro: "First think of a name for your lobby",
					position: "right"
				},
				{
					element: "#gameMode",
					intro: "Choose your gamemode! Either play multiplayer integrated with Twitch or go on a solo adventure against a AI spirit",
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
</script>
