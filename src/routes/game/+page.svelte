<script lang="ts">
	import { env } from "$env/dynamic/public";
	import { onMount } from "svelte";
	import toast, { Toaster } from "svelte-french-toast";

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
			if (confirm("Do you want to restart the game?") === true) {
				websocket.send(JSON.stringify({ action: "restart_game" }));
				toast.success("Game has been restarted!", {
					position: "bottom-center",
					style: "border-radius: 200px; background: #333; color: #fff; f"
				});

				question = "";
			}
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
			<button type="submit" class="bg-indigo-800 text-white rounded-r-lg px-10 submit-button">
				Submit
			</button>
		</form>

		<h1><br /><br />{question}</h1>
	</div>
</div>
{#if isHost}
	<button on:click={restart} class="restart-button bg-red-600 text-white rounded-lg px-10">
		<p>Restart</p>
	</button>
{/if}

<Toaster />

<style lang="postcss">
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

	.submit-button,
	.restart-button {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		transition: all 0.2s ease-in-out;
	}

	.restart-button {
		position: absolute;
		bottom: 0;
		right: 0;
		margin: 0 1rem 1rem 0;
	}

	.restart-button:hover {
		@apply cursor-pointer bg-accent opacity-75;
		transform: scale(1.03);
	}

	.restart-button > p {
		transition: all 0.2s ease-in-out;
	}

	.restart-button:hover > p {
		transform: scale(1.02);
	}

	.submit-button:hover {
		@apply cursor-pointer bg-indigo-500 opacity-75;
		transform: scale(1.01);
	}
</style>
