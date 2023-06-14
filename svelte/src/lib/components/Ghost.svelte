<script lang="ts">
	import { onMount } from "svelte";
	import GhostImage from "$lib/assets/ghost.png";
	import Motor from "$lib/components/Motor.svelte";

	const timeBetweenTicks = 350;
	const minTicksBetweenRelocation = 5;
	const maxTicksBetweenRelocation = 30;
	const maxRelocationDistance = 300;
	// Percentage chance that the ghost will move towards the location instead of randomly
	const steerPercentage = 0.25;

	// Bounds of the window
	let maxX = 0;
	let maxY = 0;

	// Width of the ghost image
	let ghostWidth = 75;

	onMount(() => {
		updateBounds();
		// A reactive statement for maxX and maxY wouldn't work here because the reference doesn't update.
		window.addEventListener("resize", updateBounds, false);
	});

	function updateBounds() {
		maxX = window.innerWidth - ghostWidth * 2;
		maxY = window.innerHeight - ghostWidth * 2;
	}
</script>

<Motor bind:maxX bind:maxY>
	<div class="-z-10 font">
		<div class="flex flex-col items-center">
			<img class="opacity-25" width={ghostWidth} src={GhostImage} alt="A spirit" />
			<slot />
		</div>
	</div>
</Motor>

<style lang="postcss">
	.font {
		@apply text-fontcolor text-2xl;
		font-family: theme(fontFamily.amatic);
	}
</style>
