<script lang="ts">
	import { page } from "$app/stores";
	import { onMount } from "svelte";

	let status = "";
	let messages: string[] = [];

	onMount(() => {
		const pin = $page.params.pin;
		const websocket = new WebSocket(`ws://localhost:8000/join?pin=${pin}`);
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
