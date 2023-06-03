<script lang="ts">
	import { createEventDispatcher, getContext } from "svelte";
	import { env } from "$env/dynamic/public";

	let socket: WebSocket;
	const dispatch = createEventDispatcher();

	function initSocketForHost() {
		socket = new WebSocket(`${env.PUBLIC_WS_URL}/host`);
		socket.onmessage = ({ data }) => {
			const message = JSON.parse(data);
			const messageType = message["type"];
			const messageContents = message["content"]; 
			switch (messageType) {
				case "pin": {
					dispatch('pinReceived', {
						pin: messageContents
					});
					break;
				}
				case "joined": {
					dispatch('joinedReceived', {
						username: messageContents
					});
					break;
				}
				case "vote": {
					dispatch('voteReceived', {
						votes: messageContents
					})
					break;
				}
				default: {
					break;
				}
			}
		};
	}

	function initSocketForPlayer(pin: string) {
		const username = localStorage.getItem("username") ?? "anonymous";
		socket = new WebSocket(`${env.PUBLIC_WS_URL}/join?pin=${pin}&username=${username}`);
		socket.onmessage = ({ data }) => {
			const message = JSON.parse(data);
			const messageType = message["type"];
			const messageContents = message["content"]; 
			switch (messageType) {
				case "prompt":
					dispatch('promptReceived', {
						vote: messageContents
					})
					break;
				default:
					break;
			}
		};
	}
</script>
