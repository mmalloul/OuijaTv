<script lang="ts">
	import "virtual:windi.css";
	import "../style.scss";
	import Menu from "$lib/components/Menu.svelte";
	import { writable } from "svelte/store";
	import { setContext } from "svelte";
	import { PlayerState } from "#lib/types/PlayerState";

	setContext("playerState", writable(PlayerState.None));
</script>

<Menu />

<div class="grow">
	<slot />
</div>

<style windi:preflights:global windi:safelist:global></style>
