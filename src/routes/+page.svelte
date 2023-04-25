<div class="flex flex-col max-w-50 gap-3 absolute-center pb-8">
    <button type="button">Host</button>
    <button disabled type="button">Join</button>
</div>

<style lang="scss">
    // this CSS is scoped, so it's fine to target components directly
    button {
        background: #1d6589;
        color: #fff;
        padding: 1rem 5rem 1rem 5rem;
        border-radius: 1rem;
        font-size: large;
        font-weight: 500;

        &:disabled {
            background: #ccc;
            color: rgb(148, 148, 148);
            cursor: not-allowed;
        }
    }

    .absolute-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
</style>