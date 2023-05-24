import path from "path";
import adapter from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/kit/vite";

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),

	kit: {
		adapter: new adapter(),
		alias: {
			"#lib": path.resolve("./src/lib")
		}
	}
};

export default config;
