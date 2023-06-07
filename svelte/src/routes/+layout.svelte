<script lang="ts">
	import "virtual:windi.css";
	import "../style.scss";
	import Menu from "$lib/components/Menu.svelte";
	import { writable } from "svelte/store";
	import { setContext } from "svelte";
	import { PlayerType } from "$lib/types/PlayerType";
	import { Toaster } from "svelte-french-toast";
	import Footer from "$lib/components/Footer.svelte";

	setContext("playerType", writable(PlayerType.None));

	let showMenu = writable(true);
	setContext("showMenu", showMenu);
</script>

<div class:hide-component={!$showMenu}>
	<Menu />
</div>

<Toaster />

<main class="grow">
	<slot />
</main>

<Footer />

<style windi:preflights:global windi:safelist:global></style>
