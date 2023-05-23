<script lang="ts">
	import "virtual:windi.css";
	import "../style.scss";
	import Menu from "$lib/components/Menu.svelte";
	import { writable } from "svelte/store";
	import { setContext } from "svelte";

	setContext("isHost", writable(false));
</script>

<Menu />

<div class="grow">
	<slot />
</div>

<style windi:preflights:global windi:safelist:global></style>
