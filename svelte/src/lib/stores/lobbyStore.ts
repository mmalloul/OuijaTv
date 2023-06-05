import { writable } from "svelte/store";

interface LobbyInfo {
  lobbyName: string;
  gameDuration: number;
}

export const lobbyStore = writable<LobbyInfo>({
  lobbyName: "",
  gameDuration: 15,
});