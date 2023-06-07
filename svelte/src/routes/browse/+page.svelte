<script lang="ts">
	import { env } from "$env/dynamic/public";
	import { onMount } from "svelte";

	let games: any[] = [];

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
	<table class="table-auto">
		<thead>
			<tr>
				<th>Game Name</th>
				<th>PIN</th>
			</tr>
		</thead>
		{#if games.length > 0}
			<tbody>
				{#each games as game}
					<tr>
						<td>{game.name}</td>
						<td>{game.pin}</td>
						<td><button class="bg-accent">Join</button></td>
					</tr>
				{/each}
			</tbody>
		{:else}
			<p>Currently no active vessels... Go conjure one!</p>
		{/if}
	</table>
</div>

<style lang="postcss">
	.font {
		@apply text-fontcolor text-4xl;
		font-family: theme(fontFamily.amatic);
	}
	.font th {
		@apply text-4xl;
	}

	.font td,
	.font p {
		@apply text-xl;
	}

	td {
		@apply px-4;
	}
</style>
