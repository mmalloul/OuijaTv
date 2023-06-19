import { writable } from "svelte/store";

interface LobbyInfo {
	lobbyName: string;
	gameMode: string;
	gameDuration: number;
	twitchChannel?: string;
}

export const lobbyStore = writable<LobbyInfo>({
	lobbyName: "",
	gameMode: "",
	gameDuration: 15,
	twitchChannel: ""
});
