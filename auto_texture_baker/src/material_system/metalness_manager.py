"""
This module handle rewrangling of metallic nodes due to issues with blender metallic baking
"""

class MetallicConnection:
    def __init__(self, material):
        self.material = material            # Material
        self.node_tree = None               # Node tree of this material
        self.metallic_node = None           # Node connected to the principled BSDF
        self.principled_bsdf = None         # Principled BSDF Node
        self.output_node = None             # Output node of the node tree

    def prepare_metallic_values(self): 
        """ Find all required nodes for rewrangling during pre-post baking stages
            Creates a new node for metallic value if not exist
        """
        self.node_tree = self.material.node_tree 
        metallic_value = 0

        # Search for the Principled BSDF node and get the metallic value
        for node in self.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                self.principled_bsdf = node
                metallic_value = self.principled_bsdf.inputs['Metallic'].default_value
                break
            
        if not self.principled_bsdf:
            print("No Principled BSDF node found in the material")
            return False

        # Find or create metallic node         
        metallic_input = self.principled_bsdf.inputs['Metallic']
        if metallic_input.is_linked:  
            self.metallic_node = metallic_input.links[0].from_node  # Get the node connected to the metallic input
        else: 
            self.create_metallic_node(metallic_value)

        # Find output node
        self._find_material_output()

        return True
    
    def _find_material_output(self):
        """Find material output node"""
        for node in self.node_tree.nodes:
            if node.type == 'OUTPUT_MATERIAL':
                self.output_node = node
                break

    def create_metallic_node(self, metallic_value): 
        """Create a new RGB node for storing metallic value if there exist no node connection to the Principled BSDF"""
        node_tree= self.node_tree
        rgb_node = node_tree.nodes.new('ShaderNodeRGB')
        rgb_node.outputs[0].default_value = (metallic_value, metallic_value, metallic_value, 1)  # (R, G, B, A)

        # Connect the new RGB node to BSDF Metallic slot
        self.metallic_node = rgb_node
        self.node_tree.links.new(self.metallic_node.outputs[0], self.principled_bsdf.inputs['Metallic'])

    def prepare_bake_metallic(self): 
        """Links metallic node directly to output """
        self.node_tree.links.new(self.metallic_node.outputs[0], self.output_node.inputs['Surface'])


        # TODO: We have to deal with linking back BSDF to output after this stage.

    def prepare_bake_others(self):
        """Unlink metallic node and set value to 0"""
        # Find metallic link
        metallic_link = None
        for link in self.node_tree.links:
            if link.from_node == self.metallic_node and link.to_node == self.principled_bsdf:
                metallic_link = link
                break
        
        # Remove link if exist 
        if metallic_link:
            self.node_tree.links.remove(metallic_link)
        self.principled_bsdf.inputs['Metallic'].default_value = 0
