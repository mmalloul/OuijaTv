<script lang="ts">

    import { onMount } from "svelte";

    const timeBetweenTicks = 350;
	const minTicksBetweenRelocation = 5;
	const maxTicksBetweenRelocation = 30;
	const maxRelocationDistance = 300;
	// Percentage chance that the ghost will move towards the location instead of randomly
	const steerPercentage = 0.25;
	const moveSmoothingms = 1500;

    // Location that the ghost is targeting
	let locationX = 0;
	let locationY = 0;
	// Current location of the ghost
	let x = 0;
	let y = 0;

	// Bounds of the window, bound from external component
	export let maxX = 0;
	export let maxY = 0;

    let tick = 0;
	let movementStep = 25;
	let ticksBetweenRelocation: number;

    onMount(() => {
        // set x and y to a random position between 0 and maxX/maxY
		locationX = Math.floor(Math.random() * maxX);
		locationY = Math.floor(Math.random() * maxY);
		x = locationX;
		y = locationY;
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
		let signX = Math.sign(locationX - x);
		let signY = Math.sign(locationY - y);
		// Move towards the location
		x += -signX * movementStep;
		y += -signY * movementStep;
	}

	/// Moves the ghost in a random direction
	function moveRandomly() {
		// Get a random sign
		let signX = Math.random() < 0.5 ? -1 : 1;
		let signY = Math.random() < 0.5 ? -1 : 1;

		x = clamp(x + signX * movementStep, 0, maxX);
		y = clamp(y + signY * movementStep, 0, maxY);
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
		x = locationX;
		y = locationY;
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
style="position: absolute; left: {x}px; bottom: {y}px; 	transition-duration: {moveSmoothingms}ms;"
>
	<slot/>
</div>