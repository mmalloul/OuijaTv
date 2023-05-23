import { render, fireEvent, screen } from "@testing-library/svelte";
import LobbyCreationPanel from "../components/LandingPage/LobbyCreationPanel.svelte";

describe("Test LobbyCreationPanel.svelte", async () => {
	test("Lobby name input is empty when rendered", async () => {
		render(LobbyCreationPanel, { showLobbyCreationPanel: true });

		const input = await screen.getByLabelText("Name of lobby:", { selector: "input" });
		// const lobbyName = await screen.getByText("Name of lobby: ");

		// const lobbyNameInput = screen.getByText("Create")

		expect(input).toHaveValue("");
	});
});
