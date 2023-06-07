<script lang="ts">
	import type { Founder } from "$lib/types/Founder";
	export let founder: Founder;
</script>

<div class="card flex flex-col items-center">
	<img class="shadow-light-600" src={founder.portrait} alt="" />

	<h2 class="m-auto text-4xl text-center">{founder.name}</h2>

	<h3 class="m-auto text-xl text-center">{founder.studentNumber}</h3>
</div>

<style lang="postcss">
	.card {
		gap: 16px;
	}

	img {
		width: 200px;
		height: 200px;
		border-radius: 50%;
	}
</style>
