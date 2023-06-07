<script lang="ts">
	import TextBlock from "$lib/components/TextBlock.svelte";
	import textBlocks from "$lib/text/contact-text";
</script>

<div class="page contact">
	<h1 class="text-6xl">Contact</h1>

	<div class="contact__container">
		<div class="contact__text">
			{#if textBlocks.length > 0}
				{#each textBlocks as item}
					<TextBlock {item} />
				{/each}
			{/if}
		</div>

		<form action="https://api.staticforms.xyz/submit" method="post">
			<input type="hidden" name="accessKey" value="9c782d83-04a7-44b6-90b9-6bd4435e137d" />

			<input type="hidden" name="redirectTo" value="http://www.ouija.tv" />
			<div class="field">
				<label class="label">Name</label>
				<div class="control">
					<input class="input" type="text" name="name" placeholder="Enter Your Name" required />
				</div>
			</div>
			<div class="field">
				<label class="label">Email</label>
				<div class="control">
					<input class="input" type="email" name="email" placeholder="Enter Your Email" required />
				</div>
			</div>
			<div class="field">
				<label class="label">Message</label>
				<div class="control">
					<textarea class="textarea" name="message" placeholder="Enter Your Message" required />
				</div>
			</div>

			<button class="button" type="submit">Submit</button>
		</form>
	</div>
</div>

<style lang="postcss">
	form {
		@apply flex flex-col items-center;
		gap: 24px;
	}

	label,
	button {
		@apply text-2xl;
	}

	.field {
		width: 100%;
	}

	.input,
	textarea,
	button {
		width: 100%;
		background-color: transparent;
		border: solid 1px theme(colors.fontcolor);
	}

	.input {
		height: 40px;
	}

	.textarea {
		min-height: 300px;
	}

	.button:hover {
		color: theme(colors.accent);
	}
	.contact {
		@apply text-fontcolor text-shadow-lg flex flex-col justify-center;
		font-family: theme(fontFamily.amatic);
		gap: 48px;
		margin-bottom: 80px;
	}

	.contact__container {
		gap: 24px;
		display: grid;
		grid-template-columns: 1fr;

		@screen md {
			grid-template-columns: 1fr 1fr;
		}
	}

	.contact__text {
		@apply flex flex-col;
		gap: 24px;
	}
</style>
