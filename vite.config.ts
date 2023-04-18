import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";
import WindiCSS from "vite-plugin-windicss";

export default defineConfig({
	plugins: [sveltekit(), WindiCSS()],
	test: {
		include: ["src/**/*.{test,spec}.{js,ts}"]
	}
});
