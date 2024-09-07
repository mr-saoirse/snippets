# Setting up a FastHTML project

Im going to focus on the tailwind version first. Download the stand-alone cli from [here](https://tailwindcss.com/blog/standalone-cli) and use the official [guide](https://tailwindcss.com/docs/installation). I added an alias/symlink for the downloaded cli.

```bash
tailwind init
```

this creates a config file. You can add the directives to your `input.css` file and then use tailwind to generate the bits with an optional `--watch` flag.

```bash
tailwind -i input.css -o main.css 

```

My config looks like this - important to apply to HTML pages in our case and I have added some of the optional plugins

```css
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html'],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

