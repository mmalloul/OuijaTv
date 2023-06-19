<script lang="ts">
	import { onMount } from "svelte";
	import GhostImage from "$lib/assets/ghost.png";
	import AbsolutePositionMotor from "$lib/components/AbsolutePositionMotor.svelte";

	// Width of the ghost image
	let ghostWidth = 75;

	// Bounds of the window
	let maxX = window.innerWidth - ghostWidth * 2;
	let maxY = window.innerHeight - ghostWidth * 2;

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

<AbsolutePositionMotor bind:maxX bind:maxY>
	<div class="-z-10 font">
		<div class="flex flex-col items-center">
			<img class="opacity-25" width={ghostWidth} src={GhostImage} alt="A spirit" />
			<slot />
		</div>
	</div>
</AbsolutePositionMotor>

<style lang="postcss">
	.font {
		@apply text-fontcolor text-2xl;
		font-family: theme(fontFamily.amatic);
	}
</style>
