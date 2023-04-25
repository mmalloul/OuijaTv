<script lang="ts">
	import { page } from "$app/stores";
	import { onMount } from "svelte";
	
    let status = "searching...";

    onMount(() => {
        const pin = $page.params.pin;
        const websocket = new WebSocket(`ws://localhost:8000/join?pin=${pin}`);
        websocket.onclose = () => status = "game not found";
        websocket.onmessage = () => status = "connected!";
    });
</script>

{status}