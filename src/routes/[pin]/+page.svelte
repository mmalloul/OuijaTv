<script lang="ts">
	import { page } from "$app/stores";
	import { onMount } from "svelte";
	import { env } from "$env/static/public";

	let status = "";
	let messages: string[] = [];

	onMount(() => {
		const pin = $page.params.pin;
		const websocket = new WebSocket(`${env.WS_URL}/join?pin=${pin}`);
		websocket.onclose = () => (status = "game not found");
		websocket.onmessage = ({ data }) => {
			if (status) {
				messages = [...messages, data];
			} else {
				status = "connected!";
			}
		};
	});
</script>

{#each messages as message}
	<div>{message}</div>
{/each}

{status}
