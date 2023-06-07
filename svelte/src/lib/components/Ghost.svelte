<script lang="ts">
	import { onMount } from "svelte";
	import GhostImage from "$lib/assets/ghost.png";

	let x = 0;
	let y = 0;
	let ghostWidth = 75;
	let maxX = 0;
	let maxY = 0;

	let movementStep = 50;
	const timeBetweenSteps = 200;

	onMount(() => {
		updateBounds();
		// A reactive statement for maxX and maxY wouldn't work here because the reference doesn't update.
		window.addEventListener("resize", updateBounds, false);
		// set x and y to a random position between 0 and maxX/maxY
		x = Math.floor(Math.random() * maxX);
		y = Math.floor(Math.random() * maxY);

		const interval = setInterval(() => {
			onTick();
		}, timeBetweenSteps);

		// Clean up the interval when the component is unmounted
		return () => {
			clearInterval(interval);
		};
	});

	function updateBounds() {
		maxX = window.innerWidth - ghostWidth * 2;
		maxY = window.innerHeight - ghostWidth * 2;
	}

	function onTick() {
		// Add a random integer between - movementStep and movementStep to x and y
		x += Math.floor(Math.random() * (movementStep * 2)) - movementStep;
		y += Math.floor(Math.random() * (movementStep * 2)) - movementStep;

		// Clamp x and y to be between 0 and 100
		x = Math.max(0, Math.min(maxX, x));
		y = Math.max(0, Math.min(maxY, y));
	}
</script>

<div class="-z-10 text-white duration-1000" style="position: absolute; left: {x}px; bottom: {y}px;">
	<img class="opacity-25" width={ghostWidth} src={GhostImage} alt="A spirit" />
	<slot />
</div>
