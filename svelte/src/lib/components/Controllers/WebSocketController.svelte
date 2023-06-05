<script lang="ts">
	import { createEventDispatcher, onMount } from "svelte";

	let socket: WebSocket;
	const dispatch = createEventDispatcher();

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
						username: messageContents
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
</script>
