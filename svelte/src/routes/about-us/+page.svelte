<script lang="ts">
	import FounderCard from "$lib/components/founder-card.svelte";
	import TextBlock from "$lib/components/TextBlock.svelte";
	import textBlocks from "$lib/text/aboutus-text";
	import founders from "$lib/types/Founder";
</script>

<div class="page aboutus flex flex-col justify-center">
	<h1 class="text-6xl">About Us</h1>

	{#if textBlocks.length > 0}
		{#each textBlocks as item}
			<TextBlock {item} />
		{/each}
	{/if}

	<h1 class="text-6xl">Founders</h1>

	<div class="aboutus__founders">
		{#each founders as founder}
			<FounderCard {founder} />
		{/each}
	</div>
</div>

<style lang="postcss">
	.aboutus {
		@apply text-fontcolor text-shadow-lg;
		font-family: theme(fontFamily.amatic);
		gap: 24px;
		margin-bottom: 80px;
	}

	.aboutus__founders {
		display: grid;
		gap: 60px;

		@screen lg {
			grid-template-row: 1fr;
			grid-template-columns: repeat(5, 1fr);
		}

		@screen @md {
			grid-template-row: 1fr;
			grid-template-columns: repeat(3, 1fr);
		}

		@screen <md {
			grid-template-row: 1fr;
			grid-template-columns: repeat(1, 1fr);
		}
	}
</style>
