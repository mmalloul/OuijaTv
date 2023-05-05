<script lang="ts">
	import { env } from "$env/dynamic/public";
	import { onMount } from "svelte";

	let websocket: WebSocket;
	let pin = "";
	let prompt = "";
	let messages: string[] = [];

	onMount(() => {
		websocket = new WebSocket(`${env.PUBLIC_WS_URL}/host`);
		websocket.onmessage = ({ data }) => {
			if (pin) {
				messages = [...messages, data];
			} else {
				pin = data;
			}
		};
	});

	function submit() {
		websocket.send(prompt);
		prompt = "";
	}
</script>

{#each messages as message}
	<div>{message}</div>
{/each}

<div class="page absolute-center flex gap-12 pb-5">
	<a href={pin} target="_blank" class="text-7xl text-center font-bold text-gray-700">
		{pin}
	</a>
	<form on:submit={submit} class="flex">
		<input
			bind:value={prompt}
			type="text"
			class="p-3 max-w-200 w-70vw border-dark-50 border rounded-l-lg"
		/>
		<button type="submit" class="bg-indigo-800 text-white rounded-r-lg px-10">Submit</button>
	</form>
</div>

<style lang="scss">
	.absolute-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}
</style>
