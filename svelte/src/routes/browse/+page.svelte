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

<div class="page">
	<ExitButton onExit={(MouseEvent) => Promise.resolve()} />

	<div class="flex justify-center mt-8 font py-10">
		<div class="table-container">
			<table class="w-full">
				<thead>
					<tr>
						<th class="flex justify-start items-center">Game Name</th>
						<th>Players</th>
						<th class="flex justify-start items-center">PIN</th>
						<th>
							<button on:click={fetchGames} class="refresh-button">
								<Icon icon="mdi:restart" />
							</button>
						</th>
					</tr>
				</thead>
				{#if loading}
					<div class="loader-container">
						<Circle />
					</div>
				{:else if games.length > 0}
					<tbody>
						{#each games as game}
							<tr>
								<td>
									<div class="flex justify-start items-center">
										{game.name}
										{#if game.twitch_channel}
											<a href={`https://www.twitch.tv/${game.twitch_channel}`}>
												<Icon icon="mdi:twitch" class="ml-2 twitch-icon" />
											</a>
										{/if}
									</div>
								</td>
								<td>{game.players.length}</td>
								<td>
									<button class="join-btn" on:click={() => goto(`/play/${game.pin}`)}>
										{game.pin}
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				{:else}
					<p>Currently no active vessels... Go conjure one!</p>
				{/if}
			</table>
		</div>
	</div>
</div>

<style lang="postcss">
	.loader-container {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100px;
	}

	.table-container {
		height: 400px;
		overflow-y: auto;
		overflow-x: hidden; /* Sometimes x-overflow pops up randomly when refreshing page :( */
	}

	.table-container::-webkit-scrollbar {
		width: 10px;
	}

	.table-container::-webkit-scrollbar-track {
		background: #f1f1f1;
	}

	.table-container::-webkit-scrollbar-thumb {
		background: #888;
	}

	.table-container::-webkit-scrollbar-thumb:hover {
		background: #555;
	}

	div :global(.twitch-icon):hover {
		color: #b9a3e3;
	}

	.font {
		@apply text-fontcolor text-4xl;
		font-family: theme(fontFamily.amatic);
	}

	td {
		text-align: left;
	}

	th,
	td {
		@apply px-4 py-2;
	}

	.join-btn:hover {
		@apply bg-accent rounded transition duration-200;
	}

	.join-btn {
		@apply border-1 p-1 rounded;
		width: 100%;
	}

	.refresh-button {
		@apply flex flex-grow justify-center items-center rounded-md text-lg lg:text-4xl;
		transition: all 0.2s ease-in-out;
		text-decoration: none;
	}

	.refresh-button:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.05);
	}
</style>
