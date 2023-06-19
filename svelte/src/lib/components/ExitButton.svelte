<script lang="ts">
	import Icon from "@iconify/svelte";
    export let onExit: (event?: MouseEvent) => Promise<void>;
</script>

<style lang="postcss">
	.back-to-menu {
		@apply font-amatic text-center text-fontcolor flex flex-1 flex-grow;
	}

	.back-to-menu a {
		@apply flex justify-center items-center px-2 rounded-md  text-lg lg: text-3xl;
		transition: all 0.2s ease-in-out;
		text-decoration: none;
	}

	.back-to-menu a:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}
</style>

<div class="back-to-menu">
	<a id="exit-button" on:click={onExit}>
		<Icon icon="formkit:arrowleft" />
		Exit
	</a>
</div>