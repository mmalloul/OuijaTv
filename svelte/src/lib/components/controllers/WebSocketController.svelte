<script lang="ts">
	import { createEventDispatcher, onMount } from "svelte";

	let socket: WebSocket;
	const dispatch = createEventDispatcher();

	/**
	 * This websocket controller is initialized in the /play/[pin] svelte page. The websocket will be bound to a specific Player/hostcontroller.
	 * This controller handles all the events that are coming from the server, so that host- and playercontroller can handle their own functionalities.
	 * @param url the websocket url.
	 */
	export function initSocket(url: string) {
		socket = new WebSocket(url);

		socket.onmessage = ({ data }) => {
			const message = JSON.parse(data);
			const messageType = message["type"];
			const messageContents = message["content"];

			switch (messageType) {
				case "pin": {
					dispatch("pinReceived", {
						pin: messageContents
					});
					break;
				}
				case "joined": {
					dispatch("joinedReceived", {
						pid: messageContents.pid,
						username: messageContents.name
					});
					break;
				}
				case "vote": {
					dispatch("voteReceived", {
						votes: messageContents
					});
					break;
				}
				case "prompt":
					dispatch("promptReceived", {
						prompt: messageContents
					});
					break;
				case "restart":
					dispatch("restartReceived");
					break;
				case "winningVote":
					dispatch("winningVoteReceived", {
						winningVote: messageContents
					});
					break;
				case "word":
					dispatch("wordUpdateReceived", {
						word: messageContents
					});
					break;
				case "counter":
					dispatch("tickReceived", {
						tick: messageContents
					});
					break;
				case "quit":
					dispatch("playerQuit", {
						pid: messageContents
					});
					break;
				case "noVotes":
					dispatch("noVotesReceived");
					break;
				case "stopCountdown":
					dispatch("stopCountdownReceived");
					break;
				case "hostExit":
					dispatch("exitReceived");
					break;
				default: {
					break;
				}
			}
		};
	}

	export function sendVote(message: any) {
		if (socket) {
			socket.send(JSON.stringify(message));
		}
	}

	export function sendPrompt(prompt: any) {
		if (socket && socket.readyState === socket.OPEN) {
			socket.send(JSON.stringify(prompt));
		}
	}

	export function sendRestart() {
		if (socket) {
			socket.send(JSON.stringify({ type: "restart" }));
		}
	}

	export function broadcastWinningVote(winningVote: string) {
		if (socket) {
			socket.send(JSON.stringify({ type: "winningVote", content: winningVote }));
		}
	}

	export function closeSocket() {
		socket.close();
	}
</script>
