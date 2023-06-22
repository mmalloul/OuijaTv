<script lang="ts">
	export let onExit: (event?: MouseEvent) => Promise<void>;
	import { goto } from "$app/navigation";
	import Icon from "@iconify/svelte";

	const exitButtonClick = async (event?: MouseEvent) => {
		if (onExit) {
			await onExit(event);
		}
	};
</script>

<div class="back-to-menu">
	<a id="exit-button" on:click|preventDefault={exitButtonClick}>
		<Icon icon="formkit:arrowleft" />
		Exit
	</a>
</div>

<style lang="postcss">
	.back-to-menu {
		@apply font-amatic text-center text-fontcolor flex flex-1 flex-grow;
	}

	#exit-button {
		@apply flex justify-center items-center rounded-md  text-lg lg:text-3xl;
		transition: all 0.2s ease-in-out;
		text-decoration: none;
	}

	.back-to-menu a:hover {
		@apply cursor-pointer bg-accent;
		transform: scale(1.03);
	}
</style>
