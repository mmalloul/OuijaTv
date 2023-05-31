<script lang="ts">
	import BoardComponent from "#lib/components/Board.svelte";

	let boardComponent: BoardComponent;

	function onVoteLetter(event: any) {
		const letterId = event.detail.id;
		boardComponent.targetLetter(letterId);
	}
</script>

<BoardComponent bind:this={boardComponent} on:letterClicked={onVoteLetter} />
