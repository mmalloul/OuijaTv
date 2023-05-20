<script lang="ts">
	import "virtual:windi.css";
	import "../style.scss";
	import Menu from "$lib/components/Menu.svelte";
	import LandingPage from "#lib/components/LandingPage/LandingPage.svelte";
</script>

<Menu />
<LandingPage />

<div class="grow">
	<slot />
</div>

<style windi:preflights:global windi:safelist:global></style>
