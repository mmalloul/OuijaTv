<script lang="ts">
	import { PlayerType } from "$lib/types/PlayerType";
	import { goto } from "$app/navigation";
	import { page } from "$app/stores";
	import { getContext, onMount } from "svelte";
	import type { Writable } from "svelte/store";
	import Icon from "@iconify/svelte";

	const username_max = 18;
	const playerType = getContext<Writable<PlayerType>>("playerType");

	let username = "";
	let roomCode = $page.params.pin ?? "";

	let validRoomCode = false;
	let validUsername = false;

	onMount(() => {
		username = localStorage.getItem("username") || "";
		validateName();
		validateRoomCode();
	});

	function validateName() {
		validUsername = username.length != 0 && username.length < username_max;
	}

	function validateRoomCode() {
		validRoomCode = /^[a-zA-Z]{6}$/.test(roomCode);
	}

	function joinRoom(code: string) {
		localStorage.setItem("username", username);
		playerType.set(PlayerType.Player);
		goto(`/play/${code}`);
	}

	function exit() {
		goto("/");
	}
</script>

<div class="page container">
	<div class="panel">
		<form on:submit|preventDefault class="join-form">
			<div class="flex flex-col gap-2 w-full relative">
				<label for="username">Username:</label>

				<button id="close-button" class="close-button" on:click={() => exit()}
					><Icon icon="zondicons:close-outline" /></button
				>

				<span class:invisible={validUsername} class="error-message">
					Your username is too long! (Max. 16 characters)
				</span>

				<input
					bind:value={username}
					on:input={validateName}
					type="text"
					id="username"
					name="username"
				/>
			</div>

			<div class="flex flex-col gap-2 w-full">
				<label for="username">Roomcode:</label>

				<span class:invisible={validRoomCode} class="error-message">
					Please enter a valid roomcode! (6 characters)
				</span>

				<input
					bind:value={roomCode}
					on:input={validateRoomCode}
					type="text"
					id="room-code"
					name="room-code"
				/>
			</div>

			<div class="flex gap-2">
				<button
					class="big-button"
					type="submit"
					on:click={() => joinRoom(roomCode)}
					disabled={!validUsername || !validRoomCode}
					>Join
				</button>
			</div>
		</form>
	</div>
</div>

<style lang="postcss">
	.container {
		@apply flex flex-col items-center md: justify-center;
	}

	.panel {
		@apply flex flex-col items-center justify-center font-amatic text-fontcolor text-center w-full text-lg mt-15  md: mt-0 md:text-4xl md:p-4;
		max-width: 500px;
	}

	input {
		@apply w-full;
	}

	.join-form {
		@apply flex flex-col items-center w-full gap-2 md:gap-4 md:p-4;
	}

	.font {
		@apply text-fontcolor text-4xl font-amatic;
	}

	.error-message {
		@apply !text-red-500 text-lg md:text-2xl;
	}

	.close-button {
		@apply text-fontcolor absolute top-0 right-0 text-lg md:text-4xl;
		text-decoration: none;
		transition: all 0.2s ease-in-out;
	}

	.close-button:hover {
		@apply text-accent;
	}
</style>
