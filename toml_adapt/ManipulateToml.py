import toml
import fileinput
import sys

class ManipulateToml():
    def __init__(self, path, action, dependency, version):
        self.path = path
        self.action = action
        self.dependency = dependency
        self.version = version

        #load file
        self.data = toml.load(self.path)
        self.tools = []
        self.get_tools()
        self.project_name = self.get_project_name()
        self.primary_tool = self.get_primary_tool()

    def get_project_name(self):
        #for poetry
        if "poetry" in self.tools:
            return self.data['tool']['poetry']['name']

    def get_primary_tool(self):
        if "poetry" in self.tools:
            return "poetry"

    def get_tools(self):
        for key, val in self.data.items():
            for k, v in val.items():
                self.tools.append(k)

    def get_dependencies(self):
        return (self.data['tool'][self.primary_tool]['dependencies'])
    
    def get_dev_dependencies(self):
        return (self.data['tool'][self.primary_tool]['dev-dependencies'])

    def get_names_of_dependencies(self):
        return list(self.get_dependencies().keys())
    
    def get_names_of_dev_dependencies(self):
        return list(self.get_dev_dependencies().keys())

    def get_versions_of_dependencies(self):
        return list(self.get_dependencies().values())

    def get_number_of_dependencies(self):
        return len(self.get_dependencies())

    def check_for_specific_version(self, version):
        return self.get_versions_of_dependencies().count(version)

    def change_dep_version(self, dependency, version):
        if version == "X":
            version = "*"
        dependencies_dict=self.data['tool'][self.primary_tool]['dependencies']
        if dependency == "ALL":
            all_deps = self.get_names_of_dependencies()
            for i in range(len(all_deps)):
                dependencies_dict[all_deps[i]] = version
        else:
            dependencies_dict[dependency] = version
            
    def change_dev_dep_version(self, dependency, version):
        if version == "X":
            version = "*"
        dev_dependencies_dict=self.data['tool'][self.primary_tool]['dev-dependencies']
        if dependency == "ALL":
            all_deps = self.get_names_of_dev_dependencies()
            for i in range(len(all_deps)):
                dev_dependencies_dict[all_deps[i]] = version
        else:
            dev_dependencies_dict[dependency] = version

    def remove_dep(self, dependency):
        data = self.get_dependencies()
        try:
            data.pop(dependency)
        except KeyError:
            print("Dependency is not present in current dependency list!")

        return data
    
    def remove_dev_dep(self, dependency):
        data = self.get_dev_dependencies()
        try:
            data.pop(dependency)
        except KeyError:
            print("Dependency is not present in current dependency list!")

        return data

    def add_dep(self, dependency, version):
        data = self.get_dependencies()
        if version == "X":
            version = "*"

        data[dependency] = version
        return data
    
    def add_dev_dep(self, dependency, version):
        data = self.get_dev_dependencies()
        if version == "X":
            version = "*"

        data[dependency] = version
        return data

    def make_action(self):
        if self.action == "change":
            self.change_dep_version(self.dependency, self.version)
        elif self.action == "change-dev":
            self.change_dev_dep_version(self.dependency,self.version)
        elif self.action == "add":
            self.add_dep(self.dependency, self.version)
        elif self.action == "remove":
            self.remove_dep(self.dependency)
        elif self.action == "add-dev":
            self.add_dev_dep(self.dependency, self.version)
        elif self.action == "remove-dev":
            self.remove_dev_dep(self.dependency)
            

    def dump_to_file(self):
        with open(self.path, "w") as toml_file:
            toml.dump(self.data, toml_file)
