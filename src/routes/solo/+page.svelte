<script lang="ts">
	import { quintOut } from "svelte/easing";
	import { crossfade } from "svelte/transition";
	import { flip } from "svelte/animate";

	const [send, receive] = crossfade({
		fallback(node, params) {
			const style = getComputedStyle(node);
			const transform = style.transform === "none" ? "" : style.transform;

			return {
				duration: 600,
				easing: quintOut,
				css: (t) => `
				transform: ${transform} scale(${t});
				opacity: ${t}`
			};
		}
	});
	let traits = [
		{ id: 1, done: false, description: "Funny" },
		{ id: 2, done: false, description: "Scary" },
		{ id: 3, done: false, description: "Friendly" },
		{ id: 4, done: false, description: "Dark" },
		{ id: 5, done: false, description: "Clever" }
	];

	// TODO api request needs to be made here
	let awnser = "";
	let question = "";
	function openAiCall() {
		const selectedTraits = traits.filter((t) => t.done).map((t) => t.description);
		const selectedTraitsString = selectedTraits.join(", ");

		console.log(selectedTraitsString);
		console.log(question);
		// return response
	}

let visible = false;

function toggleVissible() {
	visible = !visible
	const button = document.querySelector('.toggle-button');
  if (visible) {
    button.textContent = 'Close';
    document.querySelector('.absolute-center').style.top = '75%';
  } else {
    button.textContent = 'Open';
    document.querySelector('.absolute-center').style.top = '50%';
  }
}
</script>

<div class="board">
	<div>
		<h2><b>SOLO Summon</b></h2>
		<br />To select traits for the Ouija spirit, you can choose from a list of pre-defined traits
		hat are relevant to the spirit you want to communicate with. The traits can be selected by
		clicking on the corresponding checkboxes next to each trait. Once you have selected the desired
		traits, you can click on the "summnon" button to start the communication with the spirit.
		<button class="toggle-button bg-indigo-800 text-white rounded-r-lg px-10" on:click={toggleVissible}>
			open
		</button>
	</div>


	{#if visible}

	<div class="left">
		<h2>Traits</h2>
		{#each traits.filter((t) => !t.done) as todo (todo.id)}
			<label in:receive={{ key: todo.id }} out:send={{ key: todo.id }} animate:flip>
				<input type="checkbox" bind:checked={todo.done} />
				{todo.description}
			</label>
		{/each}
	</div>

	<div class="right">
		<h2>Added</h2>
		{#each traits.filter((t) => t.done) as todo (todo.id)}
			<label in:receive={{ key: todo.id }} out:send={{ key: todo.id }} animate:flip>
				<input type="checkbox" bind:checked={todo.done} />
				{todo.description}
			</label>
		{/each}
	</div>
	{/if}
</div>

<div class="absolute-center flex flex-col gap-12 pb-5">
	<form on:submit={openAiCall} class="flex">
		<input
			type="text"
			class="p-3 max-w-200 w-70vw border-dark-50 border rounded-l-lg"
			bind:value={question}
			placeholder="Enter your question here"
		/>

		<button type="submit" class="bg-indigo-800 text-white rounded-r-lg px-10">Summon</button>
	</form>

	<div>Awnser comes here</div>
</div>

<style lang="scss">
	.absolute-center {
		position: absolute;
		top: 75%;
		left: 50%;
		transform: translate(-50%, -50%);
	}

	.board {
		max-width: 55em;
		margin: 0 auto;
	}

	.left,
	.right {
		float: left;
		width: 50%;
		padding: 0 1em 0 0;
		box-sizing: border-box;
	}

	h2 {
		font-size: 2em;
		font-weight: 200;
		user-select: none;
	}

	label {
		top: 0;
		left: 0;
		display: block;
		font-size: 1em;
		line-height: 1;
		padding: 0.5em;
		margin: 0 auto 0.5em auto;
		border-radius: 2px;
		background-color: #eee;
		user-select: none;
	}

	input {
		margin: 0;
	}

	.right label {
		background-color: rgb(180, 240, 100);
	}


</style>
