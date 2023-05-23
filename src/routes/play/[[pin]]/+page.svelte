<script lang="ts">
	import { goto } from "$app/navigation";
	import { env } from "$env/dynamic/public";
	import BoardSvg from "$lib/components/BoardSVG.svelte";
	import { getContext, onMount } from "svelte";
	import { page } from "$app/stores";
	import type { Writable } from "svelte/store";

	const isHost: Writable<boolean> = getContext("isHost");
	let username: string;
	let socket: WebSocket;
	
	onMount(() => {
		username = localStorage.getItem("username") ?? "anonymous";
		
		if ($isHost) {
			socket = new WebSocket(`${env.PUBLIC_WS_URL}/host`);
			socket.onmessage = ({ data }) => {
				// pin
				goto(`play/${data}`);
				socket.onmessage = ({ data }) => {
					console.log(data);
				};
			};
		}
		else {
			
			const pin = $page.params.pin;
			if (!pin || !username) return;

			socket = new WebSocket(`${env.PUBLIC_WS_URL}/join?pin=${pin}&name=${username}`);
		}
	});

	let seekerX: number;
	let seekerY: number;
</script>

<div class="h-90vh flex flex-col items-center gap-5 pt-10">
	{#if $isHost}
		<form class="flex">
			<input type="text" placeholder="STATE YOUR INTENTION" />
		</form>
	{/if}

	<BoardSvg>
		{#if seekerX && seekerY}
			<circle id="Seeker" cx={seekerX} cy={seekerY} r="76.5" stroke="#FFF7E2" stroke-width="13" />
		{/if}
	</BoardSvg>
</div>

<style lang="postcss">
	input {
		@apply w-full mx-50 w-200 outline-0 text-center;
		font-family: theme(fontFamily.amatic);
		font-size: 3rem;
		color: rgba(255, 255, 255, 0.9);
		background-color: transparent;
	}
</style>
