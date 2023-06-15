<script lang="ts">
	import { PlayerType } from "$lib/types/PlayerType";
	import { goto } from "$app/navigation";
	import { page } from "$app/stores";
	import { getContext, onMount } from "svelte";
	import type { Writable } from "svelte/store";

	const username_max = 18;
	const playerType = getContext<Writable<PlayerType>>("playerType");

	let warning = "";
	let username = "";
	let roomCode = $page.params.pin ?? "";

	let validRoomCode: boolean = false;
	let validUsername: boolean = false;

	onMount(() => {
		username = localStorage.getItem("username") || "";
		validateName();
		validateRoomCode();
	});

	function validateName() {
		validUsername = username.length < username_max;
	}

	function validateRoomCode() {
		validRoomCode = /^[a-zA-Z]{6}$/.test(roomCode);
	}

	function joinRoom(code: string) {
		localStorage.setItem("username", username);
		playerType.set(PlayerType.Player);
		goto(`/play/${code}`);
	}
</script>

<div class="grow font flex justify-center py-32">
	<form on:submit|preventDefault class="flex flex-col items-center">
		<label class="mb-2" for="username">Username:</label>
		<input class="mb-4" bind:value={username} on:input={validateName} type="text" id="username" name="username" />
		<div class="h-4 mb-8 font--error">
			{ validUsername ? "" : "Your username is too long! (Max. 16 characters)" }
		</div>
		<label class="mb-2" for="username">Roomcode:</label>
		<input class="mb-4" bind:value={roomCode} on:input={validateRoomCode} type="text" id="room-code" name="room-code" />
		<div class="h-4 mb-8 font--error">
			{ validRoomCode ? "" : "Please enter a valid roomcode! (6 characters)" }
		</div>
		<button
			class="mt-4 px-4 py-2 rounded-md font-bold border-2 border-fontcolor disabled:opacity-30 enabled:bg-white/10 hover:bg-accent active:bg-accent/75"
			type="submit"
			on:click={() => joinRoom(roomCode)}
			disabled={!validUsername || !validRoomCode}>Join
		</button
		>
	</form>
</div>

<style lang="postcss">
	.font {
		@apply text-fontcolor text-4xl;
		font-family: theme(fontFamily.amatic);
	}

	.font--error {
		@apply text-2xl !text-red-500;
	}

	input {
		@apply text-fontcolor bg-white bg-opacity-5 text-4xl border-1 border-light-300 p-3;
	}
</style>
