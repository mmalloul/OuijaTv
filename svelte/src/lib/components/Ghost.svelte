<script lang="ts">
	import { onMount } from "svelte";
	import GhostImage from "$lib/assets/ghost.png";

	const timeBetweenTicks = 350;
	const minTicksBetweenRelocation = 5;
	const maxTicksBetweenRelocation = 30;
	const maxRelocationDistance = 300;
	// Percentage chance that the ghost will move towards the location instead of randomly
	const steerPercentage = 0.25;

	// Location that the ghost is targeting
	let locationX = 0;
	let locationY = 0;
	// Current location of the ghost
	let currentX = 0;
	let currentY = 0;

	// Bounds of the window
	let maxX = 0;
	let maxY = 0;

	// Width of the ghost image
	let ghostWidth = 75;

	let tick = 0;
	let movementStep = 25;
	let ticksBetweenRelocation: number;

	onMount(() => {
		updateBounds();
		// A reactive statement for maxX and maxY wouldn't work here because the reference doesn't update.
		window.addEventListener("resize", updateBounds, false);
		// set x and y to a random position between 0 and maxX/maxY
		currentX = Math.floor(Math.random() * maxX);
		currentY = Math.floor(Math.random() * maxY);
		locationX = currentX;
		locationY = currentY;
		ticksBetweenRelocation = randIntBetweenExclusive(
			minTicksBetweenRelocation,
			maxTicksBetweenRelocation
		);

		const interval = setInterval(() => {
			onTick();
		}, timeBetweenTicks);

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
		// Relocate every so often, otherwise move around the location
		if (++tick > ticksBetweenRelocation) {
			tick = 0;
			ticksBetweenRelocation = randIntBetweenExclusive(
				minTicksBetweenRelocation,
				maxTicksBetweenRelocation
			);
			relocate();
		} else {
			moveAroundLocation();
		}
	}

	/// Moves the ghost around the target location
	function moveAroundLocation() {
		// 25% chance to move towards the location, 75% chance to move randomly
		performByPercentage(moveTowardsLocation, moveRandomly, steerPercentage);
	}

	/// Moves the ghost towards the target location
	function moveTowardsLocation() {
		/// Get the sign of the difference between the current and target location
		let signX = Math.sign(locationX - currentX);
		let signY = Math.sign(locationY - currentY);
		// Move towards the location
		currentX += -signX * movementStep;
		currentY += -signY * movementStep;
	}

	/// Moves the ghost in a random direction
	function moveRandomly() {
		// Get a random sign
		let signX = Math.random() < 0.5 ? -1 : 1;
		let signY = Math.random() < 0.5 ? -1 : 1;

		currentX = clamp(currentX + signX * movementStep, 0, maxX);
		currentY = clamp(currentY + signY * movementStep, 0, maxY);
	}

	/// Relocates the ghost to hover around a new location
	function relocate() {
		// Pick a new location to relocate to, but don't exceed the maxRelocationDistance.
		// This is to prevent the ghost from teleporting across the screen.
		// If the ghost is too close to the edge of the screen, it will pick a location that
		// is closer to the center of the screen.
		if (locationX < maxRelocationDistance) {
			locationX = clamp(locationX + randIntBetweenExclusive(0, maxRelocationDistance), 0, maxX);
		} else if (locationX > maxX - locationX) {
			locationX = clamp(locationX + randIntBetweenExclusive(-maxRelocationDistance, 0), 0, maxX);
		} else {
			locationX = clamp(
				locationX + randIntBetweenExclusive(-maxRelocationDistance, maxRelocationDistance),
				0,
				maxX
			);
		}

		if (locationY < maxRelocationDistance) {
			locationY = clamp(locationY + randIntBetweenExclusive(0, maxRelocationDistance), 0, maxY);
		} else if (locationY > maxY - locationY) {
			locationY = clamp(locationY + randIntBetweenExclusive(-maxRelocationDistance, 0), 0, maxY);
		} else {
			locationY = clamp(
				locationY + randIntBetweenExclusive(-maxRelocationDistance, maxRelocationDistance),
				0,
				maxY
			);
		}
		// Set the current location of the ghost to the new location
		currentX = locationX;
		currentY = locationY;
	}

	/// Returns a random integer between min (inclusive) and max (exclusive)
	function randIntBetweenExclusive(min: number, max: number) {
		return Math.floor(Math.random() * (max - min) + min);
	}

	/// Returns a random integer between min (inclusive) and max (inclusive)
	function clamp(value: number, min: number, max: number) {
		return Math.max(min, Math.min(max, value));
	}

	/// Performs funcA with a percentage chance, otherwise performs funcB
	function performByPercentage(funcA: () => void, funcB: () => void, percentage: number) {
		if (Math.random() < percentage) {
			funcA();
		} else {
			funcB();
		}
	}
</script>

<div
	class="-z-10 font duration-1000"
	style="position: absolute; left: {currentX}px; bottom: {currentY}px;"
>
	<div class="flex flex-col items-center">
		<img class="opacity-25" width={ghostWidth} src={GhostImage} alt="A spirit" />
		<slot />
	</div>
</div>

<style lang="postcss">
	.font {
		@apply text-fontcolor text-2xl;
		font-family: theme(fontFamily.amatic);
	}
</style>
