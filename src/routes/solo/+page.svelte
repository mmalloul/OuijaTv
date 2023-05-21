<script lang="ts">
  import { env } from "$env/dynamic/public";
  import { onMount } from 'svelte';
  import { Wave } from 'svelte-loading-spinners';
  import toast, { Toaster } from 'svelte-french-toast';
  import BoardSvg from "$lib/components/BoardSVG.svelte";

  let hideCards = true, hideQuestion = false,hideBoard = false, hideLoader = false;
  let question = "",circleStyle = "" ,awnser="";
  const letterPositions: Record<string, Vector2> = {};
  let seekerX = 0,seekerY = 0, spirit = 0;

  function goToQuestion(s: number) {
    spirit = s;
    hideCards = false;
    hideQuestion = true;
  }

  async function askQuestion() {
    if (question == '') {
      toast('Just tell me what you want to ask and dont waste my time.', {
        icon: '👻',
        style: 'border-radius: 200px; background: #333; color: #fff;',
        duration: "600",
      });
      return;
    }
    hideLoader = true;
    console.log(question);
    console.log(spirit);
    //TODO function call python api
    callOpenAI (question,spirit);


    hideQuestion = false;
    update();
  }

  async function callOpenAI(prompt: string, spirit: number) {
  try {
    const url = env.PUBLIC_URL +"/openai?prompt=" + encodeURIComponent(prompt) + "&spirit=" + encodeURIComponent(spirit);

    const response = await fetch(url);
    const data = await response.json();
    
    let awnser1 = data.response;
    awnser = awnser1.replace(".", "");
    
  } catch (error) {
    console.error("Error:", error);
  }
}

  let elapsed = 0;
  let timeTillLoad = 2;
  function update() {
    if (elapsed < timeTillLoad) {
      elapsed++;
      setTimeout(update, 1000);
    } else {
      hideLoader = false;
      hideBoard = true;
      loadLetterPositions();
      // delay for reading in variables from the svg
      setTimeout(() => {
        loadLetterPositions();
      }, 1000);
      printAnswer(awnser);
    }
  }

  async function printAnswer(word: string) {
    const split = word.split('');
    for (let i = 0; i < split.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 2000));
      targetALetter(split[i]);
    }
    await new Promise(resolve => setTimeout(resolve, 2000));
    // go to goodbye on board
    seekerX = 960.5
    seekerY = 766.5
    return;
  }

  function targetALetter(letter: string) {
    var target = letterPositions[letter.toUpperCase()];
    seekerX = target.x;
    seekerY = target.y;
    circleStyle = `transition: cx 0.5s ease-in-out, cy 0.5s ease-in-out`;
  }

  function loadLetterPositions() {
    const circleElements = document.querySelectorAll<SVGCircleElement>("circle");
    circleElements.forEach((element) => {
      const id = element.id;
      let x = element.attributes.getNamedItem("cx")?.value;
      let y = element.attributes.getNamedItem("cy")?.value;

      if (x && y) {
        letterPositions[id.charAt(id.length - 1)] = new Vector2(parseFloat(x), parseFloat(y));
      }
    });
  }

  class Vector2 {
    constructor(public x: number, public y: number) { }
  }

  onMount(() => {
    // Remove the transition property after the animation completes
    setTimeout(() => {
      circleStyle = '';
    }, 500);
  });
</script>
<Toaster />

{#if hideBoard}
<div class="awnser" > 
	<BoardSvg>
		<circle id="Seeker" style={circleStyle}  cx={seekerX} cy={seekerY} r="76.5" stroke="#FFF7E2" stroke-width="13" />
	</BoardSvg>
</div>
{/if}

<div class="page">
{#if hideCards}
<div>    
    <h1 class="awnser">SOLO Summon</h1>  
    <div class="subtask">
        As you navigate to the website and click on the Ouija board feature, a sense of apprehension washes over you. You know that this virtual board may not be as innocuous as it seems, and that you could be inviting something dark and powerful into your life. Select the dark spirit that you desire and use him by <b>clicking</b> on the card.
    </div>
</div>
<div class="l-container">
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="b-game-card" on:click={() => goToQuestion(1)}>
        <div class="b-game-card__cover" style="background-image: url(https://cdn.leonardo.ai/users/e3cbfcf7-71a9-4b95-a419-a8930e080950/generations/35c035f9-7ed5-4be4-a8c2-442df7edc5ca/variations/Default_full_body_portrait_of_beautiful_female_1900s_gangster_1_35c035f9-7ed5-4be4-a8c2-442df7edc5ca_1.jpg);">
            <div class="name">Sgt. Sabrina</div>
            <div class="tag">Friendly, Scary</div>
            <div class="b-game-card__lore">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Optio omnis aperiam excepturi modi rem hic incidunt quibusdam, esse commodi, laboriosam velit nulla cupiditate? Aliquam, repellendus beatae. Distinctio asperiores facere nihil nisi quos fugiat aperiam culpa mollitia, sed provident labore animi commodi? Aliquid, quidem sint impedit mollitia ipsum quisquam eius. Asperiores sapiente eum ratione voluptates. Expedita cumque optio rerum autem commodi dolore inventore illo beatae ipsa sapiente, culpa delectus iste quidem?</div> <!-- new element for lore text -->
        </div>
    </div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="b-game-card" on:click={() => goToQuestion(2)}>
        <div class="b-game-card__cover" style="background-image: url(https://cdn.leonardo.ai/users/ab0ec8a3-c208-42ee-9152-5a58cff9f0c8/generations/7a51da1e-94d3-4c7c-a8ed-89a89f9f5a9c/variations/Default_black_and_white_A_masked_samurai_warrior_standing_on_a_1_7a51da1e-94d3-4c7c-a8ed-89a89f9f5a9c_1.jpg);">
            <div class="name">Asta </div>
            <div class="tag">Clever, funny</div>
            <div class="b-game-card__lore">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Optio omnis aperiam excepturi modi rem hic incidunt quibusdam, esse commodi, laboriosam velit nulla cupiditate? Aliquam, repellendus beatae. Distinctio asperiores facere nihil nisi quos fugiat aperiam culpa mollitia, sed provident labore animi commodi? Aliquid, quidem sint impedit mollitia ipsum quisquam eius. Asperiores sapiente eum ratione voluptates. Expedita cumque optio rerum autem commodi dolore inventore illo beatae ipsa sapiente, culpa delectus iste quidem?</div> <!-- new element for lore text -->
        </div>
    </div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="b-game-card" on:click={() => goToQuestion(3)}>
        <div class="b-game-card__cover" style="background-image: url(https://cdn.leonardo.ai/users/ac66a632-504c-41ea-b756-c7ccd8400f7a/generations/6f466adc-b166-4929-bcfc-a99f3043af7a/variations/Default_a_photo_of_8k_ultra_realistic_beautiful_sad_girl_stand_0_6f466adc-b166-4929-bcfc-a99f3043af7a_1.jpg);">
            <div class="name">Miko Mana</div>
            <div class="tag">Funny, Cute, Clever</div>
            <div class="b-game-card__lore">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Optio omnis aperiam excepturi modi rem hic incidunt quibusdam, esse commodi, laboriosam velit nulla cupiditate? Aliquam, repellendus beatae. Distinctio asperiores facere nihil nisi quos fugiat aperiam culpa mollitia, sed provident labore animi commodi? Aliquid, quidem sint impedit mollitia ipsum quisquam eius. Asperiores sapiente eum ratione voluptates. Expedita cumque optio rerum autem commodi dolore inventore illo beatae ipsa sapiente, culpa delectus iste quidem?</div> <!-- new element for lore text -->
        </div>
    </div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="b-game-card" on:click={() => goToQuestion(4)}>
        <div class="b-game-card__cover" style="background-image: url(https://cdn.leonardo.ai/users/ed6862c2-50bf-41c9-be15-c865e8e83377/generations/55901757-3cfe-4979-ac89-9f55c33836a9/variations/Default_Plague_Doctor_Al_Silmons_is_Plague_doctor_drawn_by_Tod_0_55901757-3cfe-4979-ac89-9f55c33836a9_1.jpg);">
            <div class="name">The Crow</div>
            <div class="tag">Dark, Scary</div>
            <div class="b-game-card__lore">Lorem ipsum dolor, sit amet consectetur adipisicing elit. Optio omnis aperiam excepturi modi rem hic incidunt quibusdam, esse commodi, laboriosam velit nulla cupiditate? Aliquam, repellendus beatae. Distinctio asperiores facere nihil nisi quos fugiat aperiam culpa mollitia, sed provident labore animi commodi? Aliquid, quidem sint impedit mollitia ipsum quisquam eius. Asperiores sapiente eum ratione voluptates. Expedita cumque optio rerum autem commodi dolore inventore illo beatae ipsa sapiente, culpa delectus iste quidem?</div> <!-- new element for lore text -->
        </div>
    </div>
</div>
{/if}

{#if hideQuestion}
<!-- question ask user for a question -->
<div class="absolute-center">
    <div class="awnser"> Ask your Question</div>
        <form on:submit={askQuestion} class="flex">
            <input
                type="text"
                class="te text-3xl p-3 max-w-200 w-70vw  border rounded-l-lg"
                bind:value={question}
                placeholder="Enter your question here"
            />
            <button type="submit" class=" but text-4xl text-white rounded-r-lg px-10">Ask</button>
        </form>
</div>
{/if}
</div>

{#if hideLoader}
    <div class="absolute-center">
        <Wave size="80" color="#FF3E00" unit="px" duration="2s" />
    </div>
{/if}

<style lang="postcss">  
.te{
    font-family: theme(fontFamily.amatic);
}

.but{
    @apply bg-accent;
    font-family: theme(fontFamily.amatic);
}
.absolute-center {
	position: absolute;
	top: 40%;
	left: 50%;
	transform: translate(-50%, -50%);
	}

.awnser {
    color: white;
	text-align: center;
    font-size: xxx-large;
    margin: 0% auto;
    @apply text-accent; 
    font-family: theme(fontFamily.amatic);
}
.subtask{
    max-width: 75%;
    text-align: center;
    margin: auto;
    color: white;
    font-size: x-large;
    font-family: theme(fontFamily.amatic);
}

.l-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 30px;
    width: 100%;
    padding: 30px;
    justify-content: center;

    @media screen and (max-width: 1150px) {
    grid-template-columns: repeat(1, 1fr);
    }
}

.b-game-card__lore {
    display: none; /* hide the lore text initially */
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: #fff;
    padding: 10px;
    font-size: 14px;
    line-height: 1.5;
    text-align: center;
    transform: translateY(100%);
    transition: transform .35s ease-in-out;
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
    
.name{
    font-size: xx-large;
    font-weight: bold;
    color: rgb(252, 252, 252);
    text-align: center;
}

.tag {
    text-align: center;
    background: #eee;
    margin: 0 50px 5px 50px;
    width: auto;
    color: black;
    font-size: large;
    font-weight: bold;
    @apply text-accent; 
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
    transform: skewX(.001deg);
    transition: transform .35s ease-in-out;
    // Gloss 
&::after {
    display: block;
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 120%;
    transform: translateY(-20%);
    will-change: transform;
    transition: transform .65s cubic-bezier(0.18, 0.9, 0.58, 1);
}}
&:hover &__cover {
    transform: rotateX(7deg) translateY(-6px);

    &::after {
    transform: translateY(0%);
    }
}
}

</style>