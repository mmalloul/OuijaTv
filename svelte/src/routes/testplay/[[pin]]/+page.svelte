<script lang="ts">
	import BoardComponent from "$lib/components/BoardComponent.svelte";

	let boardComponent: BoardComponent;

	function onVoteLetter(event: any) {
		const letterId = event.detail.id;
		boardComponent.targetALetter(letterId);
	}
</script>

<BoardComponent bind:this={boardComponent} on:voteOnLetter={onVoteLetter} />
