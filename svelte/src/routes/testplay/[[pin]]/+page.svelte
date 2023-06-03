<script lang="ts">
	import { goto } from "$app/navigation";
	import Board from "#lib/components/Board.svelte";
	import WebSocketController from "#lib/components/Controllers/WebSocketController.svelte";
	import { toast, Toaster } from "svelte-french-toast";
	import { getContext, onMount } from "svelte";
	import type { Writable } from "svelte/store";
	import { PlayerType } from "#lib/types/PlayerType";
	import { page } from "$app/stores";

	let prompt: string;
	let board: Board;
	let votes: object = {};
	let socketController: WebSocketController;
	const playerType: Writable<PlayerType> = getContext("playerType");

	$: pin = $page.params.pin;

	onMount ( () => {
		console.log($playerType)
		switch($playerType) {
			case PlayerType.Host:
				socketController.initSocketForHost();
			case PlayerType.Player:
				socketController.initSocketForPlayer($page.params.pin);
			default:
				gotoJoinPage();
				break;
		}
	})

	function onVoteLetter(event: any) {
		const letterId = event.detail.id;
		board.targetLetter(letterId);
	}

	function sendJoinedToast(event: any) {
		const username = event.detail.username;
		const message = `${username} has joined the game 👻!`;
		toast.success(message, {
			position: "bottom-center",
			style: "border-radius: 200px; background: #333; color: #fff; f"
		});
	}

	function onVoteReceived(event: any) {
		const allVotes = event.detail.votes
		votes = Object.assign({}, allVotes);
		board.targetLetter(board.getTargetLetter(votes))
	}

	function updatePrompt(event: any) {
		const newPrompt = event.detail.prompt; 
		prompt = newPrompt;
	}

	function joinGame() {
		goto(`/play/${pin}`)
	}

	function gotoJoinPage() {
		goto(`/join/${pin}`);
	}
</script>


<Board 
	bind:this={board} 
	on:letterClicked={onVoteLetter} 
/>
<WebSocketController
	on:joinedReceived={sendJoinedToast}
	on:voteReceived={onVoteReceived}
	on:promptReceived={updatePrompt}
	on:pinReceived={joinGame}
/>
<Toaster />

