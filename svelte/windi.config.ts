import { defineConfig } from "windicss/helpers";

export default defineConfig({
	/* configurations... */
	theme: {
		extend: {
			colors: {
				dark: "#121212",
				fontcolor: "#fff7e2",
				accent: "#FB5012",
				metal: "#808080"
			},
			fontFamily: {
				medieval: ["MedievalSharp", "serif"],
				eczar: ["Eczar-Regular", "sans-serif"],
				amatic: ["Amatic-SC-Regular", "sans-serif"],
				montserrat: ["Montserrat-Variable", "sans-serif"]
			},
			borderRadius: {}
		}
	}
});
