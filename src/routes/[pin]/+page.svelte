<script>
    import BoardSvg from "$lib/components/BoardSVG.svelte";

    let seekerX = 0;
    let seekerY = 0;
</script>
<BoardSvg>
    <circle
        id="Seeker"
        cx={seekerX}
        cy={seekerY}
        r="76.5"
        stroke="#FFF7E2"
        stroke-width="13"
    />
</BoardSvg>