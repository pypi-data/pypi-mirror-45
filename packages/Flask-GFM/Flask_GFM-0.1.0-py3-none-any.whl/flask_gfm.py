from flaskext.markdown import Markdown as BaseMarkdown
from mdx_gfm import GithubFlavoredMarkdownExtension


class Markdown(BaseMarkdown):
    def __init__(self, app, auto_escape=False, **markdown_options):
        super().__init__(
            app=app,
            auto_escape=auto_escape,
            **markdown_options
        )
        self.register_extension(GithubFlavoredMarkdownExtension)
