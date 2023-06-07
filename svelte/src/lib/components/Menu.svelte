<script lang="ts">
	import menuItems from "$lib/types/MenuItems";
	import { page } from "$app/stores";
</script>

<nav>
	<div class="menu">
		<input class="" type="checkbox" id="menu__toggle" />
		<label for="menu__toggle" class="menu__button">&#9776;</label>
		<ul class="menu__list">
			{#each menuItems as item}
				<li>
					<a
						class="menu__item"
						href={item.route}
						aria-label={item.name}
						class:active={$page.url.pathname == item.route}
						class:opacity-50={!item.route}
					>
						{item.name}
					</a>
				</li>
			{/each}
		</ul>
	</div>
</nav>

<style lang="postcss">
	nav {
		@apply flex md: justify-center;
	}

	.menu {
		@apply w-full p-4 max-w-screen-2xl md: p-6;
	}

	.menu__button {
		@apply block cursor-pointer text-4xl text-fontcolor md: hidden;
	}

	.menu__list {
		@apply list-none m-0 p-0 flex justify-between hidden md:flex;
	}

	.menu__list li {
		@apply block md:inline-block;
	}

	.menu__list li a:hover,
	.menu__button:hover {
		@apply text-accent;
	}

	.active {
		@apply text-accent !important;
	}

	.menu__list li a {
		@apply block text-fontcolor text-shadow-lg text-xl md:text-3xl
		text-decoration: none;
		font-family: theme(fontFamily.amatic);
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

		#menu__toggle:checked ~ .menu__list {
			@apply block;
		}

		#menu__toggle:checked ~ .menu__button {
			@apply text-accent;
		}
	}
</style>
