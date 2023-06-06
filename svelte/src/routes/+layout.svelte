<script lang="ts">
	import "virtual:windi.css";
	import "../style.scss";
	import Menu from "$lib/components/Menu.svelte";
	import { writable } from "svelte/store";
	import { setContext } from "svelte";
	import { PlayerType } from "#lib/types/PlayerType";
	import { Toaster } from "svelte-french-toast";

	setContext("playerType", writable(PlayerType.None));
</script>

<Menu />
<Toaster />

<main class="grow">
	<slot />
</main>

<style windi:preflights:global windi:safelist:global></style>
