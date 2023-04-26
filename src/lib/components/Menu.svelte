<script>
	import menuItems from "$lib/types/MenuItems";
</script>

<nav>
	<div class="menu">
		{#each menuItems as item}
			<a class="menu__item" href={item.route} aria-label={item.name}>
				{item.name}
			</a>
		{/each}
	</div>
</nav>

<style lang="postcss">
	nav {
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: theme(colors.dark);
		color: white;
		font-family: theme(fontFamily.title);
		height: 80px;
	}

	.menu {
		display: flex;
		justify-content: space-around;
		max-width: 1440px;
		width: 100%;
		padding: 0 theme(spacing.padding.medium);
	}

	@media (min-width: 768px) {
		/* medium and up / desktop */
		.menu {
			padding: 0 theme(spacing.padding.large);
		}
	}
</style>
