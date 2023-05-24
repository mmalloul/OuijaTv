import { render, fireEvent, screen } from "@testing-library/svelte";
import LobbyCreationPanel from "$lib/components/LandingPage/LobbyCreationPanel.svelte";

describe("Test LobbyCreationPanel.svelte", async () => {
	test("Lobby name input is empty when rendered", async () => {
		// Arrange
		render(LobbyCreationPanel, { showLobbyCreationPanel: true });

		// Act
		const input = await screen.getByLabelText("Name your vessel:", { selector: "input" });

		// Assert
		expect(input).toHaveValue("");
	});

	test("Lobby name input changes value", async () => {
		// Arrange
		render(LobbyCreationPanel, { showLobbyCreationPanel: true });

		// Act
		const input = await screen.getByLabelText("Name your vessel:", { selector: "input" });
		await fireEvent.change(input, { target: { value: "Test" } });

		// Assert
		expect(input).toHaveValue("Test");
	});
});
