import { defineConfig } from "windicss/helpers";

export default defineConfig({
	/* configurations... */
	theme: {
		extend: {
			colors: {
				dark: "#121212"
			},
			fontFamily: {
				title: ["MedievalSharp", "serif"],
				text: ["Eczar-Regular", "sans-serif"]
			},
			spacing: {
				padding: {
					small: "8px",
					medium: "16px",
					large: "24px"
				}
			},
			borderRadius: {}
		}
	}
});
