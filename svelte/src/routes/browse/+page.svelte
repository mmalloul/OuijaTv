<script lang="ts">
	import { env } from "$env/dynamic/public";
	import { onMount } from "svelte";

	let games: any[] = [];

	onMount(() => {
		fetchGames();
	});

	async function fetchGames() {
		fetch(`${env.PUBLIC_API_URL}/games`)
			.then((response) => response.json())
			.then((responseData) => {
				games = responseData;
				console.log(games);
			})
			.catch((error) => {
				console.error("Error:", error);
			});
	}
</script>

<table>
	<thead>
		<tr>
			<th>Game Name</th>
			<th>PIN</th>
			<th>Join Button</th>
		</tr>
	</thead>
	<tbody>
		{#each games as game}
            <tr>
                <td>{game.name}</td>
                <td>{game.pin}</td>
                <button>hallo</button>
            </tr>
		{/each}

	</tbody>
</table>
