<script lang="ts">
	import { goto } from "$app/navigation";
	import { env } from "$env/dynamic/public";
	import WebSocketController from "$lib/components/controllers/WebSocketController.svelte";
	import Icon from "@iconify/svelte";
	import { onMount } from "svelte";

	let games: any[] = [];
	let websocket: WebSocketController;

	onMount(() => {
		fetchGames();
	});

	async function fetchGames() {
		fetch(`${env.PUBLIC_URL}/games`)
			.then((response) => response.json())
			.then((responseData) => {
				games = responseData;
			})
			.catch((error) => {
				console.error("Error:", error);
			});
	}
</script>

<div class="flex justify-center mt-8 font">
	<div class="overflow-x-auto">
		<table class="table-auto w-full">
			<thead>
				<tr>
					<th>Game Name</th>
					<th>PIN</th>
					<th>Players</th>
					<th>Action</th>
				</tr>
			</thead>
			{#if games.length > 0}
				<tbody>
					{#each games as game}
						<tr>
							<td>
								<div class="flex justify-center items-center">
									{game.name}
									{#if game.twitch_channel}
										<a href={`https://www.twitch.tv/${game.twitch_channel}`}>
											<Icon icon="mdi:twitch" class="ml-2 twitch-icon" />
										</a>
									{/if}
								</div>
							</td>
							<td>{game.pin}</td>
							<td>{game.players.length}</td>
							<td>
								<button on:click={() => goto(`/play/${game.pin}`)} class="join-btn"> Join </button>
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

<style lang="postcss">
	div :global(.twitch-icon):hover {
       color: #b9a3e3;
   }

	.font {
		@apply text-fontcolor text-4xl;
		font-family: theme(fontFamily.amatic);
	}

	td {
		@apply px-4;
	}

	table {
		@apply border-collapse border-2;
	}

	th,
	td {
		@apply px-4 py-2;
	}

	.join-btn {
		@apply px-4 py-2 rounded transition duration-200;
	}
</style>
