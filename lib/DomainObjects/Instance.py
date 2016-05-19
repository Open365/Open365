class Instance:
    def __init__(self, name, instance_id):
        self.name = name
        self.id = instance_id

    @classmethod
    def from_openstack_server(cls, novaserver):
        return cls(novaserver.name, novaserver.id)
