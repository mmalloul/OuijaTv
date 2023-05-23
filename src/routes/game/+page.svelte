<script lang="ts">
	import { env } from "$env/dynamic/public";
	import { onMount } from "svelte";

	let websocket: WebSocket;
	let pin = "";
	let input = "";
	let question = "";
	let messages: string[] = [];
	let isHost = false;

	onMount(() => {
		websocket = new WebSocket(`${env.PUBLIC_WS_URL}/host`);
		websocket.onmessage = ({ data }) => {
			if (pin) {
				messages = [...messages, data];
			} else {
				pin = data;
				isHost = true;
			}
		};
	});

	function submit() {
		websocket.send(input);
		question = input;
		input = "";
	}

	function restart() {		
		if (isHost) {
			if (confirm("Do you want to restart the game?") == true)
				websocket.send(JSON.stringify({ action: 'restart_game' }));
				question = ""
		}
	}
</script>

<div class="page absolute-center flex gap-12 pb-5">
	<div>
		<a href="game/{pin}" target="_blank" class="text-7xl text-center font-bold text-gray-700">
			{pin}
		</a>
		<form on:submit={submit} class="flex">
			<input
				bind:value={input}
				type="text"
				class="p-3 max-w-200 w-70vw border-dark-50 border rounded-l-lg"
			/>
			<button type="submit" class="bg-indigo-800 text-white rounded-r-lg px-10">Submit</button>
		</form>
		{#if isHost}
			<button on:click={restart} class="bg-red-600 text-white rounded-lg px-10">Restart</button>
		{/if}
		<h1><br /><br />{question}</h1>
	</div>
</div>

<style lang="scss">
	p,
	h1 {
		color: white;
	}

	.absolute-center {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
	}
</style>
