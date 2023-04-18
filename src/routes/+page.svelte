<script lang="ts">
    import { goto } from "$app/navigation";
</script>

<div>
    This is the main page.
</div>

<button on:click={() => goto("/profile")} class="bg-dark-400 text-white p-5">
    Go to profile page
</button>