def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split('\n\n')
    markdown_blocks = [block.strip() for block in markdown_blocks if block.strip()]
    #markdown_blocks = [block.replace('"', '\\"') for block in markdown_blocks]
    return markdown_blocks