<script lang="ts">
	import { User } from "$lib/types/User";
	import { onMount } from "svelte";
    import Profile from "$lib/components/Profile.svelte";

	export let user: User;

	onMount(async () => {
		user = await fetch("/api/user").then((res) => res.json());
	});
</script>

{#if user}
	<Profile {user}/>
{/if}
