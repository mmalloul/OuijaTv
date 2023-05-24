import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";
import WindiCSS from "vite-plugin-windicss";

export default defineConfig({
	plugins: [sveltekit(), WindiCSS()],
	test: {
		globals: true,
		environment: "jsdom",
		include: ["tests/**/*.{test,spec}.{js,ts}"],
		setupFiles: ["./setupTest.js"]
	}
});
