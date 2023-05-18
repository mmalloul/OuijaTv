<script>
	import menuItems from "$lib/types/MenuItems";
</script>

<nav>
	<div class="menu">
		<input class="" type="checkbox" id="menu-toggle" />
		<label for="menu-toggle" class="menu-button">&#9776;</label>
		<ul class="menu__list">
			{#each menuItems as item}
				<li>
					<a class="menu__item" href={item.route} aria-label={item.name}>
						{item.name}
					</a>
				</li>
			{/each}
		</ul>
	</div>
</nav>

<style lang="postcss">
	nav {
		@apply flex justify-start bg-dark text-fontcolor md: justify-center;
	}

	.menu {
		@apply w-full p-4 md: p-6;
		max-width: 1440px;
	}

	.menu-button {
		@apply block cursor-pointer text-4xl md: hidden;
	}

	.menu__list {
		@apply list-none m-0 p-0 flex justify-around hidden md:flex;
	}

	.menu__list li {
		@apply block md:inline-block;
	}

	.menu__list li a {
		@apply block text-fontcolor text-xl md:text-3xl
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
	}

	#menu-toogle {
		@apply text-fontcolor;
	}

	/* hides checkbox */
	input[type="checkbox"] {
		opacity: 0;
		position: absolute;
		left: -100rem;
		top: -100rem;
	}

	@screen <sm {
		.menu__list li {
			border-bottom: 1px solid #ddd;
		}

		.menu__list li a {
			padding: 10px 0;
		}

		#menu-toggle:checked ~ .menu__list {
			@apply block;
		}
	}
</style>
