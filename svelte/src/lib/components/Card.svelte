<script lang="ts">
	export let spirit: string;
	export let name: string;
	export let backgroundImage: string;
	export let tag: string;
	export let lore: string;
	export let goToQuestion: (spirit: number, name: string, tags: string) => void;

	function handleClick() {
		let numberSprit = parseInt(spirit);
		goToQuestion(numberSprit, name, tag);
	}
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === "Enter" || event.key === " ") {
			const numberSprit = parseInt(spirit);
			goToQuestion(numberSprit, name, tag);
		}
	}
</script>

<div class="b-game-card" on:click={handleClick} on:keydown={handleKeyDown} tabindex="0">
	<div
		class="b-game-card__cover relative rounded-[50px]"
		style={`background-image: url(${backgroundImage});`}
	>
		<div class="bg-dark bg-opacity-50 py-2 rounded-t-xl">
			<div class="name font-medieval">{name}</div>
			<div class="tag">{tag}</div>
		</div>
		<div class="b-game-card__lore">{lore}</div>
	</div>
</div>

<style lang="postcss">
	.b-game-card__lore {
		@apply text-accent bg-dark;
		display: none; /* hide the lore text initially */
		position: absolute;
		bottom: 0;
		left: 0;
		width: 100%;
		/* background: co; */
		padding: 10px;
		font-size: 14px;
		line-height: 1.5;
		text-align: center;
		transform: translateY(100%);
		transition: transform 0.35s ease-in-out;
	}
	.b-game-card:hover .b-game-card__cover {
		transform: rotateX(7deg) translateY(-6px);
		&::after {
			transform: translateY(0%);
		}
	}

	.b-game-card:hover .b-game-card__lore {
		display: block; /* show the lore text on hover */
		transform: translateY(0%);
	}
	.b-game-card {
		cursor: pointer;
		position: relative;
		z-index: 1;
		width: 100%;
		padding-bottom: 150%;

		.name {
			font-size: xx-large;
			font-weight: bold;
			color: rgb(252, 252, 252);
			text-align: center;
		}

		.tag {
			text-align: center;
			margin: 0 50px 5px 50px;
			width: auto;
			color: black;
			font-size: large;
			font-weight: bold;
			@apply text-fontcolor;
			font-family: theme(fontFamily.amatic);
		}
		&__cover {
			position: absolute;
			z-index: 1;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			overflow: hidden;
			background-image: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
			background-size: cover;
			perspective-origin: 40% 50%;
			transform-style: preserve-3d;
			transform-origin: top center;
			will-change: transform;
			transform: skewX(0.001deg);
			transition: transform 0.35s ease-in-out;
			// Gloss
			&::after {
				display: block;
				content: "";
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 120%;
				transform: translateY(-20%);
				will-change: transform;
				transition: transform 0.65s cubic-bezier(0.18, 0.9, 0.58, 1);
			}
		}
		&:hover &__cover {
			transform: rotateX(7deg) translateY(-6px);

			&::after {
				transform: translateY(0%);
			}
		}
	}
</style>
