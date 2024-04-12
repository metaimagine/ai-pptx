# utils.py


def generate_slides_html(slides):
    slides_html = []
    processed_titles = set()

    for slide in slides:
        if slide["title"] in processed_titles:
            continue

        background_html = (
            slide["background"].generate_html() if "background" in slide else ""
        )

        if slide["group"]:
            # This slide is part of a group
            group_slides = [s for s in slides if s["group"] == slide["group"]]
            vertical_slides_html = "\n".join(
                [
                    f"<section {sub_slide['background'].generate_html() if 'background' in sub_slide else ''}>{sub_slide['content']}</section>"
                    for sub_slide in group_slides
                ]
            )
            slides_html.append(
                f"<section {background_html}>\n{vertical_slides_html}\n</section>"
            )
            processed_titles.add(slide["group"])
        else:
            slides_html.append(
                f"<section {background_html}>{slide['content']}</section>"
            )

    return "\n".join(slides_html)


def wrap_in_html_template(title, theme, transition, slides_html):
    """Wrap the slides HTML in the full Reveal.js template."""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="revealjs/dist/reveal.css">
        <link rel="stylesheet" href="revealjs/dist/theme/{theme}.css">
        <script src="revealjs/dist/reveal.js"></script>
        

    </head>
    <body>
        <div class="reveal">
            <div class="slides">
                {slides_html}
            </div>
        </div>
        <script>
            Reveal.initialize({{
                transition: '{transition}'
            }});
        </script>
    </body>
    </html>
    """
