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

	onMount(() => {
		username = localStorage.getItem("username") || "";
	});

	function inputValid(name: string, code: string): boolean {
		let warnings = [];
		if (name.length === 0) {
			warnings.push("Enter a username!");
		} else if (name.length > username_max) {
			warnings.push("Username too long!");
		}

		if (code.length === 0) {
			warnings.push("Enter a roomcode!");
		} else if (!/^[a-zA-Z]{6}$/.test(roomCode)) {
			warnings.push("Enter a valid roomcode!");
		}

		warning = warnings.join("\n");

		return warnings.length === 0;
	}

	function joinRoom(code: string) {
		localStorage.setItem("username", username);
		playerType.set(PlayerType.Player);
		goto(`/testplay/${code}`);
	}
</script>

<div class="container">
	<div class="flex-container">
		<form class="column" on:submit|preventDefault>
			<label for="username">Username:</label><br />
			<input bind:value={username} type="text" id="username" name="username" />
			<br /><br />
			<label for="room-code">Room code:</label><br />
			<input bind:value={roomCode} type="text" id="room-code" name="room-code" />
			<br />
			<button
				class="custom-button"
				type="submit"
				on:click={() => joinRoom(roomCode)}
				disabled={!inputValid(username, roomCode)}>Join</button
			>
		</form>
		<div class="column input-warning">
			<p>{warning}</p>
		</div>
	</div>
</div>

<style lang="postcss">
	form * {
		margin-top: 20px;
	}

	form input {
		background-color: transparent;
		border: 1px solid white;
		padding-left: 10px;
	}

	.input-warning {
		display: flex;
		justify-content: center;
		align-items: center;
		white-space: pre-line;
	}

	.container {
		@apply text-fontcolor text-4xl;
		font-family: theme(fontFamily.amatic);
		position: absolute;
		top: 50%;
		left: 50%;
		max-width: 30%;
		transform: translate(-50%, -50%);
	}

	.flex-container {
		display: flex;
	}

	.column {
		flex: 1;
	}

	.custom-button {
		@apply text-fontcolor text-4xl;
		text-decoration: none;
		text-align: center;
		font-family: theme(fontFamily.amatic);
		padding: 0.75em;
		width: 100%;
		border: 1px solid white;
		transition: all 0.2s ease-in-out;
	}

	.custom-button:hover {
		@apply cursor-pointer bg-accent opacity-75;
		transform: scale(1.01);
	}
</style>
