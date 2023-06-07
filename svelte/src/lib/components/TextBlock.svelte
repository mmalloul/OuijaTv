<script lang="ts">
	import type { TextBlock } from "$lib/types/TextBlock";
	export let item: TextBlock;
</script>

<div class="flex flex-col">
	<h2>{item.title}</h2>

	<p>{item.text}</p>
</div>

<style lang="postcss">
	div {
		@apply text-fontcolor text-shadow-lg;
		font-family: theme(fontFamily.amatic);

		h2 {
			@apply text-3xl;
		}

		p {
			font-family: theme(fontFamily.eczar);
		}
	}
</style>
