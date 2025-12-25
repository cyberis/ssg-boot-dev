class HTMLNode:
    def __init__(self, tag=None, value=None, children=None , props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        attrs = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        if attrs:
            return f' {attrs}'  # Note the leading space
        else:
            return ""

    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def __str__(self):
        attrs = ' '.join(f'{key}="{value}"' for key, value in self.props.items())
        if attrs:
            return f'<{self.tag}{attrs}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
        

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props: dict = None):
        super().__init__(tag, value, children, props)
        if self.value is None:
            raise ValueError("LeafNodes must have a value")
        if self.children is not None:
            raise ValueError("LeafNodes cannot have children")
        
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNodes must have a value to convert to HTML")
        attrs = self.props_to_html()
        if self.tag == None:
            return self.value
        return f'<{self.tag}{attrs}>{self.value}</{self.tag}>'
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None, value=None):
        super().__init__(tag, value, children, props)
        if self.tag is None:
            raise ValueError("ParentNodes must have a tag")
        if self.value is not None:
            raise ValueError("ParentNodes cannot have a value")
        if self.children is None or not isinstance(self.children, list) or len(self.children) == 0:
            raise ValueError("ParentNodes must have a non-empty list of children")
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNodes must have a tag")
        if self.value is not None:
            raise ValueError("ParentNodes cannot have a value")
        if self.children is None or not isinstance(self.children, list) or len(self.children) == 0:
            raise ValueError("ParentNodes must have a non-empty list of children")
        attrs = self.props_to_html()
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{attrs}>{children_html}</{self.tag}>'