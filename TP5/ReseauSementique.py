class SemanticNetwork:
    def __init__(self):
        self.nodes = {}
        self.links = {}

    def add_node(self, node_name, properties=None):
        if properties is None:
            properties = {}
        self.nodes[node_name] = properties
        return self

    def add_link(self, source, relation, target, link_type="normal"):
        self.links[(source, relation, target)] = link_type
        return self

    def add_is_a_link(self, source, target, link_type="normal"):
        return self.add_link(source, "is-a", target, link_type)

    def add_property(self, node_name, property_name, property_value):
        if node_name not in self.nodes:
            self.add_node(node_name)
        self.nodes[node_name][property_name] = property_value
        return self

    def get_property(self, node_name, property_name):
        if node_name in self.nodes and property_name in self.nodes[node_name]:
            return self.nodes[node_name][property_name]
        return None

    def get_links_from(self, source, relation=None):
        result = []
        for (src, rel, target), link_type in self.links.items():
            if src == source and (relation is None or rel == relation):
                result.append((rel, target, link_type))
        return result

    def get_links_to(self, target, relation=None):
        result = []
        for (src, rel, tgt), link_type in self.links.items():
            if tgt == target and (relation is None or rel == relation):
                result.append((src, rel, link_type))
        return result

    def visualize(self):
        print("Nœuds:")
        for node, props in self.nodes.items():
            print(f"  {node}: {props}")

        print("\nLiens:")
        for (src, rel, tgt), link_type in self.links.items():
            exception_mark = " [EXCEPTION]" if link_type == "exception" else ""
            print(f"  {src} --({rel})--> {tgt}{exception_mark}")

def marker_propagation(network, marked_nodes, relations, max_depth=10):
    reached_nodes = {node: [[node]] for node in marked_nodes}
    queue = [(node, 0) for node in marked_nodes]
    while queue:
        current_node, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        for relation, target, link_type in network.get_links_from(current_node):
            if relation in relations and link_type == "normal":
                if target not in reached_nodes:
                    reached_nodes[target] = []
                    queue.append((target, depth + 1))
                for path in reached_nodes[current_node]:
                    new_path = path + [target]
                    if new_path not in reached_nodes[target]:
                        reached_nodes[target].append(new_path)
    for node in marked_nodes:
        if node in reached_nodes:
            del reached_nodes[node]
    return reached_nodes

def inherit_properties(network, node_name):
    if node_name not in network.nodes:
        return {}
    properties = network.nodes[node_name].copy()
    is_a_links = []
    for relation, target, link_type in network.get_links_from(node_name):
        if relation == "is-a" and link_type == "normal":
            is_a_links.append(target)
    for parent in is_a_links:
        parent_properties = inherit_properties(network, parent)
        for prop, value in parent_properties.items():
            if prop not in properties:
                properties[prop] = value
    return properties

def inherit_properties_with_exceptions(network, node_name):
    if node_name not in network.nodes:
        return {}
    properties = network.nodes[node_name].copy()
    exception_properties = set()
    for (src, rel, tgt), link_type in network.links.items():
        if src == node_name and link_type == "exception" and rel.startswith("has_"):
            exception_properties.add(rel[4:])
    is_a_links = []
    for relation, target, link_type in network.get_links_from(node_name):
        if relation == "is-a" and link_type == "normal":
            is_a_links.append(target)
    for parent in is_a_links:
        parent_properties = inherit_properties_with_exceptions(network, parent)
        for prop, value in parent_properties.items():
            if prop not in properties and prop not in exception_properties:
                properties[prop] = value
    return properties

def marker_propagation_with_exceptions(network, marked_nodes, relations, max_depth=10):
    reached_nodes = {node: [[node]] for node in marked_nodes}
    queue = [(node, 0) for node in marked_nodes]
    exception_links = {(src, rel, tgt) for (src, rel, tgt), link_type in network.links.items() if link_type == "exception"}

    while queue:
        current_node, depth = queue.pop(0)
        if depth >= max_depth:
            continue
        for relation, target, link_type in network.get_links_from(current_node):
            if relation in relations:
                blocked = False
                if (current_node, relation, target) in exception_links:
                    blocked = True
                for is_a_source, _, parent in network.links.items():
                    if is_a_source[0] == current_node and is_a_source[1] == "is-a":
                        if (is_a_source[2], relation, target) in exception_links:
                            blocked = True
                            break
                if not blocked:
                    if target not in reached_nodes:
                        reached_nodes[target] = []
                        queue.append((target, depth + 1))
                    for path in reached_nodes[current_node]:
                        new_path = path + [target]
                        if new_path not in reached_nodes[target]:
                            reached_nodes[target].append(new_path)

    for node in marked_nodes:
        if node in reached_nodes:
            del reached_nodes[node]
    return reached_nodes

# MAIN PROGRAM EXECUTION

if __name__ == "__main__":
    network = SemanticNetwork()

    # Création des noeuds
    network.add_node("Animal", {"vivant": True})
    network.add_node("Oiseau")
    network.add_node("Pingouin")
    network.add_node("Aigle")
    network.add_node("Mammifère")
    network.add_node("Chien")
    network.add_node("Labrador")

    # Création des relations d'héritage
    network.add_is_a_link("Oiseau", "Animal")
    network.add_is_a_link("Mammifère", "Animal")
    network.add_is_a_link("Pingouin", "Oiseau")
    network.add_is_a_link("Aigle", "Oiseau")
    network.add_is_a_link("Chien", "Mammifère")
    network.add_is_a_link("Labrador", "Chien")

    # Ajout des propriétés
    network.add_property("Oiseau", "peut_voler", True)
    network.add_property("Oiseau", "a_des_plumes", True)
    network.add_property("Mammifère", "allaite", True)
    network.add_property("Mammifère", "a_des_poils", True)

    # Déclaration d'une exception + propriété locale
    network.add_link("Pingouin", "peut_voler", True, "exception")
    network.add_property("Pingouin", "peut_voler", False)

    # Visualisation
    print("Réseau sémantique:")
    network.visualize()

    # --- Partie 3: Gestion des exceptions ---
    # Hérite les propriétés pour Pingouin avec gestion des exceptions
    print("\n--- Partie 3: Gestion des exceptions ---")
    pingouin_props_exc = inherit_properties_with_exceptions(network, "Pingouin")
    print("\nPropriétés héritées pour Pingouin (avec gestion des exceptions):")
    for prop, value in pingouin_props_exc.items():
        print(f"  {prop}: {value}")

    # Exemple de propagation avec exceptions
    print("\nPropagation avec exceptions:")
    result_exc = marker_propagation_with_exceptions(network, ["Animal"], ["is-a"])
    for node, paths in result_exc.items():
        print(f"  {node}:")
        for path in paths:
            print(f"    {' -> '.join(path)}")
