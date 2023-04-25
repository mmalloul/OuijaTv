<script lang="ts">
	import { onMount } from "svelte";

	let pin = "";
	let messages: string[] = [];

	onMount(() => {
		const websocket = new WebSocket("ws://localhost:8000/host");
		websocket.onmessage = ({ data }) => {
			if (pin) {
				messages = [...messages, data];
			} else {
				pin = data;
			}
		};
	});
</script>

{#each messages as message}
	<div>{message}</div>
{/each}

<a
	href={pin}
	target="_blank"
	class="text-7xl font-bold text-center text-gray-700 pb-18 absolute-center"
>
	{pin}
</a>

<style lang="scss">
	.absolute-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}
</style>
