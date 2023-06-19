<script lang="ts">
	import Icon from "@iconify/svelte";

	export let options: string[] = [];
	export let selection = "";

	let selectionOpen = false;

	function select(option: string) {
		selection = option;
		selectionOpen = false;
	}

	function toggleSelection() {
		selectionOpen = !selectionOpen;
	}

	function getParentWidth() {
		return document.getElementById("dropdown-wrapper")?.offsetWidth;
	}
</script>

<div id="dropdown-wrapper">
	<div id="dropdown-box">
		<button type="button" on:click={() => toggleSelection()}>
			<p>
				{selection}
			</p>
			<div class="icon">
				<Icon icon="material-symbols:arrow-drop-down-rounded" width="32" />
			</div>
		</button>
	</div>
	{#if selectionOpen}
		<div id="dropdown-contents" style="width: {getParentWidth()}px">
			{#each options as option, i}
				<button
					type="button"
					on:click={() => select(option)}
					class={option == selection ? "selected" : ""}>{option}</button
				>
				{#if i !== options.length - 1}
					<hr />
				{/if}
			{/each}
		</div>
	{/if}
</div>

<style lang="postcss">
	#dropdown-wrapper {
		@apply text-fontcolor text-4xl;
		font-family: theme(fontFamily.amatic);
		position: relative;
	}

	#dropdown-box {
		@apply flex w-inherit p-4 border-1 border-fontcolor rounded-xl;
	}

	#dropdown-box button {
		@apply flex flex-row w-full;
	}

	#dropdown-box button p {
		@apply ml-auto;
	}

	.icon {
		@apply ml-auto mr-0;
	}

	#dropdown-contents {
		@apply absolute justify-center items-center flex flex-col border-1 border-fontcolor rounded-xl bg-stone-900;
	}

	#dropdown-contents button {
		@apply p-2 w-full rounded-xl;
	}

	hr {
		@apply w-full border-1 border-fontcolor;
	}

	.selected {
		@apply bg-stone-700;
	}

	#dropdown-contents button:hover {
		@apply bg-stone-600;
	}
</style>
