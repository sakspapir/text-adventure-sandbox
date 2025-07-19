class Room:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj_name):
        self.objects = [obj for obj in self.objects if obj.name != obj_name]

    def list_objects(self):
        return [obj.name for obj in self.objects]

    def describe(self):
        object_list = ", ".join(self.list_objects()) or "nothing"
        return f"{self.description}\nYou see: {object_list}."

