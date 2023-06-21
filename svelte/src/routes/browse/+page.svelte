<script lang="ts">
	import { goto } from "$app/navigation";
	import { env } from "$env/dynamic/public";
	import ExitButton from "$lib/components/ExitButton.svelte";
	import Icon from "@iconify/svelte";
	import { onMount } from "svelte";
	import { Circle } from "svelte-loading-spinners"; // Import the spinner

	let games: any[] = [];
	let loading = false;

	onMount(() => {
		fetchGames();
	});

	async function fetchGames() {
		loading = true;
		fetch(`${env.PUBLIC_URL}/games`)
			.then((response) => response.json())
			.then((responseData) => {
				games = responseData;
				loading = false;
			})
			.catch((error) => {
				console.error("Error:", error);
				loading = false;
			});
	}
</script>

<div class="page flex flex-col">
	<div class="grid-table">
		<button on:click={fetchGames} class="refresh-button">
			<Icon icon="mdi:restart" />
		</button>

		<div class="grid-container header-container">
			<div class="grid-row header-row">
				<div class="grid-cell">Game Name</div>
				<div class="grid-cell">Players</div>
				<div class="grid-cell">PIN</div>
			</div>
		</div>
		<div class="grid-container body-container overflow-auto">
			{#if loading}
				<div class="loader-container">
					<Circle />
				</div>
			{:else if games.length > 0}
				{#each games as game}
					<div class="grid-row">
						<div class="grid-cell">
							{#if game.twitch_channel}
								<a href={`https://www.twitch.tv/${game.twitch_channel}`}>
									<Icon icon="mdi:twitch" class="twitch-icon" />
								</a>
							{/if}
							{game.name}
						</div>
						<div class="grid-cell">{game.players.length}</div>
						<div class="grid-cell">
							<button class="big-button mr-5 w-full" on:click={() => goto(`/play/${game.pin}`)}>
								{game.pin}
							</button>
						</div>
					</div>
				{/each}
			{/if}
		</div>
		{#if !loading && games.length <= 0}
			<p>Currently no active games...</p>
		{/if}
	</div>
</div>

<style lang="postcss">
	.grid-table {
		max-width: 600px;
		@apply flex items-center flex-col relative text-fontcolor font-amatic text-lg w-full mx-auto md: text-4xl;
	}

	// this is the container for the header
	.header-container {
		@apply w-full;
	}

	// this is the container for the body
	.body-container {
		max-height: 70vh;
		overflow-y: auto;
		@apply w-full;

		// This will make sure that on landscape mobile the table looks good.
		@media (orientation: landscape) and (hover: none) and (pointer: coarse) {
			max-height: 50vh;
		}
	}

	// this is the container for the grid, so used both for header and body
	.grid-container {
		display: grid;
		grid-template-columns: 1fr;
	}

	// this is the row for the header, so you can adjust styling of the header
	.header-row {
		@apply text-lg font-bold mb-4 md: text-4xl;
	}

	// this is row of the table, adjust accordingly
	.grid-row {
		display: grid;
		// each fr is a column atm there are 3 columns, adjust accordingly
		grid-template-columns: 1fr 0.5fr 1fr;
		@apply w-full gap-2 md: gap-6;
	}

	// this is a cell of a table, adjust accordingly
	.grid-cell {
		@apply flex items-center w-full h-full;
		margin: 0;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.loader-container {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100px;
	}

	div :global(.twitch-icon):hover {
		color: #b9a3e3;
	}

	.join-btn:hover {
		@apply bg-accent rounded transition duration-200;
	}

	.join-btn {
		@apply border-1 p-1 rounded w-20 md:w-60;
	}

	// added absolute to this and its relative to the grid-table, adjust accordingly
	.refresh-button {
		@apply absolute top-0 right-0 flex justify-center items-center rounded-md text-4xl lg:text-4xl;
		transition: all 0.2s ease-in-out;
		text-decoration: none;
	}

	.refresh-button:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.05);
	}

	.body-container::-webkit-scrollbar {
		width: 10px;
	}

	.body-container::-webkit-scrollbar-track {
		background: black;
	}

	.body-container::-webkit-scrollbar-thumb {
		@apply bg-fontcolor rounded
		/* border-radius: 10px; */;
	}

	.body-container::-webkit-scrollbar-thumb:hover {
		background: #555;
	}
</style>
