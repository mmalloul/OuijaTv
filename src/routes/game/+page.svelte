<script lang="ts">
    import BoardSvg from "$lib/components/BoardSVG.svelte";

    function handleClick()
    {
        console.log()
    }

    let seekerX = 960, seekerY = 540

    function update(_progress: number) 
    {
        // Update the state of the world for the elapsed time since last render
        seekerX += getRandomInt(-10, 10);
        seekerY += getRandomInt(-10,10);
    }

    function draw() {
        // Draw the state of the world
    }

    function getRandomInt(a: number, b: number): number {
        const min = Math.ceil(a);
        const max = Math.floor(b);
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }



    function loop(timestamp: number) {
        var progress = timestamp - lastRender

        update(progress)
        draw()

        lastRender = timestamp
        window.requestAnimationFrame(loop)
    }

    var lastRender = 0
    window.requestAnimationFrame(loop)
</script>



<div id="wrapper">
    <label>
        <input type="range" bind:value={seekerX} min=0 max=1920>
        <input type="range" bind:value={seekerY} min=0 max=1080>
    </label>

    <BoardSvg>
        <circle id="Seeker" cx={seekerX} cy={seekerY} r="76.5" stroke="#FFF7E2" stroke-width="13"/>
    </BoardSvg>
</div>



<style>
/* TODO: remove dirty override */
:global(body) { 
    background: radial-gradient(rgb(33, 33, 33), black) !important;
}

circle {
    transition: cx .5s, cy .5s;
}

#wrapper {
    height: 75%;
    width: 75%;
}
</style>